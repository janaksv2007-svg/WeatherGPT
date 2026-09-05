import json
from pathlib import Path
from typing import Optional, Dict, Any


BASE_DIR = Path(__file__).resolve().parents[2]
WEATHER_DATA_FILE = BASE_DIR / "data" / "sample_weather.json"


def load_weather_data() -> Dict[str, Any]:
    """Load sample weather data from JSON."""

    if not WEATHER_DATA_FILE.exists():
        print(f"[Weather] File not found: {WEATHER_DATA_FILE}")
        return {}

    try:
        with open(
            WEATHER_DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        print(f"[Weather] Invalid JSON: {error}")
        return {}

    except Exception as error:
        print(f"[Weather] File read error: {error}")
        return {}


def _get_value(obj, key, default=None):
    """Safely read from dict or Pydantic object."""

    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def get_weather(
    city: str,
    time_info=None,
    intent: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Temporary Weather API adapter.

    Member 2 can later replace this function with
    the real weather API implementation.

    Parameters:
        city:
            City name.

        time_info:
            Requested time information.

        intent:
            Weather intent such as CURRENT_WEATHER,
            RAIN_FORECAST, HOURLY_FORECAST, etc.
    """

    if not city:
        return None

    weather_data = load_weather_data()

    city_name = str(city).strip().lower()

    selected_weather = None

    for location, data in weather_data.items():

        if location.lower() == city_name:
            selected_weather = data.copy()
            break

    if selected_weather is None:

        print(
            f"[Weather] No sample data available "
            f"for: {city}"
        )

        return None

    # ---------------------------------------------------------
    # Add request metadata
    # ---------------------------------------------------------

    requested_date = _get_value(
        time_info,
        "date"
    )

    time_period = _get_value(
        time_info,
        "time_period"
    )

    exact_time = _get_value(
        time_info,
        "exact_time"
    )

    selected_weather["location"] = city
    selected_weather["requested_date"] = requested_date
    selected_weather["time_period"] = time_period
    selected_weather["exact_time"] = exact_time
    selected_weather["intent"] = intent

    # ---------------------------------------------------------
    # Identify forecast type
    # ---------------------------------------------------------

    if intent == "HOURLY_FORECAST":
        selected_weather["forecast_type"] = "hourly"

    elif intent == "DAILY_FORECAST":
        selected_weather["forecast_type"] = "daily"

    elif intent == "RAIN_FORECAST":
        selected_weather["forecast_type"] = "rain"

    elif intent == "TEMPERATURE":
        selected_weather["forecast_type"] = "temperature"

    elif intent == "WIND":
        selected_weather["forecast_type"] = "wind"

    elif intent == "HUMIDITY":
        selected_weather["forecast_type"] = "humidity"

    else:
        selected_weather["forecast_type"] = "current"

    print(
        f"[Weather] {city} | "
        f"intent={intent} | "
        f"date={requested_date} | "
        f"period={time_period}"
    )

    return selected_weather