"""
Member 1 AI Module (Gemini LLM Integration)
Provides natural language intent analysis and conversational response generation using Google Gemini.
"""
import time
import json
from typing import Optional, Dict, Any

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.ai.prompts import SYSTEM_PROMPT, RESPONSE_SYSTEM_PROMPT
from app.models.schemas import ChatAnalysis
from app.language.supported import LANGUAGE_NAMES

# Initialize google.generativeai SDK
try:
    import google.generativeai as genai
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        # Use gemini-3.6-flash model
        model_name = GEMINI_MODEL if GEMINI_MODEL else "gemini-3.6-flash"
        model = genai.GenerativeModel(model_name)
    else:
        model = None
except Exception as _err:
    print(f"[Gemini Init Warning] { _err }")
    genai = None
    model = None


import re


def analyze_message(
    message: str,
    session_id: str = "default",
    language: str = "en",
) -> ChatAnalysis:
    """
    Analyze user message using Gemini LLM.
    """
    if model is None:
        raise RuntimeError("Gemini API client is not initialized or GEMINI_API_KEY is missing.")

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

Analyze the user's message and return a JSON object with intent, location, time, language, parameters, requires_weather_data, requires_risk_analysis, and requires_simulation.
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:].rstrip("`").strip()
        elif text.startswith("```"):
            text = text[3:].rstrip("`").strip()

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)

        return ChatAnalysis.model_validate_json(text)
    except Exception as e:
        print(f"[Gemini Analysis Error] {e}")
        raise e



def generate_response(
    user_message: str,
    analysis: ChatAnalysis,
    weather_data: Optional[dict] = None,
    risk_data: Optional[dict] = None,
    simulation_data: Optional[dict] = None,
    comparison_weather: Optional[dict] = None,
    climate_data: Optional[dict] = None,
    language: str = "en",
) -> str:
    """
    Generate conversational answer using Gemini LLM.
    """
    if model is None:
        raise RuntimeError("Gemini API client is not initialized or GEMINI_API_KEY is missing.")

    lang_code = language if language else (getattr(analysis, "language", "en") or "en")
    if re.search(r"[\u0B80-\u0BFF]", user_message):
        lang_code = "ta"
    lang_name = LANGUAGE_NAMES.get(lang_code, "English")

    prompt = f"""
{RESPONSE_SYSTEM_PROMPT}

USER MESSAGE:
{user_message}

TARGET RESPONSE LANGUAGE:
{lang_name} ({lang_code})

STRUCTURED ANALYSIS:
{analysis}

PRIMARY WEATHER DATA:
{weather_data}

COMPARISON WEATHER DATA:
{comparison_weather}

RISK DATA:
{risk_data}

SIMULATION DATA:
{simulation_data}

HISTORICAL CLIMATE DATA:
{climate_data}

Answer the user's question directly, clearly and concisely using the provided data.
IMPORTANT: If TARGET RESPONSE LANGUAGE is Tamil ('ta') or Tamil script is detected, write the entire response in natural Tamil script (தமிழ்).
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Generate Error] {e}")
        raise e