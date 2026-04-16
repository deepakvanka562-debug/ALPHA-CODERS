import os
import random
import re
import uuid
import logging
import mysql.connector
import threading
import requests
import json
from flask import Flask, request, jsonify, has_request_context
from flask_cors import CORS
from utils import preprocess_input, evaluate_risk, generate_recommendations
from auth import token_required, generate_tokens, rbac_admin_required

# Import config from parent directory
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import (
    OPENAI_API_KEY, WEATHER_API_KEY, POWER_GRID_API_KEY,
    DATABASE_CONFIG, API_ENDPOINTS, MODEL_CONFIG, JWT_SECRET_KEY
)

# Phase 4: Observability & Logging setup
class TraceIdFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'trace_id'):
            record.trace_id = 'background-job'
        return super().format(record)

# Configure logging with custom formatter
logging.basicConfig(level=logging.INFO)
formatter = TraceIdFormatter('%(asctime)s - %(name)s - %(levelname)s - [Trace: %(trace_id)s] - %(message)s')

# Get all handlers and set the formatter
for handler in logging.root.handlers:
    handler.setFormatter(formatter)

# Also apply to werkzeug logger (suppressed)
logging.getLogger('werkzeug').setLevel(logging.WARNING)

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'trace_id'):
            if has_request_context():
                record.trace_id = getattr(request, 'trace_id', 'background-job')
            else:
                record.trace_id = 'background-job'
        return True

logger = logging.getLogger("api-service")
logger.addFilter(TraceIdFilter())

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

logger.info(f"MODEL_CONFIG={MODEL_CONFIG}")
logger.info(f"OPENAI_API_KEY set={bool(OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here')}")

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

# In-memory job storage (no Redis required)
jobs_storage = {}
jobs_lock = threading.Lock()

class SimpleJob:
    def __init__(self, job_id):
        self.id = job_id
        self.result = None
        self.is_finished = False
        self.is_failed = False
        self.status = "queued"

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def fetch_weather_data(zone_name, temperature):
    """Fetch real weather data using API key"""
    try:
        if not WEATHER_API_KEY or WEATHER_API_KEY == "your_weather_api_key_here":
            return None

        # Example: Use weather API to get current conditions
        params = {
            'key': WEATHER_API_KEY,
            'q': zone_name,  # Use zone as location
            'aqi': 'no'
        }

        response = requests.get(API_ENDPOINTS['weather'], params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['current']['temp_c'],
                'humidity': data['current']['humidity'],
                'wind_speed': data['current']['wind_kph'],
                'condition': data['current']['condition']['text']
            }
    except Exception as e:
        logger.warning(f"Weather API failed: {e}")
    return None

def extract_json_from_text(text):
    cleaned = re.sub(r'```(?:json)?\n', '', text, flags=re.IGNORECASE).replace('```', '').strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    start = cleaned.find('{')
    if start == -1:
        raise ValueError('No JSON object found in text')

    depth = 0
    for idx in range(start, len(cleaned)):
        ch = cleaned[idx]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                candidate = cleaned[start:idx + 1]
                return json.loads(candidate)

    raise ValueError('Could not extract JSON object from text')


def predict_with_api(features, zone_name):
    """Use API for AI-powered predictions"""
    try:
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
            return None

        prompt = f"""
        Analyze power grid failure risk based on these parameters:
        Zone: {zone_name}
        Voltage: {features.get('voltage', 230)} kV
        Load: {features.get('load', 150)} MW
        Temperature: {features.get('temperature', 35)} °C

        Provide a realistic prediction in JSON format:
        {{
            "failure_probability": 0.XX (0-1 scale),
            "expected_delay_hours": XX.X (hours),
            "risk_level": "LOW/MEDIUM/HIGH",
            "recommendations": ["brief action items"]
        }}
        """

        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 200,
            'temperature': 0.3
        }

        response = requests.post(
            API_ENDPOINTS['openai'],
            headers=headers,
            json=data,
            timeout=MODEL_CONFIG['prediction_timeout']
        )
        logger.info(f"OpenAI API returned status {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            logger.info(f"OpenAI content: {content[:512]}")

            try:
                prediction = json.loads(content)
            except json.JSONDecodeError:
                try:
                    prediction = extract_json_from_text(content)
                except Exception as parse_error:
                    logger.warning(f"Failed to parse OpenAI JSON response: {parse_error}; content={content}")
                    return None

            return {
                'prob_pred': prediction['failure_probability'],
                'delay_pred': prediction['expected_delay_hours'],
                'zone_name': zone_name,
                'recommendations': prediction.get('recommendations', []),
                'source': 'openai'
            }
        else:
            logger.warning(f"OpenAI returned status {response.status_code}: {response.text}")

    except Exception as e:
        logger.error(f"API prediction failed: {e}")

    return None

# Phase 2: Login Route for JWT
@app.route('/login', methods=['POST'])
def login():
    logger.info("Processing login request")
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Simple role assignment for demonstration
    role = 'Admin' if username == 'admin' else 'General User'
    
    access_token, refresh_token = generate_tokens(username, role)
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'role': role
    })

