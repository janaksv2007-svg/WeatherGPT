import re

from typing import Optional

from app.location.message_resolver import resolve_location_from_message
from app.location.resolver import resolve_city

from app.models.schemas import (
    ChatAnalysis,
    Location,
    TimeInfo,
    Parameters,
)


# ============================================================
# KNOWN LOCATIONS
# ============================================================

KNOWN_LOCATIONS = [
    "Chennai",
    "Bangalore",
    "Bengaluru",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Coimbatore",
    "Madurai",
    "Trichy",
    "Salem",
    "Mysore",
    "Mysuru",
    "Pallikaranai",
    # Tamil script location names
    "சென்னை",
    "சென்னைக்கு",
    "சென்னையில்",
    "பள்ளிக்கரணை",
    "மதுரை",
    "கோயம்புத்தூர்",
    "கோவை",
    "திருச்சி",
    "சேலம்",
]



# ============================================================
# LOCATION DETECTION
# ============================================================

def detect_comparison_locations(message: str):

    text = message.lower()

    if not (
        "compare" in text
        or "comparison" in text
        or "versus" in text
        or " vs " in text
        or "difference between" in text
    ):
        return None

    found_locations = []

    for location in KNOWN_LOCATIONS:

        if re.search(
            rf"\b{re.escape(location.lower())}\b",
            text,
        ):
            found_locations.append(location)

    unique_locations = []

    for location in found_locations:

        if location not in unique_locations:
            unique_locations.append(location)

    if len(unique_locations) >= 2:
        return unique_locations[:2]

    return None


def detect_location(message: str) -> Optional[str]:

    message_lower = message.lower()

    for location in KNOWN_LOCATIONS:

        if re.search(
            rf"\b{re.escape(location.lower())}\b",
            message_lower,
        ):
            return location

    return None


def detect_location_with_database(message: str):

    location = detect_location(message)

    if location is not None:

        city_data = resolve_city(location)

        if city_data is not None:
            return city_data["name"], city_data

        return location, None

    city = resolve_location_from_message(message)

    if city is not None:
        return city["name"], city

    return None, None


# ============================================================
# TIME DETECTION
# ============================================================

