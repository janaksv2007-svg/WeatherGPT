"""
Member 6 Multilingual Service
Provides language translation mappings for English, Tamil, and Hindi.
"""
import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
TRANSLATIONS_FILE = DATA_DIR / "translations.json"


def get_translations(language: str = "english") -> Dict[str, Any]:
    """
    Fetch dictionary of translated weather terms.
    Language options: 'english', 'tamil', 'hindi' (or 'en', 'ta', 'hi').
    """
    lang_key = language.lower()
    if lang_key in ["en", "english"]:
        lang_key = "english"
    elif lang_key in ["ta", "tamil"]:
        lang_key = "tamil"
    elif lang_key in ["hi", "hindi"]:
        lang_key = "hindi"

    if not TRANSLATIONS_FILE.exists():
        return {}

    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get(lang_key, data.get("english", {}))
    except Exception:
        return {}