# Phase 3: Event-Driven Predict Route
@app.route('/predict', methods=['POST'])
@token_required
def predict():
    data = request.json
    logger.info(f"Received prediction request. User: {request.user['username']}")
    
    try:
        features = preprocess_input(data)
        
        # Create a job and process it in background thread
        job_id = str(uuid.uuid4())
        job = SimpleJob(job_id)
        
        with jobs_lock:
            jobs_storage[job_id] = job
        
        def process_job():
            job.status = "processing"
            try:
                # Try API prediction first
                if MODEL_CONFIG['use_api_predictions']:
                    api_result = predict_with_api(features, data.get('zone_name', 'Zone-A'))
                    if api_result:
                        job.result = api_result
                        job.is_finished = True
                        job.status = "finished"
                        logger.info(f"API prediction completed for job {job_id}")
                        return

                # Fallback to mock prediction if API fails or disabled
                if MODEL_CONFIG['fallback_to_mock']:
                    logger.info(f"Using mock prediction for job {job_id}")

                    # Fetch weather data if available
                    weather_data = fetch_weather_data(
                        data.get('zone_name', 'Zone-A'),
                        data.get('temperature', 35)
                    )

                    # Use weather data to influence prediction if available
                    base_temp = weather_data['temperature'] if weather_data else data.get('temperature', 35)
                    base_load = data.get('load', 150)
                    base_voltage = data.get('voltage', 230)

                    # More realistic prediction based on conditions
                    if base_temp > 40:  # High temperature increases risk
                        prob_pred = random.uniform(0.3, 0.8)
                    elif base_load > 200:  # High load increases risk
                        prob_pred = random.uniform(0.2, 0.7)
                    elif base_voltage < 220:  # Low voltage increases risk
                        prob_pred = random.uniform(0.25, 0.75)
                    else:
                        prob_pred = random.uniform(0.1, 0.5)

                    # Delay prediction based on risk
                    if prob_pred > 0.6:
                        delay_pred = random.uniform(20, 48)  # High risk = longer delays
                    elif prob_pred > 0.3:
                        delay_pred = random.uniform(5, 25)   # Medium risk
                    else:
                        delay_pred = random.uniform(1, 10)   # Low risk = quick fixes

                    job.result = {
                        'prob_pred': prob_pred,
                        'delay_pred': delay_pred,
                        'zone_name': data.get('zone_name', 'Zone-A'),
                        'weather_data': weather_data,
                        'source': 'mock'
                    }
                    job.is_finished = True
                    job.status = "finished"
                    logger.info(f"Mock prediction completed for job {job_id}")
                else:
                    job.is_failed = True
                    job.status = "failed"
                    logger.error(f"No prediction method available for job {job_id}")

            except Exception as e:
                job.is_failed = True
                job.status = "failed"
                logger.error(f"Job {job_id} failed: {e}")
        
        # Start background thread
        thread = threading.Thread(target=process_job, daemon=True)
        thread.start()
        
        logger.info(f"Created job {job_id} for processing")
        return jsonify({"task_id": job_id, "status": "processing"}), 202
        
    except Exception as e:
        logger.error(f"Prediction dispatch error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/task-status/<task_id>', methods=['GET'])
@token_required
def get_status(task_id):
    with jobs_lock:
        job = jobs_storage.get(task_id)
    
    if not job:
        return jsonify({"error": "No such task"}), 404
        
    if job.is_finished:
        result = job.result
        risk_level = evaluate_risk(result['prob_pred'])

        response_data = {
            "status": "finished",
            "failure_probability": round(result['prob_pred'], 1),
            "risk_level": risk_level,
            "expected_delay_hours": round(result['delay_pred'], 1),
            "zone_name": result['zone_name']
        }

        # Add weather data if available
        if 'weather_data' in result and result['weather_data']:
            response_data['weather'] = result['weather_data']

        # Add recommendations if available from API
        if 'recommendations' in result and result['recommendations']:
            response_data['recommendations'] = result['recommendations']
        else:
            # Generate default recommendations based on risk
            response_data['recommendations'] = generate_recommendations(result, risk_level)

        response_data['prediction_source'] = result.get('source', 'unknown')

        logger.info(f"Task {task_id} completed successfully.")
        return jsonify(response_data), 200
        
    elif job.is_failed:
        logger.error(f"Task {task_id} failed.")
        return jsonify({"status": "failed"}), 500
    else:
        return jsonify({"status": "processing"}), 202

# Phase 2: Secure Admin Endpoint
@app.route('/admin/logs', methods=['GET'])
@token_required
@rbac_admin_required
def get_logs():
    return jsonify({"message": "You have accessed the secure Admin Logs console."})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "version": "1.0.0"}), 200

@app.route('/debug/openai', methods=['GET'])
def debug_openai():
    result = predict_with_api({'voltage': 230, 'load': 150, 'temperature': 35}, 'Zone-A')
    return jsonify({
        'openai_key_set': bool(OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here'),
        'model_config': MODEL_CONFIG,
        'result': result
    }), 200

if __name__ == '__main__':
    logger.info("Starting Flask application (Simple Mode - No Redis required)")
    app.run(debug=False, use_reloader=False, port=5000, host="0.0.0.0")
