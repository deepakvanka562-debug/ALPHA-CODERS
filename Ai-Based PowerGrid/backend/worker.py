import os
import random
from rq import Worker, Queue, Connection
from redis import Redis
import time
import logging

# Simple Python logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
logger = logging.getLogger("worker")

redis_conn = Redis(host='127.0.0.1', port=6379)

def perform_prediction(features, trace_id, context):
    """Async job processing the ML prediction."""
    logger.info(f"[Trace: {trace_id}] Worker received job with context: {context}")
    
    # Simulate intensive ML computation
    time.sleep(2)
    
    load, temp, weather, health, maintenance_delay = features
    
    # Calculate mock risk
    risk_score = (load * 0.4) + (temp * 0.1) + (weather * 15) + (health * 20) + (maintenance_delay * 10)
    prob_pred = max(0, min(100, risk_score / 150 * 100))
    
    # Calculate mock delay
    delay_pred = (prob_pred * 0.1) + (weather * 2) + (health * 3) + random.uniform(0, 2)
    delay_pred = max(0, min(48, delay_pred))
    
    result = {
        "prob_pred": prob_pred,
        "delay_pred": delay_pred,
        "zone_name": context.get("zone_name", "Unknown")
    }
    
    logger.info(f"[Trace: {trace_id}] Worker completed job with result: {result}")
    return result

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(['default'])
        logger.info("Initializing background worker. Waiting for tasks on the 'default' queue...")
        worker.work()
