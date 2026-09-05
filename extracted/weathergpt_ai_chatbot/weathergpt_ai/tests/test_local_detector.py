from app.intent.local_detector import analyze_locally


def test_current_weather():
    result = analyze_locally(
        "What's the weather in Chennai?",
        "test123"
    )

    assert result is not None
    assert result.intent == "CURRENT_WEATHER"
    assert result.location.name == "Chennai"


def test_rain_forecast():
    result = analyze_locally(
        "Will it rain tomorrow in Chennai?",
        "test123"
    )

    assert result is not None
    assert result.intent == "RAIN_FORECAST"
    assert result.location.name == "Chennai"
    assert result.time.date == "tomorrow"


def test_temperature():
    result = analyze_locally(
        "What is the temperature in Bangalore?",
        "test123"
    )

    assert result is not None
    assert result.intent == "TEMPERATURE"
    assert result.location.name == "Bangalore"


def test_wind():
    result = analyze_locally(
        "How windy is it in Mumbai?",
        "test123"
    )

    assert result is not None
    assert result.intent == "WIND"
    assert result.location.name == "Mumbai"


def test_complex_query_goes_to_gemini():
    result = analyze_locally(
        "Is it safe to travel tomorrow evening in Chennai?",
        "test123"
    )

    assert result is None
    