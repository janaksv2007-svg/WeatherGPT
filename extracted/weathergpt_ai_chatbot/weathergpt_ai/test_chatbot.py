import requests
import json


API_URL = "http://127.0.0.1:8000/chat"

session_id = "integration_test_001"


test_messages = [
    "What is the weather in Chennai?",
    "What about tomorrow?",
    "Will it rain in Mumbai after 6 PM?",
    "Is Delhi safe for travel this weekend?",
    "What happens if rainfall increases to 100 mm?",
    "What if wind speed increases to 60 km/h?",
    "Compare Chennai and Mumbai weather.",
    "சென்னையில் நாளைக்கு மழை பெய்யுமா?",
    "मुंबई में आज बारिश होगी?",
    "Hello"
]


def test_message(message):
    print("\n" + "=" * 70)
    print("USER:", message)
    print("=" * 70)

    payload = {
        "message": message,
        "session_id": session_id
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("ERROR:")
            print(response.text)
            return

        data = response.json()

        print("\n--- ANALYSIS ---")
        print(
            json.dumps(
                data.get("analysis"),
                indent=2,
                ensure_ascii=False
            )
        )

        print("\n--- AI RESPONSE ---")
        print(data.get("response"))

        if "weather_data" in data:
            print("\n--- WEATHER DATA ---")
            print(
                json.dumps(
                    data["weather_data"],
                    indent=2,
                    ensure_ascii=False
                )
            )

    except requests.exceptions.ConnectionError:
        print(
            "\nERROR: Could not connect to FastAPI."
            "\nMake sure the server is running:"
            "\n"
            "\nuvicorn app.main:app --reload"
        )

    except Exception as error:
        print("\nERROR:", error)


if __name__ == "__main__":

    print("=" * 70)
    print("WeatherGPT - Member 1 Integration Test")
    print("=" * 70)

    for message in test_messages:
        test_message(message)

    print("\n" + "=" * 70)
    print("TESTING COMPLETED")
    print("=" * 70)