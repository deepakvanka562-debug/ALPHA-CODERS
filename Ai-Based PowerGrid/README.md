# AI-Powered Power Grid Failure & Delay Prediction Agent

This project provides a full-stack solution to predict power grid failures based on live/historical parameters.

## Prerequisites
- **Python 3.8+**
- **Node.js 18+** (Required for the Vite + React dev server)
- **MySQL Server** (Running on `localhost:3306`, user: `root`, no password by default)

## 1. Database Setup
1. Open your MySQL client or command line.
2. Execute the script located at `database/schema.sql` to generate the `power_grid_db` database and `predictions` table.

## 2. Backend Setup
1. Open a terminal and navigate to the project root: `cd "d:\Ai-Based PowerGrid"`
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Generate the ML Models (this synthesizes data and trains the AI):
   ```bash
   cd backend
   python model.py
   ```
5. Start the Flask API server:
   ```bash
   python app.py
   ```
   *The server will run at http://127.0.0.1:5000*

## 3. Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd "d:\Ai-Based PowerGrid\frontend"
   ```
2. Install Node modules:
   ```bash
   npm install
   ```
3. Start the Vite React app:
   ```bash
   npm run dev
   ```
   *The application will open in your browser, providing a modern, dynamic dashboard to input grid parameters.*

---
### Developer Notes
- The React frontend uses a sleek, premium Glassmorphism design and talks securely to the Python ML backend.
- The Python model is generated randomly for simulation but uses Random Forest Classifiers/Regressors to provide realistic variance in Delay/Probability.
