import requests


BASE_URL = "http://127.0.0.1:8000"


def test_current_weather():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_current",
            "message": "What is the weather in Chennai?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_tomorrow_forecast():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_tomorrow",
            "message": "What will the weather be in Chennai tomorrow?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_rain_forecast():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_rain",
            "message": "Will it rain in Chennai?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_temperature():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_temperature",
            "message": "What is the temperature in Chennai?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_wind():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_wind",
            "message": "What is the wind speed in Chennai?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_comparison():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_comparison",
            "message": "Compare the weather in Chennai and Mumbai."
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data


def test_what_if():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": "pytest_whatif",
            "message": "What if rainfall increases to 100 mm?"
        },
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()

    assert "analysis" in data
    assert "response" in data