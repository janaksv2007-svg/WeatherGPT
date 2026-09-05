"""
WeatherGPT — Unified FastAPI Backend Integration Entry Point
Connects all 6 Member Modules:
- Member 1: AI Chatbot, Intent Analysis, Gemini LLM & Conversation Memory
- Member 2: Live Weather Service (Open-Meteo current, hourly, daily, air quality)
- Member 3: Risk Engine (0-100 score) & Counterfactual What-If Scenario Simulator
- Member 4: Flutter Mobile & Web Client Integration Hub
- Member 5: Disaster Alerts (IMD/NDMA), RainViewer Live Radar, Lightning Tracking & WebSocket Notifier
- Member 6: Climate Trends, Historical Graphs, Anomaly Detection & Multilingual Support
"""
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Imports from app modules
from app.chat.chatbot import chat_response
from app.config import CHENNAI, PALLIKARANAI, BBOX
from app.services import rainviewer, imd_alerts, lightning, weather, news
from app import notifier
from app.services.risk_engine import calculate_risk
from app.services.simulation_engine import simulate_scenario
from app.services.anomaly import detect_anomalies
from app.services.historical import get_historical_climate
from app.services.multilingual import get_translations


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start WebSocket alert polling background task
    task = asyncio.create_task(notifier.poll_loop())
    yield
    task.cancel()


app = FastAPI(
    title="WeatherGPT Unified API Engine",
    description="Central API Server connecting AI Chatbot, Live Weather, Risk Engine, What-If Simulator, Alerts & Climate Insights",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for Flutter Mobile/Web and React Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------- SCHEMAS ---
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    language: str = "en"


class RiskRequest(BaseModel):
    temperature: float = 28.0
    humidity: float = 70.0
    rainfall_mm: float = 0.0
    rain_probability: float = 0.0
    wind_speed_kmh: float = 10.0
    condition: str = "Clear"
    lightning_count: int = 0


class ScenarioRequest(BaseModel):
    baseline_weather: Optional[Dict[str, Any]] = None
    target_rainfall_mm: Optional[float] = None
    rainfall_change_mm: Optional[float] = None
    rainfall_change_percent: Optional[float] = None
    wind_speed_change_percent: Optional[float] = None
    additional_rainfall_hours: Optional[float] = None
    temperature_change_celsius: Optional[float] = None


# ------------------------------------------------------------- HEALTH ---
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "WeatherGPT Unified API Engine",
        "version": "2.0.0",
        "modules_connected": ["Member 1 AI", "Member 2 Weather", "Member 3 Risk", "Member 4 Flutter", "Member 5 Alerts/Radar", "Member 6 Climate"]
    }


# --------------------------------------------------- MEMBER 1: CHATBOT ---
@app.post("/chat")
def chat(request: ChatRequest):
    """Unified natural language chatbot endpoint."""
    raw_result = chat_response(
        message=request.message,
        session_id=request.session_id,
        language=request.language,
    )
    
    # Enrich with Risk & Alert information according to Golden Rule
    analysis = raw_result.get("analysis", {})
    weather_data = raw_result.get("weather_data")
    
    risk_info = None
    if weather_data and isinstance(weather_data, dict):
        risk_info = calculate_risk(
            temperature=weather_data.get("temperature", 28.0),
            humidity=weather_data.get("humidity", 70.0),
            rainfall_mm=weather_data.get("rainfall_mm", 0.0),
            wind_speed_kmh=weather_data.get("wind_speed_kmh", 10.0),
            condition=weather_data.get("condition", "Clear")
        )

    climate_info = raw_result.get("climate")
    sim_info = raw_result.get("simulation_data")
    if not risk_info:
        risk_info = raw_result.get("risk")

    return {
        "success": True,
        "session_id": request.session_id,
        "user_message": request.message,
        "analysis": analysis,
        "weather": weather_data,
        "risk": risk_info,
        "simulation": sim_info,
        "climate": climate_info,
        "alerts": [],
        "response": raw_result.get("response", "")
    }



