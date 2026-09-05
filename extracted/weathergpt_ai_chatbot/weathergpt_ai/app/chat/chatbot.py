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


# =============================================================
# GREETING
# =============================================================

def _is_greeting(
    message: str,
) -> bool:

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
    }

    return text in greetings


def _greeting_response() -> str:

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
) -> str:

    location = _get_location_name(
        analysis
    )

    intent = _get_intent(
        analysis
    )

    if not location:
        location = "your location"

    if not weather_data:

        return (
            f"Weather information for "
            f"{location} is currently unavailable."
        )

    if not isinstance(
        weather_data,
        dict,
    ):

        return (
            "Weather data was received, "
            "but I could not format it."
        )

    temperature = weather_data.get(
        "temperature"
    )

    humidity = weather_data.get(
        "humidity"
    )

    rainfall = weather_data.get(
        "rainfall_mm"
    )

    wind = weather_data.get(
        "wind_speed_kmh"
    )

    condition = weather_data.get(
        "condition"
    )

    requested_date = weather_data.get(
        "requested_date"
    )

    # ---------------------------------------------------------
    # Current
    # ---------------------------------------------------------

    if intent == "CURRENT_WEATHER":

        return (
            f"Current weather in {location}: "
            f"{temperature}°C, {condition}. "
            f"Humidity is {humidity}%, "
            f"rainfall is {rainfall} mm, "
            f"and wind speed is {wind} km/h."
        )

    # ---------------------------------------------------------
    # Rain
    # ---------------------------------------------------------

    if intent == "RAIN_FORECAST":

        period = (
            f" for {requested_date}"
            if requested_date
            else ""
        )

        return (
            f"Rain forecast for {location}{period}: "
            f"rainfall is {rainfall} mm "
            f"with conditions reported as "
            f"{condition}."
        )

    # ---------------------------------------------------------
    # Temperature
    # ---------------------------------------------------------

    if intent == "TEMPERATURE":

        return (
            f"The temperature in {location} "
            f"is {temperature}°C."
        )

    # ---------------------------------------------------------
    # Wind
    # ---------------------------------------------------------

    if intent == "WIND":

        return (
            f"Wind speed in {location} "
            f"is {wind} km/h."
        )

    # ---------------------------------------------------------
    # Humidity
    # ---------------------------------------------------------

    if intent == "HUMIDITY":

        return (
            f"Humidity in {location} "
            f"is {humidity}%."
        )

    # ---------------------------------------------------------
    # Daily
    # ---------------------------------------------------------

    if intent == "DAILY_FORECAST":

        period = (
            f" for {requested_date}"
            if requested_date
            else ""
        )

        return (
            f"Daily weather information for "
            f"{location}{period}: "
            f"{temperature}°C, {condition}, "
            f"humidity {humidity}%, "
            f"rainfall {rainfall} mm, "
            f"wind {wind} km/h."
        )

    # ---------------------------------------------------------
    # Hourly
    # ---------------------------------------------------------

    if intent == "HOURLY_FORECAST":

        return (
            f"Hourly weather information for "
            f"{location}: "
            f"{temperature}°C, {condition}, "
            f"humidity {humidity}%, "
            f"rainfall {rainfall} mm, "
            f"wind {wind} km/h."
        )

    # ---------------------------------------------------------
    # Travel
    # ---------------------------------------------------------

    if intent == "TRAVEL_WEATHER":

        return (
            f"For travel to {location}, "
            f"the available weather is "
            f"{condition} with {temperature}°C, "
            f"rainfall {rainfall} mm, "
            f"and wind speed {wind} km/h."
        )

    # ---------------------------------------------------------
    # Outdoor
    # ---------------------------------------------------------

    if intent == "OUTDOOR_ACTIVITY":

        return (
            f"For outdoor activities in {location}, "
            f"the weather is currently {condition} "
            f"at {temperature}°C with "
            f"{rainfall} mm rainfall."
        )

    # ---------------------------------------------------------
    # Risk
    # ---------------------------------------------------------

    if intent == "WEATHER_RISK":

        return (
            f"Weather risk information for "
            f"{location} requires the Risk Engine. "
            f"Current weather: {condition}, "
            f"{temperature}°C, rainfall {rainfall} mm, "
            f"wind {wind} km/h."
        )

    # ---------------------------------------------------------
    # What-If
    # ---------------------------------------------------------

    if intent == "WHAT_IF_SCENARIO":

        return (
            f"I understood the What-If scenario "
            f"for {location}. "
            f"The scenario data is ready to be passed "
            f"to the Risk and Simulation modules."
        )

    # ---------------------------------------------------------
    # Default
    # ---------------------------------------------------------

    return (
        f"Weather in {location}: "
        f"{temperature}°C, {condition}, "
        f"humidity {humidity}%, "
        f"rainfall {rainfall} mm, "
        f"wind {wind} km/h."
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
) -> str:

    try:

        result = generate_response(
            user_message=message,
            analysis=analysis,
            weather_data=weather_data,
            comparison_weather=comparison_weather,
            simulation_data=simulation_data,
        )

        if result:

            return str(
                result
            ).strip()

    except Exception as error:

        print(
            f"[Gemini Error] {error}"
        )

    return _generate_fallback_response(
        analysis,
        weather_data,
    )


