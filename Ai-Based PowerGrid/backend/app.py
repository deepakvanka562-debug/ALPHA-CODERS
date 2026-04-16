import os
import random
import uuid
import logging
import mysql.connector
from flask import Flask, request, jsonify, has_request_context
from flask_cors import CORS
from redis import Redis
from rq import Queue
from utils import preprocess_input, evaluate_risk, generate_recommendations
from auth import token_required, generate_tokens, rbac_admin_required

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

# Add filter to root logger and suppress Werkzeug's verbose debug logging
root_logger = logging.getLogger()
root_logger.addFilter(TraceIdFilter())
logging.getLogger('werkzeug').setLevel(logging.WARNING)

app = Flask(__name__)
CORS(app)

# Phase 3: Setup Redis Queue
redis_conn = Redis(host='127.0.0.1', port=6379)
q = Queue(connection=redis_conn)

@app.before_request
def before_request():
    request.trace_id = request.headers.get('X-Trace-Id', str(uuid.uuid4()))

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='power_grid_db'
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Phase 2: Login Route for JWT
@app.route('/login', methods=['POST'])
def login():
    logger.info("Processing login request")
    data = request.json
    username = data.get('username')
    password = data.get('password') # In a real app, verify password
    
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
@token_required # Phase 2: Secure Endpoint
def predict():
    data = request.json
    logger.info(f"Received prediction request. User: {request.user['username']}")
    
    try:
        features = preprocess_input(data)
        
        # Dispatch to Queue (Phase 3)
        # We need to pass 'data' context so the task status can build recommendations, 
        # or we just get prob_pred/delay_pred from the worker and construct recommendations locally on completion.
        # Process asynchronously via Event Queue
        from worker import perform_prediction
        job = q.enqueue(perform_prediction, features, request.trace_id, data)
        
        logger.info(f"Enqueued job {job.id} to RabbitMQ/Redis queue.")
        return jsonify({"task_id": job.id, "status": "processing"}), 202
        
    except Exception as e:
        logger.error(f"Prediction dispatch error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/task-status/<task_id>', methods=['GET'])
@token_required
def get_status(task_id):
    job = q.fetch_job(task_id)
    if not job:
        return jsonify({"error": "No such task"}), 404
        
    if job.is_finished:
        result = job.result
        # The worker returned {"prob_pred": x, "delay_pred": y}
        # In a real app we'd pass original input data to construct recommendations and log it.
        # For simplicity, we just format the mock result.
        risk_level = evaluate_risk(result['prob_pred'])
        
        logger.info(f"Task {task_id} completed successfully.")
        return jsonify({
            "status": "finished",
            "failure_probability": round(result['prob_pred'], 1),
            "risk_level": risk_level,
            "expected_delay_hours": round(result['delay_pred'], 1),
            "zone_name": result['zone_name']
        }), 200
        
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

if __name__ == '__main__':
    logger.info("Starting Flask application with Async Queue enabled")
    app.run(debug=True, port=5000, host="0.0.0.0")