@app.post("/analyze")
def analyze(request: ChatRequest):
    """AI analysis endpoint returning intent, location, time, and language metadata."""
    result = chat_response(
        message=request.message,
        session_id=request.session_id,
        language=request.language,
    )
    return {
        "session_id": request.session_id,
        "message": request.message,
        "analysis": result.get("analysis"),
    }


# --------------------------------------------------- MEMBER 2: WEATHER ---
@app.get("/api/weather")
async def current_weather(location: str = Query("chennai")):
    """Live weather forecast from Open-Meteo (current, hourly, daily, air quality)."""
    return await weather.get_weather(location)


@app.get("/api/locations")
async def locations():
    return {"chennai": CHENNAI, "pallikaranai": PALLIKARANAI, "bbox": BBOX}


# ----------------------------------------------- MEMBER 3: RISK & SIM ---
@app.post("/api/risk")
def compute_risk(req: RiskRequest):
    """Calculate 0-100 risk score and hazard factor breakdown."""
    return calculate_risk(
        temperature=req.temperature,
        humidity=req.humidity,
        rainfall_mm=req.rainfall_mm,
        rain_probability=req.rain_probability,
        wind_speed_kmh=req.wind_speed_kmh,
        condition=req.condition,
        lightning_count=req.lightning_count
    )


@app.post("/api/simulation")
def run_simulation(req: ScenarioRequest):
    """Run counterfactual what-if scenario simulation."""
    baseline = req.baseline_weather or {
        "temperature": 28.0,
        "rainfall_mm": 10.0,
        "wind_speed_kmh": 15.0,
        "humidity": 70.0,
        "condition": "Cloudy"
    }

    scenario = {
        "target_rainfall_mm": req.target_rainfall_mm,
        "rainfall_change_mm": req.rainfall_change_mm,
        "rainfall_change_percent": req.rainfall_change_percent,
        "wind_speed_change_percent": req.wind_speed_change_percent,
        "additional_rainfall_hours": req.additional_rainfall_hours,
        "temperature_change_celsius": req.temperature_change_celsius
    }

    return simulate_scenario(baseline_weather=baseline, scenario=scenario)


# ------------------------------------------------- MEMBER 5: ALERTS/MAP ---
@app.get("/api/alerts")
async def disaster_alerts():
    """Live IMD disaster alerts & warnings (NDMA Sachet)."""
    return {"alerts": await imd_alerts.get_alerts()}


@app.get("/api/radar/rainviewer")
async def rainviewer_frames():
    """Live RainViewer radar frame timestamps and map tiles."""
    return await rainviewer.get_frames()


@app.get("/api/lightning")
async def lightning_strikes():
    """Live lightning strikes tracking."""
    return await lightning.get_strikes()


@app.get("/api/news")
async def weather_news():
    """Weather news feed."""
    return await news.get_news()


@app.websocket("/ws/alerts")
async def ws_alerts(ws: WebSocket):
    await notifier.manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        notifier.manager.disconnect(ws)


# ----------------------------------------------- MEMBER 6: CLIMATE/LANG ---
@app.get("/api/climate")
def climate_data(city: str = Query("chennai")):
    """Historical climate trends and statistics."""
    return get_historical_climate(city)


@app.get("/api/anomalies")
def anomaly_data(temp: float = Query(31.0), rain: float = Query(0.0)):
    """Climate anomaly detection analysis."""
    return detect_anomalies(current_temp=temp, current_rain=rain)


@app.get("/api/translations")
def translations(language: str = Query("english")):
    """Multilingual terms translation."""
    return get_translations(language)


# ----------------------------------------------------- STATIC FRONTEND ---
from pathlib import Path
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend_web"
STATIC_DIR = FRONTEND_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "WeatherGPT Unified API Engine Running"}