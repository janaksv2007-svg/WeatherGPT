from app.chat.chatbot import chat_response


def run_test(title, message, session_id, weather_data=None, risk_data=None, simulation_data=None):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print("USER:", message)

    try:
        result = chat_response(
            message,
            session_id,
            weather_data=weather_data,
            risk_data=risk_data,
            simulation_data=simulation_data,
        )

        analysis = result["analysis"]

        print("INTENT:", analysis["intent"])
        print("LOCATION:", analysis["location"])
        print("TIME:", analysis["time"])
        print("LANGUAGE:", analysis["language"])
        print("WEATHER DATA:", analysis["requires_weather_data"])
        print("RISK ANALYSIS:", analysis["requires_risk_analysis"])
        print("SIMULATION:", analysis["requires_simulation"])

        print("\nAI RESPONSE:")
        print(result["response"])

    except Exception as error:
        print("❌ ERROR:", error)


# ---------------------------------------------------------
# TEST DATA
# ---------------------------------------------------------

chennai_weather = {
    "temperature": 29,
    "humidity": 82,
    "rainfall_mm": 45,
    "wind_speed_kmh": 22,
    "condition": "Heavy Rain",
}

mumbai_weather = {
    "temperature": 30,
    "humidity": 78,
    "rainfall_mm": 20,
    "wind_speed_kmh": 18,
    "condition": "Cloudy",
}

chennai_risk = {
    "risk_score": 72,
    "risk_level": "HIGH",
    "primary_risk": "Flooding",
}

chennai_simulation = {
    "scenario": "Rainfall increases to 100 mm",
    "baseline_risk": 72,
    "simulated_risk": 88,
    "risk_change": 16,
}


# ---------------------------------------------------------
# 1. CURRENT WEATHER
# ---------------------------------------------------------

run_test(
    "TEST 1 - CURRENT WEATHER",
    "What is the weather in Chennai?",
    "test_current",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 2. DAILY FORECAST
# ---------------------------------------------------------

run_test(
    "TEST 2 - DAILY FORECAST",
    "What will the weather be in Chennai tomorrow?",
    "test_daily",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 3. RAIN FORECAST
# ---------------------------------------------------------

run_test(
    "TEST 3 - RAIN FORECAST",
    "Will it rain in Mumbai tomorrow?",
    "test_rain",
    weather_data=mumbai_weather,
)


# ---------------------------------------------------------
# 4. WIND
# ---------------------------------------------------------

run_test(
    "TEST 4 - WIND",
    "What is the wind speed in Chennai?",
    "test_wind",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 5. HUMIDITY
# ---------------------------------------------------------

run_test(
    "TEST 5 - HUMIDITY",
    "What is the humidity in Chennai?",
    "test_humidity",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 6. TEMPERATURE
# ---------------------------------------------------------

run_test(
    "TEST 6 - TEMPERATURE",
    "What is the temperature in Chennai?",
    "test_temperature",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 7. WEATHER COMPARISON
# ---------------------------------------------------------

comparison_weather = {
    "Chennai": chennai_weather,
    "Mumbai": mumbai_weather,
}

run_test(
    "TEST 7 - WEATHER COMPARISON",
    "Compare Chennai and Mumbai weather",
    "test_comparison",
    weather_data=comparison_weather,
)


# ---------------------------------------------------------
# 8. WEATHER RISK
# ---------------------------------------------------------

run_test(
    "TEST 8 - WEATHER RISK",
    "What is the weather risk in Chennai?",
    "test_risk",
    weather_data=chennai_weather,
    risk_data=chennai_risk,
)


# ---------------------------------------------------------
# 9. WHAT-IF SIMULATION
# ---------------------------------------------------------

run_test(
    "TEST 9 - WHAT-IF SIMULATION",
    "What if rainfall increases to 100 mm in Chennai?",
    "test_simulation",
    weather_data=chennai_weather,
    risk_data=chennai_risk,
    simulation_data=chennai_simulation,
)


# ---------------------------------------------------------
# 10. TRAVEL WEATHER
# ---------------------------------------------------------

run_test(
    "TEST 10 - TRAVEL WEATHER",
    "Is Chennai safe for travel this weekend?",
    "test_travel",
    weather_data=chennai_weather,
    risk_data=chennai_risk,
)


# ---------------------------------------------------------
# 11. OUTDOOR ACTIVITY
# ---------------------------------------------------------

run_test(
    "TEST 11 - OUTDOOR ACTIVITY",
    "Is it good to go outside in Chennai today?",
    "test_outdoor",
    weather_data=chennai_weather,
    risk_data=chennai_risk,
)


# ---------------------------------------------------------
# 12. TAMIL
# ---------------------------------------------------------

run_test(
    "TEST 12 - TAMIL",
    "சென்னையில் இன்று மழை பெய்யுமா?",
    "test_tamil",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 13. HINDI
# ---------------------------------------------------------

run_test(
    "TEST 13 - HINDI",
    "क्या चेन्नई में आज बारिश होगी?",
    "test_hindi",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 14. TELUGU
# ---------------------------------------------------------

run_test(
    "TEST 14 - TELUGU",
    "చెన్నైలో ఈరోజు వర్షం పడుతుందా?",
    "test_telugu",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 15. MALAYALAM
# ---------------------------------------------------------

run_test(
    "TEST 15 - MALAYALAM",
    "ചെന്നൈയിൽ ഇന്ന് മഴ പെയ്യുമോ?",
    "test_malayalam",
    weather_data=chennai_weather,
)


# ---------------------------------------------------------
# 16. KANNADA
# ---------------------------------------------------------

run_test(
    "TEST 16 - KANNADA",
    "ಚೆನ್ನೈನಲ್ಲಿ ಇಂದು ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?",
    "test_kannada",
    weather_data=chennai_weather,
)


print("\n")
print("=" * 70)
print("ALL MEMBER 1 TESTS COMPLETED")
print("=" * 70)