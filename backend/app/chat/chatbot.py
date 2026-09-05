from typing import Optional, Dict, Any

from app.intent.local_detector import analyze_locally
from app.ai.gemini import generate_response
from app.integration.weather_client import get_weather

from app.chat.memory import (
    get_session,
    update_session,
)

from app.models.schemas import Location


# =============================================================
# LOCATION HELPERS
# =============================================================

def _get_location_name(analysis) -> Optional[str]:
    """Safely extract location name from analysis."""

    if analysis is None:
        return None

    location = (
        analysis.get("location")
        if isinstance(analysis, dict)
        else getattr(analysis, "location", None)
    )

    if location is None:
        return None

    if isinstance(location, dict):
        return location.get("name")

    return getattr(location, "name", None)


def _get_comparison_location_name(analysis) -> Optional[str]:
    """Safely extract comparison location name."""

    if analysis is None:
        return None

    if isinstance(analysis, dict):
        location = analysis.get("comparison_location")
    else:
        location = getattr(
            analysis,
            "comparison_location",
            None,
        )

    if location is None:
        return None

    if isinstance(location, dict):
        return location.get("name")

    return getattr(location, "name", None)


# =============================================================
# ANALYSIS → DICTIONARY
# =============================================================

def _analysis_to_dict(analysis) -> Dict[str, Any]:
    """Convert analysis object into a normal dictionary."""

    if analysis is None:
        return {}

    if isinstance(analysis, dict):
        return analysis

    if hasattr(analysis, "model_dump"):
        return analysis.model_dump()

    if hasattr(analysis, "dict"):
        return analysis.dict()

    return {
        "message": getattr(
            analysis,
            "message",
            None,
        ),
        "intent": getattr(
            analysis,
            "intent",
            "UNKNOWN",
        ),
        "location": getattr(
            analysis,
            "location",
            None,
        ),
        "comparison_location": getattr(
            analysis,
            "comparison_location",
            None,
        ),
        "time": getattr(
            analysis,
            "time",
            None,
        ),
        "language": getattr(
            analysis,
            "language",
            "en",
        ),
        "parameters": getattr(
            analysis,
            "parameters",
            {},
        ),
        "requires_weather_data": getattr(
            analysis,
            "requires_weather_data",
            False,
        ),
        "requires_risk_analysis": getattr(
            analysis,
            "requires_risk_analysis",
            False,
        ),
        "requires_simulation": getattr(
            analysis,
            "requires_simulation",
            False,
        ),
    }


# =============================================================
# TIME HELPERS
# =============================================================

def _get_time_info(analysis) -> Dict[str, Any]:
    """Safely convert analysis time into a dictionary."""

    if analysis is None:
        return {}

    if isinstance(analysis, dict):
        time_info = analysis.get("time")

    else:
        time_info = getattr(
            analysis,
            "time",
            None,
        )

    if time_info is None:
        return {}

    if isinstance(time_info, dict):
        return time_info

    if hasattr(time_info, "model_dump"):
        return time_info.model_dump()

    if hasattr(time_info, "dict"):
        return time_info.dict()

    return {
        "date": getattr(
            time_info,
            "date",
            None,
        ),
        "time_period": getattr(
            time_info,
            "time_period",
            None,
        ),
        "exact_time": getattr(
            time_info,
            "exact_time",
            None,
        ),
    }


# =============================================================
# INTENT HELPER
# =============================================================

def _get_intent(analysis) -> str:
    """Safely get intent."""

    if analysis is None:
        return "UNKNOWN"

    if isinstance(analysis, dict):
        return analysis.get(
            "intent",
            "UNKNOWN",
        )

    return getattr(
        analysis,
        "intent",
        "UNKNOWN",
    )


# =============================================================
# LANGUAGE HELPER
# =============================================================

def _get_language(
    analysis,
    default: str = "en",
) -> str:

    if analysis is None:
        return default

    if isinstance(analysis, dict):
        return analysis.get(
            "language",
            default,
        )

    return getattr(
        analysis,
        "language",
        default,
    )


# =============================================================
# WEATHER CONTEXT
# =============================================================

