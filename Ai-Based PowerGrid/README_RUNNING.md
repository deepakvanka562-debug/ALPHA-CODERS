# Power Grid AI - Running System

## Quick Start

Your AI-powered Power Grid monitoring system is now **fully operational**!

### 🚀 Access Points

| Service | URL | Status |
|---------|-----|--------|
| **Dashboard** | http://127.0.0.1:8080 | ✅ Running |
| **Backend API** | http://127.0.0.1:5000 | ✅ Running |
| **API Health** | http://127.0.0.1:5000/health | ✅ OK |
| **Database** | localhost:3306 | ✅ Running |

### 👤 Login Credentials

- **Username:** `admin`
- **Password:** `password`

### 🎯 Features

✅ **User Authentication** - JWT-based secure login  
✅ **Real-time Predictions** - AI-based power grid failure prediction  
✅ **Risk Assessment** - LOW/MEDIUM/HIGH risk levels  
✅ **Delay Estimation** - Expected downtime predictions  
✅ **Async Processing** - Background job queue system  
✅ **Responsive Dashboard** - Modern, beautiful UI  

### 📊 Example Prediction Parameters

- **Zone Name:** Zone-A
- **Voltage:** 230 kV
- **Load:** 150 MW
- **Temperature:** 35°C

**Prediction Results:**
- Failure Probability: 40.0%
- Risk Level: LOW
- Expected Delay: 33.4 hours

### 🛠️ Technical Stack

**Backend:**
- Framework: Flask (Python)
- Authentication: JWT tokens
- Database: MySQL
- Job Queue: In-memory threading

**Frontend:**
- UI: Modern responsive HTML5/CSS3/JavaScript
- API Client: Fetch API
- Status: Real-time updates

### 📂 Project Files

```
d:\Ai-Based PowerGrid\
├── backend/
│   ├── app_simple.py        ← API Server (port 5000)
│   ├── auth.py              ← Authentication module
│   ├── model.py             ← ML models
│   ├── utils.py             ← Utility functions
│   └── requirements.txt      ← Python dependencies
├── frontend/
│   └── simple_dashboard.html ← Dashboard UI
├── dashboard.py             ← Dashboard Server (port 8080)
├── run_dashboard.py         ← Dashboard runner
└── .vscode/
    └── launch.json          ← Debug configuration
```

### 🔌 Running the System

The system is currently running in two terminals:

**Terminal 1 - Dashboard Server:**
```
python dashboard.py
```

**Terminal 2 - Backend API Server:**
```
python backend/app_simple.py
```

### 🧪 Testing the API

```bash
# Health check
curl http://127.0.0.1:5000/health

# Login
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Make prediction (requires token)
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"zone_name":"Zone-A","voltage":230,"load":150,"temperature":35}'
```

### ⚙️ Configuration

- **Dashboard Port:** 8080
- **API Port:** 5000
- **Database Host:** 127.0.0.1
- **Database Port:** 3306
- **Database Name:** power_grid_db

### 📝 Notes

- No Redis or Node.js required - system runs with Python only
- JWT tokens expire after standard session time
- Predictions are processed asynchronously in background threads
- All data is logged with trace IDs for debugging
- Dashboard auto-refreshes prediction status

### 🔧 Troubleshooting

**Dashboard not opening?**  
→ Try: `http://127.0.0.1:8080` instead of `localhost:8080`

**API not responding?**  
→ Check if port 5000 is in use: `netstat -ano | findstr :5000`

**Prediction hanging?**  
→ Backend processes requests asynchronously - click "Check Status" to see results

**Database connection error?**  
→ Ensure MySQL is running: `mysqld` or use services

---

**Last Updated:** April 16, 2026  
**Status:** ✅ All Systems Operational
