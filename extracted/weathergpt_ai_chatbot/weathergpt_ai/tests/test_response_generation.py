from app.ai.gemini import generate_response
from app.models.schemas import ChatAnalysis, Location, TimeInfo


def test_generate_weather_response():

    analysis = ChatAnalysis(
        message="What's the weather in Chennai?",
        intent="CURRENT_WEATHER",
        location=Location(name="Chennai"),
        time=TimeInfo(),
        language="en",
        requires_weather_data=True,
        requires_risk_analysis=False,
        requires_simulation=False,
    )

    weather_data = {
        "location": "Chennai",
        "temperature": 31,
        "humidity": 72,
        "rain_probability": 60,
        "wind_speed": 18,
        "condition": "Cloudy",
    }

    response = generate_response(
        user_message="What's the weather in Chennai?",
        analysis=analysis,
        weather_data=weather_data,
    )

    assert response
    assert isinstance(response, str)