def detect_time(message: str) -> TimeInfo:

    text = message.lower().strip()

    date = None
    time_period = None
    exact_time = None

    # ========================================================
    # DATE
    # ========================================================

    # --------------------------------------------------------
    # English
    # --------------------------------------------------------

    if "tomorrow" in text:

        date = "tomorrow"

    elif "tonight" in text:

        date = "today"
        time_period = "night"

    elif "today" in text:

        date = "today"

    elif (
        "this weekend" in text
        or "weekend" in text
    ):

        date = "weekend"

    elif "next week" in text:

        date = "next week"

    elif "weekdays" in text:

        date = "weekdays"

    # --------------------------------------------------------
    # Tamil
    # --------------------------------------------------------

    elif any(
        phrase in text
        for phrase in [
            "நாளை",
            "நாளைக்கு",
            "நாளில்",
        ]
    ):

        date = "tomorrow"

    elif any(
        phrase in text
        for phrase in [
            "இன்று",
            "இன்றைக்கு",
        ]
    ):

        date = "today"

    elif any(
        phrase in text
        for phrase in [
            "இந்த வார இறுதி",
            "வார இறுதி",
        ]
    ):

        date = "weekend"

    # --------------------------------------------------------
    # Hindi
    # --------------------------------------------------------

    elif any(
        phrase in text
        for phrase in [
            "कल",
            "कल को",
        ]
    ):

        date = "tomorrow"

    elif any(
        phrase in text
        for phrase in [
            "आज",
            "आज के",
        ]
    ):

        date = "today"

    elif any(
        phrase in text
        for phrase in [
            "इस सप्ताहांत",
            "सप्ताहांत",
        ]
    ):

        date = "weekend"

    # ========================================================
    # TIME PERIOD
    # ========================================================

    # --------------------------------------------------------
    # English
    # --------------------------------------------------------

    if "morning" in text:

        time_period = "morning"

    elif "afternoon" in text:

        time_period = "afternoon"

    elif "evening" in text:

        time_period = "evening"

    elif "night" in text:

        time_period = "night"

    # --------------------------------------------------------
    # Tamil
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "காலை",
            "காலையில்",
        ]
    ):

        time_period = "morning"

    elif any(
        phrase in text
        for phrase in [
            "மதியம்",
            "மதியத்தில்",
        ]
    ):

        time_period = "afternoon"

    elif any(
        phrase in text
        for phrase in [
            "மாலை",
            "மாலையில்",
        ]
    ):

        time_period = "evening"

    elif any(
        phrase in text
        for phrase in [
            "இரவு",
            "இரவில்",
            "இன்றிரவு",
        ]
    ):

        time_period = "night"

    # --------------------------------------------------------
    # Hindi
    # --------------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "सुबह",
            "सुबह में",
        ]
    ):

        time_period = "morning"

    elif any(
        phrase in text
        for phrase in [
            "दोपहर",
            "दोपहर में",
        ]
    ):

        time_period = "afternoon"

    elif any(
        phrase in text
        for phrase in [
            "शाम",
            "शाम में",
        ]
    ):

        time_period = "evening"

    elif any(
        phrase in text
        for phrase in [
            "रात",
            "रात में",
        ]
    ):

        time_period = "night"

    # ========================================================
    # EXACT TIME
    # ========================================================

    time_match = re.search(
        r"\b(?:after|at|around|before)\s+"
        r"(\d{1,2})"
        r"(?::(\d{2}))?"
        r"\s*(am|pm)?\b",
        text,
    )

    if time_match:

        hour = int(
            time_match.group(1)
        )

        minute = int(
            time_match.group(2) or 0
        )

        meridiem = time_match.group(3)

        if meridiem:

            if (
                meridiem == "pm"
                and hour != 12
            ):
                hour += 12

            elif (
                meridiem == "am"
                and hour == 12
            ):
                hour = 0

        if (
            0 <= hour <= 23
            and 0 <= minute <= 59
        ):

            exact_time = (
                f"{hour:02d}:{minute:02d}"
            )

            if 5 <= hour < 12:
                time_period = "morning"

            elif 12 <= hour < 17:
                time_period = "afternoon"

            elif 17 <= hour < 21:
                time_period = "evening"

            else:
                time_period = "night"

            if date is None:
                date = "today"

    # ========================================================
    # RELATIVE HOURS
    # ========================================================

    relative_hours = re.search(
        r"\bin\s+(\d+)\s+hours?\b",
        text,
    )

    if relative_hours:

        hours = int(
            relative_hours.group(1)
        )

        date = "relative"

        exact_time = (
            f"in {hours} hours"
        )

    # ========================================================
    # RELATIVE MINUTES
    # ========================================================

    relative_minutes = re.search(
        r"\bin\s+(\d+)\s+minutes?\b",
        text,
    )

    if relative_minutes:

        minutes = int(
            relative_minutes.group(1)
        )

        date = "relative"

        exact_time = (
            f"in {minutes} minutes"
        )

    # ========================================================
    # THIS MORNING / AFTERNOON / EVENING
    # ========================================================

    if "this morning" in text:

        if date is None:
            date = "today"

        time_period = "morning"

    elif "this afternoon" in text:

        if date is None:
            date = "today"

        time_period = "afternoon"

    elif "this evening" in text:

        if date is None:
            date = "today"

        time_period = "evening"

    elif "this night" in text:

        if date is None:
            date = "today"

        time_period = "night"

    return TimeInfo(
        date=date,
        time_period=time_period,
        exact_time=exact_time,
    )


# ============================================================
# MULTILINGUAL KEYWORDS
# ============================================================

