from app.chat.chatbot import analyze_chat


def test_current_weather():
    result = analyze_chat(
        "What's the weather in Chennai?",
        "test_current"
    )

    assert result is not None
    assert result.intent == "CURRENT_WEATHER"
    assert result.location.name == "Chennai"
    assert result.requires_weather_data is True


def test_follow_up_tomorrow():
    session_id = "test_follow_up"

    # First message establishes the location
    first = analyze_chat(
        "What's the weather in Chennai?",
        session_id
    )

    assert first is not None
    assert first.location.name == "Chennai"

    # Follow-up should remember Chennai
    second = analyze_chat(
        "What about tomorrow?",
        session_id
    )

    assert second is not None
    assert second.location.name == "Chennai"
    assert second.time.date == "tomorrow"
    assert second.intent == "DAILY_FORECAST"
    assert second.requires_weather_data is True