# Power Grid AI - API Key Setup

## 🚀 Quick Setup

Your system now supports **real API integrations** for predictions and data fetching!

## 🔑 API Key Configuration

### Step 1: Copy Environment Template
```bash
cp .env.example .env
```

### Step 2: Add Your API Keys

Edit the `.env` file and add your actual API keys:

```env
# OpenAI API Key (for AI-powered predictions)
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Weather API Key (for real climate data)
WEATHER_API_KEY=your-weather-api-key-here

# Power Grid API Key (for external grid data)
POWER_GRID_API_KEY=your-power-grid-api-key-here

# Database Password
MYSQL_PASSWORD=your_mysql_password

# Security
JWT_SECRET_KEY=your-secure-jwt-secret-here
```

## 📋 Supported APIs

### 1. **OpenAI API** (GPT-3.5/4)
- **Purpose:** AI-powered failure predictions
- **Get Key:** https://platform.openai.com/api-keys
- **Cost:** Pay-per-use
- **Features:** Intelligent risk assessment, recommendations

### 2. **Weather API** (WeatherAPI.com)
- **Purpose:** Real-time climate data for predictions
- **Get Key:** https://www.weatherapi.com/
- **Cost:** Free tier available
- **Features:** Temperature, humidity, wind speed

### 3. **Power Grid API** (Optional)
- **Purpose:** External grid monitoring data
- **Get Key:** Contact your grid operator
- **Features:** Real grid telemetry

## ⚙️ Configuration Options

### In `.env` file:
```env
# Enable/disable API predictions
USE_API_PREDICTIONS=true

# Fallback to mock data if API fails
FALLBACK_TO_MOCK=true
```

### In `config.py`:
- **API Endpoints:** Modify URLs if needed
- **Timeouts:** Adjust API call timeouts
- **Model Settings:** Configure prediction behavior

## 🔄 How It Works

1. **User submits prediction request**
2. **System tries OpenAI API first** (if key provided)
3. **Fetches weather data** (if weather key provided)
4. **Combines data for intelligent predictions**
5. **Falls back to mock data** (if APIs fail and fallback enabled)

## 📊 Enhanced Features

### With API Keys:
- ✅ **AI-powered predictions** using GPT
- ✅ **Real weather data** integration
- ✅ **Intelligent recommendations**
- ✅ **Climate-aware risk assessment**

### Without API Keys:
- ✅ **Smart mock predictions** (weather-influenced)
- ✅ **All features still work**

## 🧪 Testing

### Test API Integration:
```bash
# Check if APIs are working
python -c "from config import OPENAI_API_KEY; print('OpenAI Key:', 'Set' if OPENAI_API_KEY != 'your_openai_api_key_here' else 'Not Set')"
```

### Test Predictions:
1. Start servers: `python dashboard.py` & `python backend/app_simple.py`
2. Open: `http://127.0.0.1:8080`
3. Login and run predictions
4. Check terminal logs for API calls

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- **Use strong JWT secrets** in production
- **API keys have usage costs** - monitor usage
- **Rotate keys regularly** for security

## 📞 Support

If API integration fails:
1. Check API key validity
2. Verify internet connection
3. Check API rate limits
4. Review terminal error logs

---

**Status:** ✅ API Integration Ready
**Last Updated:** April 16, 2026