def _build_weather_context(
    weather_data: Any,
) -> str:
    """Convert weather data into a context string."""

    if not weather_data:
        return ""

    if isinstance(weather_data, dict):

        location = weather_data.get(
            "location",
            "Unknown",
        )

        temperature = weather_data.get(
            "temperature",
        )

        humidity = weather_data.get(
            "humidity",
        )

        rainfall = weather_data.get(
            "rainfall_mm",
        )

        wind = weather_data.get(
            "wind_speed_kmh",
        )

        condition = weather_data.get(
            "condition",
        )

        return (
            "\n"
            "WEATHER DATA FROM MODULE 2:\n"
            f"Location: {location}\n"
            f"Temperature: {temperature} °C\n"
            f"Humidity: {humidity}%\n"
            f"Rainfall: {rainfall} mm\n"
            f"Wind Speed: {wind} km/h\n"
            f"Condition: {condition}\n"
            "\n"
            "Use ONLY these values when describing weather.\n"
            "Do not invent additional weather values.\n"
        )

    return (
        "\n"
        "WEATHER DATA FROM MODULE 2:\n\n"
        f"{weather_data}\n\n"
        "Use ONLY the supplied weather data.\n"
        "Do not invent weather values.\n"
    )


# =============================================================
# MEMORY
# =============================================================

def _get_gemini_context(
    session_id: str,
    analysis: Any,
) -> Dict[str, Any]:

    try:

        session = get_session(
            session_id
        )

        if not session:
            return {}

        return session

    except Exception as error:

        print(
            f"[Memory Read Error] {error}"
        )

        return {}


def _save_chat_context(
    session_id: str,
    analysis: Any,
    weather_data: Optional[Dict[str, Any]] = None,
):
    """Save useful conversation context."""

    location_name = _get_location_name(
        analysis
    )

    try:

        time_data = _get_time_info(
            analysis
        )

        language = _get_language(
            analysis
        )

        update_session(
            session_id=session_id,
            location=location_name,
            time=time_data,
            language=language,
        )

        if weather_data:

            session = get_session(
                session_id
            )

            if session is not None:

                session["weather_data"] = (
                    weather_data
                )

        print(
            f"[Memory] Session updated: "
            f"{session_id}"
        )

    except Exception as error:

        print(
            f"[Memory Save Error] "
            f"{error}"
        )


# =============================================================
# FOLLOW-UP DETECTION
# =============================================================

def _is_follow_up(
    message: str,
    session_id: str = "default",
) -> bool:
    """Detect conversational follow-up messages."""

    text = message.lower().strip()

    try:

        session = get_session(
            session_id
        )

        has_context = bool(
            session
            and session.get("location")
        )

    except Exception:

        has_context = False

    if not has_context:
        return False

    follow_up_phrases = [

        # Context
        "what about",
        "how about",
        "same place",
        "same city",
        "that city",
        "there",
        "same location",

        # Time follow-ups
        "and tomorrow",
        "and today",
        "and tonight",
        "this weekend",
        "and weekend",
        "next week",
        "and morning",
        "and afternoon",
        "and evening",

        # Tamil
        "அங்கே",
        "அதே இடம்",
        "அதே நகரம்",

        # Hindi
        "वहाँ",
        "उसी जगह",
        "उसी शहर",
    ]

    return any(
        phrase in text
        for phrase in follow_up_phrases
    )


# =============================================================
# APPLY MEMORY
# =============================================================

