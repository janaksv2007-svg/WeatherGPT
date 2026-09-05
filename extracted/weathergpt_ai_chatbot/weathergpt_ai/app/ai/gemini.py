# app/ai/gemini.py

import time

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.ai.prompts import (
    SYSTEM_PROMPT,
    RESPONSE_SYSTEM_PROMPT,
)
from app.models.schemas import ChatAnalysis
from app.language.supported import LANGUAGE_NAMES


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# ANALYZE USER MESSAGE
# ============================================================

def analyze_message(
    message: str,
    session_id: str = "default",
    language: str = "en",
) -> ChatAnalysis:
    """
    Analyze a user's weather-related message using Gemini.

    Gemini is responsible for:
    - Intent detection
    - Location extraction
    - Time extraction
    - Language awareness
    - Weather requirement detection
    - Risk/simulation requirement detection

    Gemini MUST NOT invent actual weather information.
    """

    language_name = LANGUAGE_NAMES.get(language, "English")

    prompt = f"""
{SYSTEM_PROMPT}

USER MESSAGE:
{message}

SESSION ID:
{session_id}

DETECTED LANGUAGE:
{language_name}

REQUESTED LANGUAGE CODE:
{language}

Analyze the user's message and return the structured result.

IMPORTANT RULES:

1. Set the language field to "{language}".

2. Do NOT translate the user's original message.

3. Extract the location only if the user actually provides
   a recognizable location.

4. If the location is missing, use null.
   NEVER invent or guess a location.

5. Extract the requested time period when possible.

6. Supported time expressions include:
   - today
   - tomorrow
   - tonight
   - morning
   - afternoon
   - evening
   - night
   - weekend
   - next week
   - weekdays
   - in X hours
   - after X PM
   - before X AM

7. Detect comparison requests such as:
   "Compare Chennai and Mumbai"
   "Which is hotter, Chennai or Delhi?"
   "Compare the weather in Mumbai and Bangalore."

8. Detect What-If requests such as:
   "What if rainfall increases to 100 mm?"
   "What if wind speed increases to 60 km/h?"

9. For What-If requests, extract the requested parameter
   and value when available.

10. Do NOT calculate risk yourself.

11. Do NOT invent:
   - temperature
   - rainfall
   - wind speed
   - humidity
   - weather conditions
   - alerts
   - risk scores
   - simulation results

12. Actual weather information will come from the weather API.

13. Actual risk information will come from the risk engine.

14. Actual simulation results will come from the simulation engine.

Return ONLY the structured response matching the ChatAnalysis schema.
"""

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ChatAnalysis,
                ),
            )

            # ------------------------------------------------
            # Preferred: Gemini parsed response
            # ------------------------------------------------

            if response.parsed:
                return response.parsed

            # ------------------------------------------------
            # Fallback: Parse JSON text
            # ------------------------------------------------

            if response.text:
                return ChatAnalysis.model_validate_json(
                    response.text
                )

            raise ValueError(
                "Gemini returned an empty analysis response."
            )

        except Exception as e:

            last_error = e

            error_text = str(e).upper()

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "HIGH DEMAND" in error_text
                or "SERVICE UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE EXHAUSTED" in error_text
                or "TIMEOUT" in error_text
            )

            # ------------------------------------------------
            # Permanent error
            # ------------------------------------------------

            if not is_temporary_error:
                raise

            # ------------------------------------------------
            # Retry temporary errors
            # ------------------------------------------------

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"⚠️ Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    # --------------------------------------------------------
    # All retries failed
    # --------------------------------------------------------

    raise last_error


# ============================================================
# SAFE ANALYSIS SERIALIZATION
# ============================================================

def _serialize_analysis(analysis) -> str:
    """
    Convert ChatAnalysis/Pydantic/dict objects into JSON-like text.

    This prevents errors such as:

        'dict' object has no attribute 'model_dump_json'
    """

    # Pydantic v2
    if hasattr(analysis, "model_dump_json"):

        return analysis.model_dump_json(
            indent=2
        )

    # Pydantic model_dump
    if hasattr(analysis, "model_dump"):

        return str(
            analysis.model_dump()
        )

    # Older Pydantic
    if hasattr(analysis, "dict"):

        return str(
            analysis.dict()
        )

    # Dictionary
    if isinstance(analysis, dict):

        return str(analysis)

    # Final fallback
    return str(analysis)


