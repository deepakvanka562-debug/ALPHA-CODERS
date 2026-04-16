"""
Configuration file for API keys and settings
Add your API keys here - they will be loaded by the backend
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys - Add your keys here or set in .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "your_openai_api_key_here")
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', "your_weather_api_key_here")
POWER_GRID_API_KEY = os.getenv('POWER_GRID_API_KEY', "your_power_grid_api_key_here")

# Database Configuration
DATABASE_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': os.getenv('MYSQL_PASSWORD', ''),  # Load from env or use empty
    'database': 'power_grid_db'
}

# API Endpoints
API_ENDPOINTS = {
    'openai': 'https://api.openai.com/v1/chat/completions',
    'weather': 'https://api.weatherapi.com/v1/current.json',
    'power_grid': 'https://api.powergrid.com/v1/data'
}

# Model Settings
MODEL_CONFIG = {
    'use_api_predictions': os.getenv('USE_API_PREDICTIONS', 'true').lower() == 'true',
    'fallback_to_mock': os.getenv('FALLBACK_TO_MOCK', 'true').lower() == 'true',
    'prediction_timeout': 30      # API timeout in seconds
}

# Security Settings
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "your_jwt_secret_key_here")
JWT_EXPIRATION_HOURS = 24

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [Trace: %(trace_id)s] - %(message)s"