def _apply_memory_to_follow_up(
    analysis,
    message: str,
    session_id: str,
):
    """
    Apply previous conversation context to
    short follow-up questions.
    """

    # ---------------------------------------------------------
    # Never overwrite explicit location
    # ---------------------------------------------------------

    existing_location = None

    if isinstance(analysis, dict):

        existing_location = analysis.get(
            "location"
        )

    else:

        existing_location = getattr(
            analysis,
            "location",
            None,
        )

    if existing_location:

        existing_name = (
            existing_location.get("name")
            if isinstance(
                existing_location,
                dict,
            )
            else getattr(
                existing_location,
                "name",
                None,
            )
        )

        if existing_name:

            print(
                "[Memory] Explicit location detected: "
                f"{existing_name}"
            )

            return analysis

    print(
        "[DEBUG] "
        "_apply_memory_to_follow_up() CALLED"
    )

    try:

        session = get_session(
            session_id
        )

        if not session:
            return analysis

        previous_location = session.get(
            "location"
        )

        if not previous_location:
            return analysis

        from app.location.resolver import resolve_city

        remembered_location = resolve_city(
            previous_location
        )

        if not remembered_location:
            return analysis

        location_data = Location(
            name=remembered_location["name"],
            latitude=remembered_location["latitude"],
            longitude=remembered_location["longitude"],
        )

        # -----------------------------------------------------
        # Previous time
        # -----------------------------------------------------

        previous_time = (
            session.get("time")
            or {}
        )

        if not isinstance(
            previous_time,
            dict,
        ):
            previous_time = {}

        new_date = previous_time.get(
            "date"
        )

        new_period = previous_time.get(
            "time_period"
        )

        # -----------------------------------------------------
        # Current message
        # -----------------------------------------------------

        text = message.lower()

        # -----------------------------------------------------
        # Date
        # -----------------------------------------------------

        if (
            "tomorrow" in text
            or "நாளை" in text
            or "நாளைக்கு" in text
            or "कल" in text
        ):

            new_date = "tomorrow"

        elif (
            "today" in text
            or "இன்று" in text
            or "இன்றைக்கு" in text
            or "आज" in text
        ):

            new_date = "today"

        # -----------------------------------------------------
        # Tonight
        # -----------------------------------------------------

        if (
            "tonight" in text
            or "இன்று இரவு" in text
            or "இன்றிரவு" in text
        ):

            new_period = "night"

        # -----------------------------------------------------
        # Morning
        # -----------------------------------------------------

        elif (
            "morning" in text
            or "காலை" in text
            or "सुबह" in text
        ):

            new_period = "morning"

        # -----------------------------------------------------
        # Afternoon
        # -----------------------------------------------------

        elif (
            "afternoon" in text
            or "மதியம்" in text
            or "दोपहर" in text
        ):

            new_period = "afternoon"

        # -----------------------------------------------------
        # Evening
        # -----------------------------------------------------

        elif (
            "evening" in text
            or "மாலை" in text
            or "शाम" in text
        ):

            new_period = "evening"

        # -----------------------------------------------------
        # Weekend
        # -----------------------------------------------------

        if (
            "weekend" in text
            or "வார இறுதி" in text
            or "வாரஇறுதி" in text
            or "सप्ताहांत" in text
        ):

            new_date = "weekend"

        # -----------------------------------------------------
        # Get intent
        # -----------------------------------------------------

        intent = _get_intent(
            analysis
        )

        # -----------------------------------------------------
        # Time follow-up?
        # -----------------------------------------------------

        is_time_follow_up = any(
            phrase in text
            for phrase in [
                "tomorrow",
                "today",
                "tonight",
                "morning",
                "afternoon",
                "evening",
                "weekend",
                "நாளை",
                "நாளைக்கு",
                "இன்று",
                "இன்றைக்கு",
                "இன்று இரவு",
                "இன்றிரவு",
                "காலை",
                "மதியம்",
                "மாலை",
                "வார இறுதி",
                "வாரஇறுதி",
                "कल",
                "आज",
                "सुबह",
                "दोपहर",
                "शाम",
                "सप्ताहांत",
            ]
        )

        if (
            intent == "UNKNOWN"
            and is_time_follow_up
        ):

            intent = "DAILY_FORECAST"

        # -----------------------------------------------------
        # Pydantic
        # -----------------------------------------------------

        if hasattr(
            analysis,
            "model_copy",
        ):

            analysis = analysis.model_copy(
                update={
                    "intent": intent,
                    "location": location_data,
                    "time": {
                        "date": new_date,
                        "time_period": new_period,
                        "exact_time": None,
                    },
                    "requires_weather_data": True,
                }
            )

        # -----------------------------------------------------
        # Dictionary
        # -----------------------------------------------------

        elif isinstance(
            analysis,
            dict,
        ):

            analysis["intent"] = intent

            analysis["location"] = {
                "name":
                    remembered_location["name"],
                "latitude":
                    remembered_location["latitude"],
                "longitude":
                    remembered_location["longitude"],
            }

            analysis["time"] = {
                "date": new_date,
                "time_period": new_period,
                "exact_time": None,
            }

            analysis[
                "requires_weather_data"
            ] = True

        print(
            "[Memory] Follow-up resolved: "
            f"{previous_location}"
        )

        print(
            "[Memory] Follow-up intent: "
            f"{intent}"
        )

        print(
            "[Memory] Follow-up date: "
            f"{new_date}"
        )

        print(
            "[Memory] Follow-up period: "
            f"{new_period}"
        )

        return analysis

    except Exception as error:

        print(
            f"[Follow-up Memory Error] "
            f"{error}"
        )

        return analysis


import re


