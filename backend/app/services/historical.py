"""
Member 6 Historical Climate Service
Provides historical trends, monthly climate averages, and annual rainfall statistics.
"""
import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CHENNAI_DATA_FILE = DATA_DIR / "chennai_weather.json"


def get_historical_climate(city: str = "chennai") -> Dict[str, Any]:
    """
    Load historical climate data and monthly trends.
    """
    if not CHENNAI_DATA_FILE.exists():
        return {"error": "Historical data file missing"}

    try:
        with open(CHENNAI_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "city": city,
            "annual_rainfall_avg_mm": data.get("annual_rainfall_avg_mm", 1400),
            "monthly_trends": data.get("monthly", {}),
            "extreme_events": data.get("extreme_events", [])
        }
    except Exception as e:
        return {"error": str(e)}