# ============================================================
# GENERATE FINAL CHATBOT RESPONSE
# ============================================================

def generate_response(
    user_message: str,
    analysis: ChatAnalysis,
    weather_data: dict | None = None,
    risk_data: dict | None = None,
    simulation_data: dict | None = None,
    comparison_weather: dict | None = None,
) -> str:
    """
    Generate the final conversational response.

    Gemini receives structured information from:
    - AI analysis
    - Weather API
    - Risk engine
    - Simulation engine
    - Comparison weather API

    Gemini does NOT calculate weather or risk itself.
    """

    # --------------------------------------------------------
    # Safely serialize analysis
    # --------------------------------------------------------

    analysis_json = _serialize_analysis(
        analysis
    )

    # --------------------------------------------------------
    # Prepare weather data
    # --------------------------------------------------------

    primary_weather = (
        weather_data
        if weather_data is not None
        else "No primary weather data provided."
    )

    # --------------------------------------------------------
    # Prepare comparison data
    # --------------------------------------------------------

    comparison_data = (
        comparison_weather
        if comparison_weather is not None
        else "No comparison weather data provided."
    )

    # --------------------------------------------------------
    # Prepare risk data
    # --------------------------------------------------------

    risk_information = (
        risk_data
        if risk_data is not None
        else "No risk data provided."
    )

    # --------------------------------------------------------
    # Prepare simulation data
    # --------------------------------------------------------

    simulation_information = (
        simulation_data
        if simulation_data is not None
        else "No simulation data provided."
    )

    # ========================================================
    # FINAL GEMINI PROMPT
    # ========================================================

    prompt = f"""
{RESPONSE_SYSTEM_PROMPT}

USER MESSAGE:
{user_message}

STRUCTURED ANALYSIS:
{analysis_json}

PRIMARY WEATHER DATA:
{primary_weather}

COMPARISON WEATHER DATA:
{comparison_data}

RISK DATA:
{risk_information}

SIMULATION DATA:
{simulation_information}


============================================================
IMPORTANT RESPONSE RULES
============================================================

1. Answer the user's actual question directly.

2. Use ONLY information provided in the data above.

3. NEVER invent weather information.

4. NEVER invent:
   - temperature
   - rainfall
   - wind speed
   - humidity
   - weather condition
   - weather alerts
   - risk score
   - risk level
   - simulation result

5. If weather data is unavailable, clearly tell the user
   that weather data is unavailable.

6. If risk data is unavailable, do not create your own
   risk score.

7. If simulation data is unavailable, do not calculate
   a simulated risk yourself.

8. If comparison weather data is provided, compare BOTH
   locations.

9. For comparison requests:
   - Mention both locations.
   - Compare available weather values.
   - Do not ignore the second location.

10. For What-If requests:
    - Explain the scenario using the provided simulation data.
    - Do not calculate a new risk value.

11. If the user's question is conversational, answer naturally.

12. If the user asks a follow-up question, use the supplied
    structured analysis and data to answer it.

13. Keep the response concise but useful.

14. Do not expose internal implementation details.

15. Do not mention Gemini, API calls, schemas, Python,
    backend modules, or internal processing unless the user
    explicitly asks about them.

16. Respond in the requested language.

17. If the requested language is not English and the required
    weather data is available, answer naturally in that language.

18. Never claim that weather information is real-time unless
    the supplied weather data explicitly represents current
    weather.

19. If the user asks for a location that is not available in
    the supplied data, do not guess the weather.

============================================================
TASK
============================================================

Generate the final response to the user.
"""

    # ========================================================
    # GEMINI RETRY LOOP
    # ========================================================

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            # ------------------------------------------------
            # Normal response
            # ------------------------------------------------

            if response.text:

                return response.text.strip()

            raise ValueError(
                "Gemini returned an empty response."
            )

        except Exception as e:

            last_error = e

            error_text = str(e).upper()

            is_temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "HIGH DEMAND" in error_text
                or "SERVICE UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE EXHAUSTED" in error_text
                or "TIMEOUT" in error_text
            )

            # ------------------------------------------------
            # Permanent error
            # ------------------------------------------------

            if not is_temporary_error:
                raise

            # ------------------------------------------------
            # Retry
            # ------------------------------------------------

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"⚠️ Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    # ========================================================
    # ALL RETRIES FAILED
    # ========================================================

    raise last_error