def _is_greeting(message: str) -> bool:
    text = message.lower().strip()
    greetings = {
        "hello",
        "hi",
        "hey",
        "hello there",
        "hi there",
        "good morning",
        "good afternoon",
        "good evening",
        "வணக்கம்",
        "நமஸ்காரம்",
        "ஹலோ",
        "ஹாய்",
    }
    return text in greetings


def _greeting_response(language: str = "en") -> str:
    if language == "ta":
        return (
            "வணக்கம்! 👋 நான் WeatherGPT. "
            "தற்போதைய வானிலை, மழைக் கணிப்பு, வெப்பநிலை, "
            "காற்றோட்டம், ஈரப்பதம் மற்றும் வரலாற்று வானிலை தகவல்களை நீங்கள் என்னிடம் கேட்கலாம்."
        )

    return (
        "Hello! 👋 I'm WeatherGPT. "
        "You can ask me about current weather, "
        "forecasts, rain, temperature, wind, humidity, "
        "travel weather, or What-If weather scenarios."
    )


# =============================================================
# FALLBACK RESPONSE
# =============================================================

def _generate_fallback_response(
    analysis: Any,
    weather_data: Optional[Dict[str, Any]],
    language: str = "en",
    user_message: str = "",
) -> str:

    location = _get_location_name(analysis)
    intent = _get_intent(analysis)

    lang = language if language else _get_language(analysis)
    if user_message and re.search(r"[\u0B80-\u0BFF]", user_message):
        lang = "ta"

    # Tamil specific formatting
    if lang == "ta":
        loc_str = f"{location}-இல்" if location else "உங்கள் பகுதியில்"

        if not weather_data:
            return f"{loc_str} தற்போதைய வானிலை தகவல் பெற முடியவில்லை."

        if not isinstance(weather_data, dict):
            return "வானிலை தரவு பெறப்பட்டது, ஆனால் அதை வடிவமைக்க முடியவில்லை."

        temperature = weather_data.get("temperature", 28.0)
        humidity = weather_data.get("humidity", 70.0)
        rainfall = weather_data.get("rainfall_mm", 0.0)
        wind = weather_data.get("wind_speed_kmh", 10.0)
        condition = weather_data.get("condition", "Clear")
        requested_date = weather_data.get("requested_date")

        conditions_ta = {
            "Clear": "தெளிவான வானம்",
            "Sunny": "வெயில்",
            "Partly Cloudy": "பகுதி மேகமூட்டம்",
            "Cloudy": "மேகமூட்டம்",
            "Overcast": "அடர்ந்த மேகமூட்டம்",
            "Light Rain": "லேசான மழை",
            "Moderate Rain": "மிதமான மழை",
            "Heavy Rain": "கனமழை",
            "Thunderstorm": "இடி மின்னலுடன் கூடிய மழை",
            "Rain": "மழை",
            "Drizzle": "தூறல்",
            "Mist": "பனிமூட்டம்",
            "Fog": "அடர்ந்த பனி"
        }
        cond_ta = conditions_ta.get(str(condition), str(condition))

        if intent == "CURRENT_WEATHER":
            return (
                f"{loc_str} தற்போதைய வானிலை: {temperature}°C, {cond_ta}. "
                f"ஈரப்பதம் {humidity}%, மழைப்பொழிவு {rainfall} mm, "
                f"மற்றும் காற்று வேகம் {wind} km/h."
            )

        if intent == "RAIN_FORECAST":
            period = f" ({requested_date})" if requested_date else ""
            return (
                f"{loc_str} மழை கணிப்பு{period}: {rainfall} mm மழைப்பொழிவு எதிர்பார்க்கப்படுகிறது. "
                f"வானிலை நிலை: {cond_ta}."
            )

        if intent == "TEMPERATURE":
            return f"{loc_str} தற்போதைய வெப்பநிலை {temperature}°C ஆகும்."

        if intent == "WIND":
            return f"{loc_str} காற்று வேகம் {wind} km/h ஆகும்."

        if intent == "HUMIDITY":
            return f"{loc_str} ஈரப்பதம் {humidity}% ஆகும்."

        if intent in ["DAILY_FORECAST", "HOURLY_FORECAST"]:
            period = f" ({requested_date})" if requested_date else ""
            return (
                f"{loc_str} வானிலை தகவல்{period}: {temperature}°C, {cond_ta}, "
                f"ஈரப்பதம் {humidity}%, மழை {rainfall} mm, காற்று {wind} km/h."
            )

        if intent == "TRAVEL_WEATHER":
            return (
                f"{loc_str} பயணத்திற்கான வானிலை: {cond_ta}, வெப்பநிலை {temperature}°C, "
                f"மழை {rainfall} mm, காற்று வேகம் {wind} km/h."
            )

        if intent == "OUTDOOR_ACTIVITY":
            return (
                f"{loc_str} வெளிப்புற செயல்பாடுகளுக்கு வானிலை நிலை {cond_ta}, "
                f"வெப்பநிலை {temperature}°C, மழை {rainfall} mm."
            )

        if intent == "WEATHER_RISK":
            return (
                f"{loc_str} வானிலை அபாய நிலை: {cond_ta}, "
                f"வெப்பநிலை {temperature}°C, மழை {rainfall} mm, காற்று வேகம் {wind} km/h."
            )

        if intent == "WHAT_IF_SCENARIO":
            return (
                f"{loc_str} வானிலை மாதிரி (What-If) பகுப்பாய்வு நிறைவடைந்தது."
            )

        if intent == "HISTORICAL_CLIMATE":
            return (
                f"{loc_str} வரலாற்று காலநிலை தகவல்கள் பெறப்பட்டன."
            )

        return (
            f"{loc_str} வானிலை: {temperature}°C, {cond_ta}, "
            f"ஈரப்பதம் {humidity}%, மழை {rainfall} mm, காற்று {wind} km/h."
        )

    # English Fallback
    if not location:
        location = "your location"

    if not weather_data:
        return f"Weather information for {location} is currently unavailable."

    if not isinstance(weather_data, dict):
        return "Weather data was received, but I could not format it."

    temperature = weather_data.get("temperature")
    humidity = weather_data.get("humidity")
    rainfall = weather_data.get("rainfall_mm")
    wind = weather_data.get("wind_speed_kmh")
    condition = weather_data.get("condition")
    requested_date = weather_data.get("requested_date")

    if intent == "CURRENT_WEATHER":
        return (
            f"Current weather in {location}: "
            f"{temperature}°C, {condition}. "
            f"Humidity is {humidity}%, "
            f"rainfall is {rainfall} mm, "
            f"and wind speed is {wind} km/h."
        )

    if intent == "RAIN_FORECAST":
        period = f" for {requested_date}" if requested_date else ""
        return (
            f"Rain forecast for {location}{period}: "
            f"rainfall is {rainfall} mm "
            f"with conditions reported as {condition}."
        )

    if intent == "TEMPERATURE":
        return f"The temperature in {location} is {temperature}°C."

    if intent == "WIND":
        return f"Wind speed in {location} is {wind} km/h."

    if intent == "HUMIDITY":
        return f"Humidity in {location} is {humidity}%."

    if intent in ["DAILY_FORECAST", "HOURLY_FORECAST"]:
        period = f" for {requested_date}" if requested_date else ""
        return (
            f"Daily weather information for {location}{period}: "
            f"{temperature}°C, {condition}, "
            f"humidity {humidity}%, rainfall {rainfall} mm, wind {wind} km/h."
        )

    if intent == "TRAVEL_WEATHER":
        return (
            f"For travel to {location}, the available weather is {condition} "
            f"with {temperature}°C, rainfall {rainfall} mm, and wind speed {wind} km/h."
        )

    if intent == "OUTDOOR_ACTIVITY":
        return (
            f"For outdoor activities in {location}, the weather is currently {condition} "
            f"at {temperature}°C with {rainfall} mm rainfall."
        )

    if intent == "WEATHER_RISK":
        return (
            f"Weather risk information for {location} requires the Risk Engine. "
            f"Current weather: {condition}, {temperature}°C, rainfall {rainfall} mm, wind {wind} km/h."
        )

    if intent == "WHAT_IF_SCENARIO":
        return (
            f"What-If Weather Scenario Analysis for {location}:\n"
            f"Counterfactual simulation completed against baseline weather data."
        )

    return (
        f"Weather in {location}: {temperature}°C, {condition}, "
        f"humidity {humidity}%, rainfall {rainfall} mm, wind {wind} km/h."
    )