RAIN_WORDS = [
    "rain",
    "rainfall",
    "precipitation",

    # Tamil
    "மழை",
    "மழைக்கு",
    "மழைபெய்யுமா",

    # Hindi
    "बारिश",
    "बारिशहोगी",
    "वर्षा",
]


WEATHER_WORDS = [
    "weather",

    # Tamil
    "வானிலை",

    # Hindi
    "मौसम",
]


TEMPERATURE_WORDS = [
    "temperature",
    "temp",
    "hot",
    "cold",

    # Tamil
    "வெப்பநிலை",
    "சூடு",
    "குளிர்",

    # Hindi
    "तापमान",
    "गर्मी",
    "ठंड",
]


WIND_WORDS = [
    "wind",
    "windy",

    # Tamil
    "காற்று",

    # Hindi
    "हवा",
]


HUMIDITY_WORDS = [
    "humidity",

    # Tamil
    "ஈரப்பதம்",

    # Hindi
    "नमी",
]

# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_language(message: str) -> str:

    text = message.strip()

    # --------------------------------------------------------
    # Tamil Unicode range
    # --------------------------------------------------------

    tamil_characters = re.findall(
        r"[\u0B80-\u0BFF]",
        text,
    )

    # --------------------------------------------------------
    # Hindi / Devanagari Unicode range
    # --------------------------------------------------------

    hindi_characters = re.findall(
        r"[\u0900-\u097F]",
        text,
    )

    # --------------------------------------------------------
    # Determine language
    # --------------------------------------------------------

    if len(tamil_characters) > 0:

        return "ta"

    if len(hindi_characters) > 0:

        return "hi"

    return "en"


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(message: str) -> str:

    text = message.lower().strip()

    # ========================================================
    # OUTDOOR
    # ========================================================

    outdoor_keywords = [
        "go outside",
        "go outdoors",
        "outdoor",
        "outside",
        "play outside",
        "walk outside",
        "walking",
        "jogging",
        "running",
        "cycling",
        "picnic",
        "hiking",
        "outdoor activity",
        "play cricket",
        "play football",
        "play sports",
    ]

    if any(
        keyword in text
        for keyword in outdoor_keywords
    ):

        return "OUTDOOR_ACTIVITY"

    # ========================================================
    # HISTORICAL CLIMATE
    # ========================================================

    if any(
        kw in text
        for kw in [
            "historic",
            "historical",
            "climate",
            "trend",
            "past years",
            "past weather",
            "history",
            "climate trends",
            "average rainfall",
            "records",
            "வரலாறு",
            "வரலாற்று",
            "கடந்த கால",
        ]
    ):
        return "HISTORICAL_CLIMATE"

    # ========================================================
    # COMPARISON
    # ========================================================

    if (
        "compare" in text
        or "comparison" in text
        or " vs " in text
        or "versus" in text
        or "difference between" in text
    ):

        return "WEATHER_COMPARISON"

    # ========================================================
    # WHAT-IF
    # ========================================================

    if any(
        kw in text
        for kw in [
            "what if",
            "suppose",
            "if rainfall",
            "if rain",
            "if wind speed",
            "if wind",
            "simulate",
            "simulation",
            "scenario",
            "modelling",
        ]
    ):

        return "WHAT_IF_SCENARIO"

    # ========================================================
    # TRAVEL
    # ========================================================

    if any(
        word in text
        for word in [
            "travel",
            "trip",
            "journey",
            "visit",
            "safe to travel",
            "travelling",
            "traveling",
        ]
    ):

        return "TRAVEL_WEATHER"

    # ========================================================
    # RISK
    # ========================================================

    if any(
        word in text
        for word in [
            "risk",
            "risk score",
            "hazard",
            "flood",
            "flooding",
            "dangerous",
            "danger",
            "safe",
            "warning level",
            "ஆபத்து",
            "பாதுகாப்பு",
        ]
    ):

        return "WEATHER_RISK"


        return "WEATHER_RISK"

    # ========================================================
    # EXPLANATION
    # ========================================================

    if any(
        word in text
        for word in [
            "why",
            "explain",
            "meaning",
            "cause",
        ]
    ):

        return "WEATHER_EXPLANATION"

    # ========================================================
    # RAIN
    # ========================================================

    if any(
        word in text
        for word in RAIN_WORDS
    ):

        return "RAIN_FORECAST"

    # ========================================================
    # TEMPERATURE
    # ========================================================

    if any(
        word in text
        for word in TEMPERATURE_WORDS
    ):

        return "TEMPERATURE"

    # ========================================================
    # WIND
    # ========================================================

    if any(
        word in text
        for word in WIND_WORDS
    ):

        return "WIND"

    # ========================================================
    # HUMIDITY
    # ========================================================

    if any(
        word in text
        for word in HUMIDITY_WORDS
    ):

        return "HUMIDITY"
    
    # ========================================================
    # DAILY FORECAST
    # ========================================================

    if any(
        phrase in text
        for phrase in [
            "daily forecast",
            "daily weather",
            "day forecast",
            "7 day forecast",
            "7-day forecast",
            "next few days",
            "forecast for each day",
        ]
    ):

        return "DAILY_FORECAST"
    
    # ========================================================
    # HOURLY
    # ========================================================

    if any(
        word in text
        for word in [
            "hourly",
            "next few hours",
            "next hour",
        ]
    ):

        return "HOURLY_FORECAST"

    # ========================================================
    # FUTURE FORECAST
    # ========================================================

    future_words = [
        "tomorrow",
        "tonight",
        "this evening",
        "this morning",
        "this afternoon",
        "this weekend",
        "weekend",
        "next week",
        "next month",

        # Tamil
        "நாளை",
        "நாளைக்கு",
        "இன்று",
        "இன்றைக்கு",
        "இந்த வார இறுதி",
        "வார இறுதி",

        # Hindi
        "कल",
        "आज",
        "इस सप्ताहांत",
        "सप्ताहांत",
    ]

    if any(
        word in text
        for word in future_words
    ):

        return "DAILY_FORECAST"

    # ========================================================
    # CURRENT WEATHER
    # ========================================================

    if any(
        word in text
        for word in WEATHER_WORDS
    ):

        return "CURRENT_WEATHER"

    if any(
        word in text
        for word in [
            "right now",
            "currently",
        ]
    ):

        return "CURRENT_WEATHER"

    # ========================================================
    # GENERAL CHAT
    # ========================================================

    return "GENERAL_WEATHER_CHAT"


