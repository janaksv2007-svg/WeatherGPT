import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "WeatherGPT Unified API Engine" in data["service"]


def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"message": "Will it rain in Chennai tomorrow?", "session_id": "test-1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "response" in data
    assert data["analysis"]["intent"] in ["RAIN_FORECAST", "DAILY_FORECAST", "CURRENT_WEATHER"]


def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={"message": "What is the temperature in Mumbai?", "session_id": "test-2"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data


def test_weather_api():
    response = client.get("/api/weather?location=chennai")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert "hourly" in data
    assert "daily" in data


def test_risk_api():
    response = client.post(
        "/api/risk",
        json={
            "temperature": 32.0,
            "humidity": 80.0,
            "rainfall_mm": 45.0,
            "wind_speed_kmh": 25.0,
            "condition": "Heavy Rain"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert data["risk_score"] > 0


def test_simulation_api():
    response = client.post(
        "/api/simulation",
        json={
            "target_rainfall_mm": 100.0,
            "additional_rainfall_hours": 3.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "baseline" in data
    assert "simulated" in data
    assert "risk_change" in data


def test_alerts_api():
    response = client.get("/api/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data


def test_climate_api():
    response = client.get("/api/climate?city=chennai")
    assert response.status_code == 200
    data = response.json()
    assert "annual_rainfall_avg_mm" in data


def test_anomalies_api():
    response = client.get("/api/anomalies?temp=38.0&rain=60.0")
    assert response.status_code == 200
    data = response.json()
    assert "is_anomaly" in data
    assert data["is_anomaly"] is True


def test_tamil_chatbot():
    response = client.post(
        "/chat",
        json={"message": "சென்னையில் இன்று மழை பெய்யுமா?", "session_id": "test-tamil", "language": "ta"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "response" in data
    assert data["analysis"]["language"] == "ta"


def test_simulation_chatbot():
    response = client.post(
        "/chat",
        json={"message": "What if rainfall increases to 100 mm in Chennai?", "session_id": "test-sim"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "simulation" in data
    assert data["simulation"]["simulated_risk"] > 0


def test_historical_climate_chatbot():
    response = client.post(
        "/chat",
        json={"message": "What are the historical climate trends for Chennai?", "session_id": "test-climate"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "climate" in data
    assert "annual_rainfall_avg_mm" in data["climate"]

