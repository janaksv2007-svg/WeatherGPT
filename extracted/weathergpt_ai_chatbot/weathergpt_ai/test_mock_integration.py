from app.chat.chatbot import analyze_chat
from app.ai.gemini import generate_response

from app.mock.data import (
    MOCK_WEATHER_DATA,
    MOCK_RISK_DATA,
    MOCK_SIMULATION_DATA,
)


MESSAGE = "What if rainfall increases by 75 mm in Chennai?"
SESSION_ID = "demo-session"


print("\n==============================")
print("STEP 1: USER MESSAGE")
print("==============================")

print(MESSAGE)


print("\n==============================")
print("STEP 2: MEMBER 1 ANALYSIS")
print("==============================")

analysis = analyze_chat(
    message=MESSAGE,
    session_id=SESSION_ID,
)

print(analysis.model_dump_json(indent=2))


print("\n==============================")
print("STEP 3: MOCK MEMBER 2 WEATHER")
print("==============================")

print(MOCK_WEATHER_DATA)


print("\n==============================")
print("STEP 4: MOCK MEMBER 3 RISK")
print("==============================")

print(MOCK_RISK_DATA)


print("\n==============================")
print("STEP 5: MOCK SIMULATION")
print("==============================")

print(MOCK_SIMULATION_DATA)


print("\n==============================")
print("STEP 6: GEMINI FINAL RESPONSE")
print("==============================")

try:

    response = generate_response(
        user_message=MESSAGE,
        analysis=analysis,
        weather_data=MOCK_WEATHER_DATA,
        risk_data=MOCK_RISK_DATA,
        simulation_data=MOCK_SIMULATION_DATA,
    )

    print(response)

except Exception as e:

    print("Gemini is currently unavailable.")
    print("The Member 1 analysis and mock integration are working.")
    print(f"Gemini error: {e}")