# ============================================================
# RAINFALL CHANGE
# ============================================================

# ============================================================
# RAINFALL CHANGE
# ============================================================

def detect_rainfall_change(
    message: str,
) -> Optional[float]:

    text = message.lower()

    # --------------------------------------------------------
    # DECREASE
    # --------------------------------------------------------

    decrease_pattern = (
        r"(?:decrease|decreases|decreased)"
        r".*?"
        r"(?:by\s+)?"
        r"(\d+(?:\.\d+)?)"
        r"\s*mm"
    )

    decrease_match = re.search(
        decrease_pattern,
        text,
    )

    if decrease_match:

        value = float(
            decrease_match.group(1)
        )

        return -value

    # --------------------------------------------------------
    # INCREASE
    # --------------------------------------------------------

    increase_pattern = (
        r"(?:increase|increases|increased)"
        r".*?"
        r"by\s+"
        r"(\d+(?:\.\d+)?)"
        r"\s*mm"
    )

    increase_match = re.search(
        increase_pattern,
        text,
    )

    if increase_match:

        value = float(
            increase_match.group(1)
        )

        return value

    return None
# ============================================================
# TARGET RAINFALL
# ============================================================

def detect_target_rainfall(
    message: str,
) -> Optional[float]:

    text = message.lower()

    # --------------------------------------------------------
    # Examples:
    # "rainfall increases to 100 mm"
    # "rainfall rises to 150 mm"
    # "rainfall reaches 200 mm"
    # "rainfall becomes 80 mm"
    # --------------------------------------------------------

    pattern = (
        r"(?:rainfall|rain|precipitation)"
        r".*?"
        r"(?:increase|increases|increased|"
        r"rise|rises|rose|"
        r"reach|reaches|"
        r"become|becomes)"
        r".*?"
        r"(?:to|reach|reaches|become|becomes)?"
        r"\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*mm"
    )

    match = re.search(
        pattern,
        text,
    )

    if match:
        return float(
            match.group(1)
        )

    return None

