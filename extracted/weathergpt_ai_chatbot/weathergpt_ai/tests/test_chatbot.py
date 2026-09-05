import requests
import json

URL = "http://127.0.0.1:8000/analyze"

tests = [
    "What's the weather in Chennai?",
    "Will it rain in Mumbai tomorrow?",
    "What is the temperature in Delhi?",
    "How strong is the wind in Bangalore?",
    "What's the humidity in Hyderabad?",
    "Give me the forecast for Chennai tomorrow.",
    "Compare Chennai and Mumbai weather.",
    "What if rainfall increases by 50 mm in Chennai?",
    "What about tomorrow?",
    "How about there?",
]

session_id = "test-session-001"

for i, message in enumerate(tests, start=1):

    print("\n" + "=" * 70)
    print(f"TEST {i}")
    print("=" * 70)

    print("USER:")
    print(message)

    try:
        response = requests.post(
            URL,
            json={
                "message": message,
                "session_id": session_id
            },
            timeout=30
        )

        print("\nSTATUS:")
        print(response.status_code)

        print("\nRESULT:")

        if response.ok:
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to FastAPI.")
        print("Make sure the server is running:")
        print("uvicorn app.main:app --reload")
        break

    except Exception as e:
        print(f"\nERROR: {e}")