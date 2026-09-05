from app.intent.local_detector import analyze_locally


def test_compare_weather():
    result = analyze_locally(
        "Compare the weather in Chennai and Mumbai.",
        "test"
    )

    assert result is not None
    assert result.intent == "WEATHER_COMPARISON"
    assert result.location.name == "Chennai"
    assert result.comparison_location.name == "Mumbai"
    assert result.requires_weather_data is True
    assert result.requires_risk_analysis is False
    assert result.requires_simulation is False


def test_vs_weather():
    result = analyze_locally(
        "Chennai vs Mumbai",
        "test"
    )

    assert result is not None
    assert result.intent == "WEATHER_COMPARISON"
    assert result.location.name == "Chennai"
    assert result.comparison_location.name == "Mumbai"


def test_difference_weather():
    result = analyze_locally(
        "What is the difference between Chennai and Mumbai weather?",
        "test"
    )

    assert result is not None
    assert result.intent == "WEATHER_COMPARISON"
    assert result.location.name == "Chennai"
    assert result.comparison_location.name == "Mumbai"