# ============================================================
# WIND TARGET
# ============================================================

def detect_wind_target(
    message: str,
) -> Optional[float]:

    text = message.lower()

    pattern = (
        r"(?:wind\s*speed|wind)"
        r".*?"
        r"(?:to|reaches|reach|becomes)"
        r"\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*"
        r"(?:km/h|kmph|kph)"
    )

    match = re.search(
        pattern,
        text,
    )

    if match:

        return float(
            match.group(1)
        )

    return None


# ============================================================
# LOCAL PROCESSING DECISION
# ============================================================

def can_handle_locally(
    message: str,
) -> bool:

    text = message.lower().strip()

    intent = detect_intent(
        message
    )

    # --------------------------------------------------------
    # Follow-up
    # --------------------------------------------------------

    follow_up_phrases = [
        "what about",
        "how about",
        "there",
        "that city",
        "same place",
        "also",
        "and tomorrow",
        "and evening",
        "and morning",
        "and afternoon",
        "what then",
    ]

    for phrase in follow_up_phrases:

        if phrase in text:
            return False

    # --------------------------------------------------------
    # Explanation → Gemini
    # --------------------------------------------------------

    if intent == "WEATHER_EXPLANATION":
        return False

    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    if intent == "WEATHER_COMPARISON":

        locations = detect_comparison_locations(
            message
        )

        return locations is not None

    # --------------------------------------------------------
    # What-If
    # --------------------------------------------------------

    if intent == "WHAT_IF_SCENARIO":

        rainfall_change = detect_rainfall_change(
            message
        )

        target_rainfall = detect_target_rainfall(
            message
        )

        wind_target = detect_wind_target(
            message
        )

        return (
            rainfall_change is not None
            or target_rainfall is not None
            or wind_target is not None
        )

    # --------------------------------------------------------
    # Risk
    # --------------------------------------------------------

    if intent == "WEATHER_RISK":
        return True

    # --------------------------------------------------------
    # Travel
    # --------------------------------------------------------

    if intent == "TRAVEL_WEATHER":
        return True

    # --------------------------------------------------------
    # Outdoor
    # --------------------------------------------------------

    if intent == "OUTDOOR_ACTIVITY":
        return True

    return True


# ============================================================
# WHAT-IF ANALYZER
# ============================================================

def analyze_what_if_locally(
    message: str,
    session_id: str,
) -> Optional[ChatAnalysis]:

    location_name, city_data = (
        detect_location_with_database(
            message
        )
    )

    # --------------------------------------------------------
    # Location is optional for What-If
    # --------------------------------------------------------

    location = Location(
        name=location_name,
        latitude=(
            city_data["latitude"]
            if city_data
            else None
        ),
        longitude=(
            city_data["longitude"]
            if city_data
            else None
        ),
    )

    time_info = detect_time(
        message
    )

    rainfall_change = detect_rainfall_change(
        message
    )

    target_rainfall = detect_target_rainfall(
        message
    )

    wind_target = detect_wind_target(
        message
    )

    if (
        rainfall_change is None
        and target_rainfall is None
        and wind_target is None
    ):

        return None

    parameters = Parameters(
        rainfall_change_mm=rainfall_change,
        wind_speed_kmh=wind_target,
        target_rainfall_mm=target_rainfall,
    )

    return ChatAnalysis(
        message=message,
        intent="WHAT_IF_SCENARIO",
        location=location,
        comparison_location=None,
        time=time_info,
        language=detect_language(message),
        parameters=parameters,
        requires_weather_data=True,
        requires_risk_analysis=True,
        requires_simulation=True,
    )


