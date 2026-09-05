from app.intent.local_detector import analyze_locally


def test_what_if_rainfall_increase():

    result = analyze_locally(
        "What if rainfall increases by 50mm?",
        "test123"
    )

    assert result is not None

    assert result.intent == "WHAT_IF_SCENARIO"

    assert result.parameters.rainfall_change_mm == 50.0

    assert result.requires_weather_data is True

    assert result.requires_risk_analysis is True

    assert result.requires_simulation is True


def test_what_if_rainfall_decrease():

    result = analyze_locally(
        "What if rainfall decreases by 20mm?",
        "test123"
    )

    assert result is not None

    assert result.intent == "WHAT_IF_SCENARIO"

    assert result.parameters.rainfall_change_mm == -20.0


def test_what_if_with_location():

    result = analyze_locally(
        "What if rainfall increases by 50mm in Chennai?",
        "test123"
    )

    assert result is not None

    assert result.intent == "WHAT_IF_SCENARIO"

    assert result.location.name == "Chennai"

    assert result.parameters.rainfall_change_mm == 50.0


def test_what_if_with_time():

    result = analyze_locally(
        "What if rainfall increases by 50mm tomorrow evening in Chennai?",
        "test123"
    )

    assert result is not None

    assert result.intent == "WHAT_IF_SCENARIO"

    assert result.location.name == "Chennai"

    assert result.time.date == "tomorrow"

    assert result.time.time_period == "evening"

    assert result.parameters.rainfall_change_mm == 50.0