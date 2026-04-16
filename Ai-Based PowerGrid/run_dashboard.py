"""
Simple web server to serve the dashboard HTML
Run with: python run_dashboard.py
Then open: http://localhost:8080
"""

from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def index():
    # Serve the simple dashboard HTML
    return send_from_directory('frontend', 'simple_dashboard.html')

@app.route('/health')
def health():
    return {'status': 'running'}, 200

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════╗
    ║  Power Grid AI - Simple Dashboard      ║
    ║  Opening http://localhost:8080         ║
    ║  Backend: http://localhost:5000        ║
    ║                                        ║
    ║  Login with: admin / password          ║
    ╚════════════════════════════════════════╝
    """)
    app.run(debug=False, port=8080, host="0.0.0.0", use_reloader=False)
