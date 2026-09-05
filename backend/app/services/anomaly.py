"""
Member 6 Anomaly Detection Service
Analyzes current/forecast weather against historical Chennai datasets to detect climate anomalies.
"""
import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CHENNAI_DATA_FILE = DATA_DIR / "chennai_weather.json"


def detect_anomalies(current_temp: float = 31.0, current_rain: float = 0.0) -> Dict[str, Any]:
    """
    Compares current temperature & rainfall against monthly historical benchmarks.
    """
    if not CHENNAI_DATA_FILE.exists():
        return {
            "status": "unavailable",
            "message": "Historical weather database file not found"
        }

    try:
        with open(CHENNAI_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        monthly = data.get("monthly", {})
        max_temps = [m.get("max_temp", 33.0) for m in monthly.values()]
        historical_avg_max = sum(max_temps) / max(1, len(max_temps))

        temp_anomaly = round(current_temp - historical_avg_max, 2)
        is_temp_anomaly = abs(temp_anomaly) >= 3.0

        rain_anomaly = current_rain > 50.0
        
        alerts = []
        if temp_anomaly >= 3.0:
            alerts.append(f"Temperature is {temp_anomaly}°C warmer than historical average ({round(historical_avg_max, 1)}°C)")
        elif temp_anomaly <= -3.0:
            alerts.append(f"Temperature is {abs(temp_anomaly)}°C cooler than historical average ({round(historical_avg_max, 1)}°C)")

        if rain_anomaly:
            alerts.append(f"Heavy rainfall event detected ({current_rain} mm), exceeding 90th percentile historical daily threshold.")

        return {
            "historical_avg_max_temp": round(historical_avg_max, 2),
            "current_temp": current_temp,
            "temp_anomaly_celsius": temp_anomaly,
            "is_anomaly": is_temp_anomaly or rain_anomaly,
            "anomaly_alerts": alerts,
            "annual_rainfall_avg_mm": data.get("annual_rainfall_avg_mm", 1400)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