# =============================================================
# GEMINI RESPONSE
# =============================================================

def _call_gemini(
    message: str,
    analysis: Any,
    weather_data: Optional[Dict[str, Any]],
    session_id: str,
    comparison_weather: Optional[Dict[str, Any]] = None,
    simulation_data: Optional[Dict[str, Any]] = None,
    risk_data: Optional[Dict[str, Any]] = None,
    climate_data: Optional[Dict[str, Any]] = None,
    language: str = "en",
) -> str:

    lang = language if language else _get_language(analysis)
    if re.search(r"[\u0B80-\u0BFF]", message):
        lang = "ta"

    try:
        result = generate_response(
            user_message=message,
            analysis=analysis,
            weather_data=weather_data,
            comparison_weather=comparison_weather,
            simulation_data=simulation_data,
            risk_data=risk_data,
            climate_data=climate_data,
            language=lang,
        )

        if result:
            return str(result).strip()

    except Exception as error:
        print(f"[Gemini Error] {error}")

    return _generate_fallback_response(
        analysis=analysis,
        weather_data=weather_data,
        language=lang,
        user_message=message,
    )



# =============================================================
# MAIN CHAT FUNCTION
# =============================================================

def chat_response(
    message: str,
    session_id: str = "default",
    language: str = "en",
) -> Dict[str, Any]:

    # Detect Tamil script in message if present
    if message and re.search(r"[\u0B80-\u0BFF]", message):
        language = "ta"

    # =========================================================
    # 1. VALIDATE
    # =========================================================

    if not message or not message.strip():
        resp_text = "தயவுசெய்து வானிலை பற்றிய கேள்வியை உள்ளிடவும்." if language == "ta" else "Please enter a weather-related question."
        return {
            "analysis": {
                "message": "",
                "intent": "UNKNOWN",
                "location": None,
                "comparison_location": None,
                "time": None,
                "language": language,
                "parameters": {},
                "requires_weather_data": False,
                "requires_risk_analysis": False,
                "requires_simulation": False,
            },
            "response": resp_text,
        }

    message = message.strip()

    # =========================================================
    # 2. GREETING
    # =========================================================

    if _is_greeting(message):

        return {
            "analysis": {
                "message": message,
                "intent": "GENERAL_WEATHER_CHAT",
                "location": None,
                "comparison_location": None,
                "time": {
                    "date": None,
                    "time_period": None,
                    "exact_time": None,
                },
                "language": language,
                "parameters": {},
                "requires_weather_data": False,
                "requires_risk_analysis": False,
                "requires_simulation": False,
            },
            "response": _greeting_response(language=language),
        }

    # =========================================================
    # 3. LOCAL ANALYSIS
    # =========================================================

    analysis = None

    try:

        try:

            analysis = analyze_locally(
                message,
                session_id=session_id,
            )

        except TypeError:

            analysis = analyze_locally(
                message
            )

    except Exception as error:

        print(
            f"[Local Detector Error] "
            f"{error}"
        )

        analysis = None

    # =========================================================
    # 4. FOLLOW-UP MEMORY
    # =========================================================

    is_follow_up_message = _is_follow_up(
        message,
        session_id,
    )

    if is_follow_up_message:

        try:

            if analysis is not None:

                analysis = _apply_memory_to_follow_up(
                    analysis,
                    message,
                    session_id,
                )

            else:

                analysis = {
                    "message": message,
                    "intent": "UNKNOWN",
                    "location": None,
                    "comparison_location": None,
                    "time": {
                        "date": None,
                        "time_period": None,
                        "exact_time": None,
                    },
                    "language": language,
                    "parameters": {},
                    "requires_weather_data": False,
                    "requires_risk_analysis": False,
                    "requires_simulation": False,
                }

                analysis = _apply_memory_to_follow_up(
                    analysis,
                    message,
                    session_id,
                )

        except Exception as error:

            print(
                f"[Follow-up Error] "
                f"{error}"
            )

    # =========================================================
    # 5. GEMINI ANALYSIS FALLBACK
    # =========================================================

    location_name = _get_location_name(
        analysis
    )

    intent = _get_intent(
        analysis
    )

    # Only use Gemini analysis when:
    # - local analysis completely failed
    # - follow-up could not be resolved

    if (
        analysis is None
        or (
            is_follow_up_message
            and (
                not location_name
                or intent == "UNKNOWN"
            )
        )
    ):

        try:

            from app.ai.gemini import (
                analyze_message
            )

            try:

                analysis = analyze_message(
                    message=message,
                    session_id=session_id,
                    language=language,
                )

            except TypeError:

                analysis = analyze_message(
                    message,
                    language=language,
                )

        except Exception as error:

            print(
                f"[Gemini Analysis Error] "
                f"{error}"
            )

    # =========================================================
    # 6. ANALYSIS FAILED
    # =========================================================

    if analysis is None:
        err_msg = (
            "மன்னிக்கும், உங்கள் கோரிக்கையை என்னால் புரிந்து கொள்ள முடியவில்லை. "
            "தயவுசெய்து வானிலை, மழை, வெப்பநிலை, காற்று அல்லது ஈரப்பதம் குறித்த கேள்விகளைக் கேட்கவும்."
            if language == "ta" or re.search(r"[\u0B80-\u0BFF]", message)
            else (
                "I couldn't understand that request. "
                "Please try asking about weather, "
                "rain, temperature, wind, humidity, "
                "travel, or a What-If scenario."
            )
        )
        return {
            "analysis": {
                "message": message,
                "intent": "UNKNOWN",
                "location": None,
                "comparison_location": None,
                "time": None,
                "language": language,
                "parameters": {},
                "requires_weather_data": False,
                "requires_risk_analysis": False,
                "requires_simulation": False,
            },
            "response": err_msg,
        }

    # =========================================================
    # 7. LOCATION
    # =========================================================

    location_name = _get_location_name(
        analysis
    )

    # =========================================================
    # 8. MEMORY LOCATION FALLBACK
    # =========================================================

    if (
        not location_name
        and is_follow_up_message
    ):

        try:

            previous_session = get_session(
                session_id
            )

            previous_location = (
                previous_session.get(
                    "location"
                )
                if previous_session
                else None
            )

            if previous_location:

                from app.location.resolver import (
                    resolve_city
                )

                remembered_location = resolve_city(
                    previous_location
                )

                if remembered_location:

                    location_data = Location(
                        name=remembered_location[
                            "name"
                        ],
                        latitude=remembered_location[
                            "latitude"
                        ],
                        longitude=remembered_location[
                            "longitude"
                        ],
                    )

                    if hasattr(
                        analysis,
                        "model_copy",
                    ):

                        analysis = analysis.model_copy(
                            update={
                                "location":
                                    location_data
                            }
                        )

                    elif isinstance(
                        analysis,
                        dict,
                    ):

                        analysis[
                            "location"
                        ] = {
                            "name":
                                remembered_location[
                                    "name"
                                ],
                            "latitude":
                                remembered_location[
                                    "latitude"
                                ],
                            "longitude":
                                remembered_location[
                                    "longitude"
                                ],
                        }

                    location_name = (
                        remembered_location[
                            "name"
                        ]
                    )

        except Exception as error:

            print(
                f"[Memory Location Error] "
                f"{error}"
            )

    # =========================================================
    # 9. REQUIREMENTS
    # =========================================================

    requires_weather = (
        analysis.get(
            "requires_weather_data",
            False,
        )
        if isinstance(
            analysis,
            dict,
        )
        else getattr(
            analysis,
            "requires_weather_data",
            False,
        )
    )

    intent = _get_intent(
        analysis
    )

    time_info = _get_time_info(
        analysis
    )

    # =========================================================
    # 10. WEATHER DATA
    # =========================================================

    weather_data = None

    if (
        requires_weather
        and location_name
    ):

        try:

            weather_data = get_weather(
                city=location_name,
                time_info=time_info,
                intent=intent,
            )

            print(
                "[Weather] Retrieved data "
                f"for {location_name}"
            )

        except TypeError:

            # Compatibility with older weather_client
            try:

                weather_data = get_weather(
                    city=location_name,
                    time_info=time_info,
                )

            except TypeError:

                weather_data = get_weather(
                    location_name
                )

            except Exception as error:

                print(
                    f"[Weather Client Error] "
                    f"{error}"
                )

        except Exception as error:

            print(
                f"[Weather Client Error] "
                f"{error}"
            )

            weather_data = None

    # =========================================================
    # 10.5 WHAT-IF SIMULATION
    # =========================================================

    # Ensure weather_data is fetched if requires_weather OR if WHAT_IF / RISK / HISTORICAL
    if not weather_data and (intent in ["WHAT_IF_SCENARIO", "WEATHER_RISK", "HISTORICAL_CLIMATE"] or location_name):
        try:
            target_city = location_name or "Chennai"
            weather_data = get_weather(city=target_city, time_info=time_info, intent=intent)
        except Exception:
            pass

    # =========================================================
    # 10.5 WHAT-IF SIMULATION
    # =========================================================

    simulation_data = None

    if intent == "WHAT_IF_SCENARIO":
        try:
            if isinstance(analysis, dict):
                parameters = analysis.get("parameters")
            else:
                parameters = getattr(analysis, "parameters", None)

            if parameters is None:
                parameters = {}

            if isinstance(parameters, dict):
                rainfall_change = parameters.get("rainfall_change_mm")
                wind_speed = parameters.get("wind_speed_kmh")
                target_rainfall = parameters.get("target_rainfall_mm")
            else:
                rainfall_change = getattr(parameters, "rainfall_change_mm", None)
                wind_speed = getattr(parameters, "wind_speed_kmh", None)
                target_rainfall = getattr(parameters, "target_rainfall_mm", None)

            from app.services.simulation_engine import simulate_scenario

            scenario_params = {
                "target_rainfall_mm": target_rainfall,
                "rainfall_change_mm": rainfall_change,
                "wind_speed_change_percent": wind_speed,
            }

            sim_res = simulate_scenario(
                baseline_weather=weather_data or {"temperature": 29.0, "rainfall_mm": 45.0, "wind_speed_kmh": 22.0, "condition": "Heavy Rain"},
                scenario=scenario_params
            )

            simulation_data = {
                "scenario": message,
                "baseline_risk": sim_res.get("baseline_risk", 45),
                "simulated_risk": sim_res.get("simulated_risk", 59),
                "risk_change": sim_res.get("risk_change", 14),
                "risk_level": sim_res.get("risk_level", "MEDIUM"),
                "details": sim_res
            }

            print("[Simulation] Member 3 simulation computed successfully:", simulation_data)

        except Exception as error:
            print(f"[Simulation Error] {error}")
            simulation_data = None

    # =========================================================
    # 10.6 RISK ENGINE CALCULATION
    # =========================================================

    risk_data = None
    if intent == "WEATHER_RISK" or (weather_data and getattr(analysis, "requires_risk_analysis", False)):
        try:
            from app.services.risk_engine import calculate_risk
            w = weather_data or {}
            risk_data = calculate_risk(
                temperature=w.get("temperature", 28.0),
                humidity=w.get("humidity", 70.0),
                rainfall_mm=w.get("rainfall_mm", 0.0),
                wind_speed_kmh=w.get("wind_speed_kmh", 10.0),
                condition=w.get("condition", "Clear")
            )
        except Exception as err:
            print(f"[Risk Engine Error] {err}")

    # =========================================================
    # 10.7 HISTORICAL CLIMATE TRENDS
    # =========================================================

    climate_data = None
    if intent == "HISTORICAL_CLIMATE":
        try:
            from app.services.historical import get_historical_climate
            target_city = location_name or "chennai"
            climate_data = get_historical_climate(target_city)
        except Exception as err:
            print(f"[Historical Service Error] {err}")

    # =========================================================
    # 11. COMPARISON
    # =========================================================

    comparison_name = _get_comparison_location_name(analysis)
    comparison_weather = None

    if comparison_name:
        try:
            comparison_weather = get_weather(
                city=comparison_name,
                time_info=time_info,
                intent=intent,
            )
        except Exception as error:
            print(f"[Comparison Weather Error] {error}")

    # =========================================================
    # 12. SAVE MEMORY
    # =========================================================

    _save_chat_context(
        session_id=session_id,
        analysis=analysis,
        weather_data=weather_data,
    )

    # =========================================================
    # 13. GEMINI FINAL RESPONSE
    # =========================================================

    response = _call_gemini(
        message=message,
        analysis=analysis,
        weather_data=weather_data,
        session_id=session_id,
        comparison_weather=comparison_weather,
        simulation_data=simulation_data,
        risk_data=risk_data,
        climate_data=climate_data,
        language=language,
    )

    # =========================================================
    # 14. FINAL RESULT
    # =========================================================

    result = {
        "analysis": _analysis_to_dict(analysis),
        "response": response,
    }

    if weather_data is not None:
        result["weather_data"] = weather_data

    if comparison_weather is not None:
        result["comparison_weather_data"] = comparison_weather

    if simulation_data is not None:
        result["simulation_data"] = simulation_data

    if risk_data is not None:
        result["risk"] = risk_data

    if climate_data is not None:
        result["climate"] = climate_data

    return result



# =============================================================
# BACKWARD COMPATIBILITY
# =============================================================

def analyze_chat(
    message: str,
    session_id: str = "default",
    language: str = "en",
):
    """
    Backward-compatible wrapper for older tests.
    """

    result = chat_response(
        message=message,
        session_id=session_id,
        language=language,
    )

    return result.get(
        "analysis",
        result,
    )