# =============================================================
# MAIN CHAT FUNCTION
# =============================================================

def chat_response(
    message: str,
    session_id: str = "default",
    language: str = "en",
) -> Dict[str, Any]:

    # =========================================================
    # 1. VALIDATE
    # =========================================================

    if not message or not message.strip():

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
            "response":
                "Please enter a weather-related question.",
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
            "response":
                _greeting_response(),
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
            "response": (
                "I couldn't understand that request. "
                "Please try asking about weather, "
                "rain, temperature, wind, humidity, "
                "travel, or a What-If scenario."
            ),
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

    simulation_data = None

    if (
        intent == "WHAT_IF_SCENARIO"
        and weather_data
    ):

        try:

            if isinstance(
                analysis,
                dict,
            ):

                parameters = analysis.get(
                    "parameters"
                )

            else:

                parameters = getattr(
                    analysis,
                    "parameters",
                    None,
                )

            if parameters is None:
                parameters = {}

            if isinstance(
                parameters,
                dict,
            ):

                rainfall_change = parameters.get(
                    "rainfall_change_mm"
                )

                wind_speed = parameters.get(
                    "wind_speed_kmh"
                )

                target_rainfall = parameters.get(
                    "target_rainfall_mm"
                )

            else:

                rainfall_change = getattr(
                    parameters,
                    "rainfall_change_mm",
                    None,
                )

                wind_speed = getattr(
                    parameters,
                    "wind_speed_kmh",
                    None,
                )

                target_rainfall = getattr(
                    parameters,
                    "target_rainfall_mm",
                    None,
                )

            print(
                "[Simulation] Parameters:",
                parameters,
            )

            print(
                "[Simulation] Rainfall change:",
                rainfall_change,
            )

            print(
                "[Simulation] Target rainfall:",
                target_rainfall,
            )

            print(
                "[Simulation] Wind speed:",
                wind_speed,
            )

            # -------------------------------------------------
            # TEMPORARY MOCK
            # Replace with Member 3
            # -------------------------------------------------

            baseline_risk = 45

            simulated_risk = baseline_risk

            if rainfall_change is not None:

                simulated_risk = min(
                    100,
                    baseline_risk
                    + int(
                        rainfall_change
                        * 0.27
                    ),
                )

            elif target_rainfall is not None:

                current_rainfall = weather_data.get(
                    "rainfall_mm",
                    0,
                )

                rainfall_difference = (
                    target_rainfall
                    - current_rainfall
                )

                simulated_risk = min(
                    100,
                    max(
                        0,
                        baseline_risk
                        + int(
                            rainfall_difference
                            * 0.27
                        ),
                    ),
                )

            elif wind_speed is not None:

                current_wind = weather_data.get(
                    "wind_speed_kmh",
                    0,
                )

                wind_difference = (
                    wind_speed
                    - current_wind
                )

                simulated_risk = min(
                    100,
                    max(
                        0,
                        baseline_risk
                        + int(
                            wind_difference
                            * 0.5
                        ),
                    ),
                )

            risk_change = (
                simulated_risk
                - baseline_risk
            )

            if simulated_risk >= 70:

                risk_level = "HIGH"

            elif simulated_risk >= 40:

                risk_level = "MEDIUM"

            else:

                risk_level = "LOW"

            simulation_data = {
                "scenario": message,
                "baseline_risk": baseline_risk,
                "simulated_risk": simulated_risk,
                "risk_change": risk_change,
                "risk_level": risk_level,
            }

            print(
                "[Simulation] "
                "Temporary mock simulation created"
            )

            print(
                "[Simulation] Result:",
                simulation_data,
            )

        except Exception as error:

            print(
                f"[Simulation Error] "
                f"{error}"
            )

            simulation_data = None

    # =========================================================
    # 11. COMPARISON
    # =========================================================

    comparison_name = (
        _get_comparison_location_name(
            analysis
        )
    )

    comparison_weather = None

    if comparison_name:

        try:

            comparison_weather = get_weather(
                city=comparison_name,
                time_info=time_info,
                intent=intent,
            )

            print(
                "[Comparison Weather] "
                f"Retrieved data for "
                f"{comparison_name}"
            )

        except TypeError:

            try:

                comparison_weather = get_weather(
                    city=comparison_name,
                    time_info=time_info,
                )

            except TypeError:

                comparison_weather = get_weather(
                    comparison_name
                )

            except Exception as error:

                print(
                    f"[Comparison Weather Error] "
                    f"{error}"
                )

        except Exception as error:

            print(
                f"[Comparison Weather Error] "
                f"{error}"
            )

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
    )

    # =========================================================
    # 14. FINAL RESULT
    # =========================================================

    result = {
        "analysis":
            _analysis_to_dict(
                analysis
            ),
        "response":
            response,
    }

    if weather_data is not None:

        result[
            "weather_data"
        ] = weather_data

    if comparison_weather is not None:

        result[
            "comparison_weather_data"
        ] = comparison_weather

    if simulation_data is not None:

        result[
            "simulation_data"
        ] = simulation_data

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