# ============================================================
# COMPARISON ANALYZER
# ============================================================

def analyze_comparison_locally(
    message: str,
    session_id: str,
) -> Optional[ChatAnalysis]:

    locations = detect_comparison_locations(
        message
    )

    if locations is None:
        return None

    # --------------------------------------------------------
    # Primary
    # --------------------------------------------------------

    primary_city = resolve_location_from_message(
        f"in {locations[0]}"
    )

    primary_location = Location(
        name=(
            primary_city["name"]
            if primary_city
            else locations[0]
        ),
        latitude=(
            primary_city["latitude"]
            if primary_city
            else None
        ),
        longitude=(
            primary_city["longitude"]
            if primary_city
            else None
        ),
    )

    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    second_city = resolve_location_from_message(
        f"in {locations[1]}"
    )

    second_location = Location(
        name=(
            second_city["name"]
            if second_city
            else locations[1]
        ),
        latitude=(
            second_city["latitude"]
            if second_city
            else None
        ),
        longitude=(
            second_city["longitude"]
            if second_city
            else None
        ),
    )

    time_info = detect_time(
        message
    )

    return ChatAnalysis(
        message=message,
        intent="WEATHER_COMPARISON",
        location=primary_location,
        comparison_location=second_location,
        time=time_info,
        language=detect_language(message),
        parameters=Parameters(),
        requires_weather_data=True,
        requires_risk_analysis=False,
        requires_simulation=False,
    )


# ============================================================
# MAIN LOCAL ANALYZER
# ============================================================

def analyze_locally(
    message: str,
    session_id: str,
) -> Optional[ChatAnalysis]:

    intent = detect_intent(
        message
    )

    # ========================================================
    # COMPARISON
    # ========================================================

    if intent == "WEATHER_COMPARISON":

        if not can_handle_locally(message):
            return None

        result = analyze_comparison_locally(
            message,
            session_id,
        )

        if result is not None:
            return result

        return None

    # ========================================================
    # WHAT-IF
    # ========================================================

    if intent == "WHAT_IF_SCENARIO":

        if not can_handle_locally(message):
            return None

        result = analyze_what_if_locally(
            message,
            session_id,
        )

        if result is not None:
            return result

        return None

    # ========================================================
    # OTHER INTENTS
    # ========================================================

    if not can_handle_locally(message):
        return None

    # ========================================================
    # LOCATION
    # ========================================================

    location_name, city_data = (
        detect_location_with_database(
            message
        )
    )

    # Do not guess

    if location_name is None:
        return None

    location = Location(
        name=location_name,
        latitude=(
            city_data["latitude"]
            if city_data
            else None
        ),
        longitude=(
            city_data["longitude"]
            if city_data
            else None
        ),
    )

    # ========================================================
    # TIME
    # ========================================================

    time_info = detect_time(
        message
    )

    # ========================================================
    # PARAMETERS
    # ========================================================

    parameters = Parameters(
        rainfall_change_mm=None,
        wind_speed_kmh=None,
        target_rainfall_mm=None,
    )

    # ========================================================
    # FLAGS
    # ========================================================

    requires_weather_data = True

    requires_risk_analysis = (
        intent == "WEATHER_RISK"
    )

    requires_simulation = False

    # ========================================================
    # RESULT
    # ========================================================

    return ChatAnalysis(
        message=message,
        intent=intent,
        location=location,
        comparison_location=None,
        time=time_info,
        language=detect_language(message),
        parameters=parameters,
        requires_weather_data=requires_weather_data,
        requires_risk_analysis=requires_risk_analysis,
        requires_simulation=requires_simulation,
    )