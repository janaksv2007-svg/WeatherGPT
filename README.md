# WeatherGPT — Unified AI Weather Engine, Risk Engine & Chatbot Stack

An intelligent, multi-module weather intelligence platform connecting:
- **Member 1**: AI Chatbot with Local Intent Detector & Google Gemini LLM (`gemini-3.6-flash`).
- **Member 2**: Live Weather Service (Open-Meteo API for current, hourly, daily, air quality).
- **Member 3**: Risk Engine (0-100 score) & What-If Counterfactual Scenario Simulator.
- **Member 4**: Flutter Mobile & Web Client App (`mobile_flutter/`).
- **Member 5**: IMD/NDMA Disaster Warnings, RainViewer Live Radar, Lightning Tracking & WebSocket Notifier.
- **Member 6**: Climate Trends, Historical Data, Anomaly Detection & Multilingual Support.

---

## 🚀 How to Run WeatherGPT

### Option A: 1-Click Starter (Recommended)

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn[standard] httpx websockets google-generativeai pydantic python-dotenv pytest
   ```

2. **Start the Unified Server**:
   ```bash
   python start_server.py
   ```

3. **Access Applications**:
   - 🌐 **Web Dashboard & AI Chatbot**: Open [http://localhost:8000](http://localhost:8000)
   - 📚 **Swagger API Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs)
   - 📱 **Flutter Mobile App**: Connects to `http://127.0.0.1:8000`

---

### Option B: Running from GitHub

```bash
# 1. Clone the repository
git clone https://github.com/janaksv2007-svg/WeatherGPT.git
cd WeatherGPT

# 2. Install dependencies
pip install fastapi uvicorn[standard] httpx websockets google-generativeai pydantic python-dotenv pytest

# 3. Launch server
python start_server.py
```

---

### Option C: Running the Flutter Mobile App

```bash
cd mobile_flutter
flutter pub get
flutter run
```

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
python -m pytest tests/test_api_all.py -v
```

---

## 📂 Project Architecture

```
WeatherGPT/
├── backend/                  # Unified FastAPI Engine
│   └── app/
│       ├── ai/               # Gemini LLM Integration & Prompts
│       ├── chat/             # Chatbot Controller & Memory
│       ├── intent/           # Member 1 Local Intent Detector
│       ├── services/         # Member 3 Risk & Simulation, Member 6 Climate
│       └── main.py           # Unified API Server Endpoint Registry
├── frontend_web/             # Web App Dashboard & AI Chatbot UI (Dark Theme)
│   ├── index.html
│   └── static/               # app.js & style.css
├── mobile_flutter/           # Member 4 Flutter Mobile App
├── tests/                    # Pytest Suite (9/9 passed)
├── start_server.py           # 1-Click Root Server Launcher
└── README.md
```
