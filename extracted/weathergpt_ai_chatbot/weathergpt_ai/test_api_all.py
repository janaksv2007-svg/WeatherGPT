import requests
import json

BASE_URL = "http://127.0.0.1:8000"
CHAT_URL = f"{BASE_URL}/chat"


def test_chat(session_id, message):
    print("\n" + "=" * 80)
    print(f"SESSION : {session_id}")
    print(f"USER    : {message}")
    print("=" * 80)

    payload = {
        "session_id": session_id,
        "message": message
    }

    try:
        response = requests.post(
            CHAT_URL,
            json=payload,
            timeout=30
        )

        print(f"HTTP STATUS: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            print("\nANALYSIS:")
            print(json.dumps(
                data.get("analysis"),
                indent=2,
                ensure_ascii=False
            ))

            print("\nBOT RESPONSE:")
            print(data.get("response"))

        else:
            print("\nERROR:")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to FastAPI server.")
        print("Make sure the server is running:")
        print("python -m uvicorn app.main:app --reload")

    except requests.exceptions.Timeout:
        print("\nERROR: Request timed out.")

    except Exception as e:
        print(f"\nERROR: {e}")


# ============================================================
# 1. CURRENT WEATHER
# ============================================================

test_chat(
    "session-current",
    "What's the weather in Chennai?"
)


# ============================================================
# 2. DAILY FORECAST
# ============================================================

test_chat(
    "session-forecast",
    "What's the weather in Chennai tomorrow?"
)


# ============================================================
# 3. HOURLY FORECAST
# ============================================================

test_chat(
    "session-hourly",
    "Give me the hourly forecast for Chennai."
)


# ============================================================
# 4. RAIN FORECAST
# ============================================================

test_chat(
    "session-rain",
    "Will it rain in Mumbai today?"
)


# ============================================================
# 5. TEMPERATURE
# ============================================================

test_chat(
    "session-temperature",
    "What is the temperature in Delhi?"
)


# ============================================================
# 6. WIND
# ============================================================

test_chat(
    "session-wind",
    "What is the wind speed in Chennai?"
)


# ============================================================
# 7. HUMIDITY
# ============================================================

test_chat(
    "session-humidity",
    "What is the humidity in Chennai?"
)


# ============================================================
# 8. WEATHER COMPARISON
# ============================================================

test_chat(
    "session-comparison",
    "Compare the weather in Chennai and Mumbai."
)


# ============================================================
# 9. TRAVEL WEATHER
# ============================================================

test_chat(
    "session-travel",
    "Is Chennai safe for travel this weekend?"
)


# ============================================================
# 10. OUTDOOR ACTIVITY
# ============================================================

test_chat(
    "session-outdoor",
    "Is it good to go outside in Chennai today?"
)


# ============================================================
# 11. WEATHER RISK
# ============================================================

test_chat(
    "session-risk",
    "What is the weather risk in Chennai?"
)


# ============================================================
# 12. WHAT-IF RAINFALL
# ============================================================

test_chat(
    "session-whatif-rain",
    "What if rainfall increases to 100 mm?"
)


# ============================================================
# 13. WHAT-IF WIND
# ============================================================

test_chat(
    "session-whatif-wind",
    "What if wind speed increases to 60 km/h?"
)


# ============================================================
# 14. FOLLOW-UP / MEMORY
# ============================================================

test_chat(
    "session-memory",
    "What's the weather in Chennai?"
)

test_chat(
    "session-memory",
    "What about tomorrow?"
)


# ============================================================
# 15. FOLLOW-UP WITH TIME
# ============================================================

test_chat(
    "session-memory-time",
    "What's the weather in Mumbai?"
)

test_chat(
    "session-memory-time",
    "What about tomorrow evening?"
)


# ============================================================
# 16. TAMIL
# ============================================================

test_chat(
    "session-tamil",
    "சென்னையில் நாளைக்கு மழை பெய்யுமா?"
)


# ============================================================
# 17. HINDI
# ============================================================

test_chat(
    "session-hindi",
    "क्या दिल्ली में आज बारिश होगी?"
)


# ============================================================
# 18. TELUGU
# ============================================================

test_chat(
    "session-telugu",
    "చెన్నైలో ఈరోజు వర్షం పడుతుందా?"
)


# ============================================================
# 19. MALAYALAM
# ============================================================

test_chat(
    "session-malayalam",
    "ചെന്നൈയിൽ ഇന്ന് മഴ പെയ്യുമോ?"
)


# ============================================================
# 20. KANNADA
# ============================================================

test_chat(
    "session-kannada",
    "ಚೆನ್ನೈನಲ್ಲಿ ಇಂದು ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?"
)


# ============================================================
# 21. COMPLEX QUERY
# ============================================================

test_chat(
    "session-complex",
    "What's the weather in Chennai tomorrow evening and "
    "will it be safe for outdoor activities?"
)


print("\n")
print("=" * 80)
print("ALL API TESTS COMPLETED")
print("=" * 80)