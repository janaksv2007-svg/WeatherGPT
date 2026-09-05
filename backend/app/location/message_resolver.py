import re
from typing import Optional

from app.location.resolver import resolve_city
from app.location.multilingual_database import resolve_alias


# ============================================================
# WORDS THAT SHOULD NOT BE TREATED AS CITY NAMES
# ============================================================

IGNORED_WORDS = {
    # Articles
    "a", "an", "the",

    # Verbs / helping verbs
    "is", "are", "am", "was", "were",
    "be", "been", "being",
    "will", "would", "could", "should",
    "can", "may", "might",
    "do", "does", "did",

    # Question words
    "what", "when", "where", "why",
    "how", "which", "who",

    # Weather words
    "weather", "forecast",
    "temperature", "temp",
    "rain", "raining", "rainfall",
    "wind", "winds",
    "humidity",

    # Time words
    "today", "tomorrow", "tonight",
    "morning", "afternoon",
    "evening", "night",
    "weekend", "weekends",
    "week", "weeks",
    "next", "this",

    # Prepositions
    "in", "at", "for", "on",
    "from", "to", "of",
    "with", "about",
    "around", "near",

    # Connectors
    "and", "or",

    # Safety / travel
    "safe", "safety",
    "travel", "trip",

    # Outdoor
    "outside", "outdoor",
    "activity", "activities",

    # Common conversation words
    "please", "tell", "me",
    "give", "show",
    "there", "here",
    "it", "its",
    "my", "your",
    "our", "their",
}


# ============================================================
# TIME PATTERN
# ============================================================

TIME_WORDS_PATTERN = (
    r"\b(today|tomorrow|tonight|morning|afternoon|"
    r"evening|night|this weekend|next week|weekdays?)\b.*$"
)


# ============================================================
# NORMALIZE CITY CANDIDATE
# ============================================================

def normalize_candidate(candidate: str) -> str:
    """
    Clean a possible city name.

    Example:
        "Chennai tomorrow"
        -> "Chennai"

        "Mumbai today"
        -> "Mumbai"
    """

    candidate = candidate.strip()

    candidate = candidate.strip(
        " ,.!?;:()[]{}\"'"
    )

    candidate = re.sub(
        TIME_WORDS_PATTERN,
        "",
        candidate,
        flags=re.IGNORECASE,
    ).strip()

    candidate = candidate.strip(
        " ,.!?;:()[]{}\"'"
    )

    return candidate


# ============================================================
# EXTRACT CITY CANDIDATES FROM ENGLISH SENTENCES
# ============================================================

def extract_city_candidates(message: str) -> list[str]:
    """
    Extract possible city names from English sentences.

    Examples:

        "weather in Chennai"
        -> ["Chennai"]

        "rain in Mumbai tomorrow"
        -> ["Mumbai"]

        "temperature for Delhi"
        -> ["Delhi"]
    """

    patterns = [
        r"\bin\s+([A-Za-z][A-Za-z .'-]{1,50})",
        r"\bat\s+([A-Za-z][A-Za-z .'-]{1,50})",
        r"\bfor\s+([A-Za-z][A-Za-z .'-]{1,50})",
        r"\baround\s+([A-Za-z][A-Za-z .'-]{1,50})",
        r"\bnear\s+([A-Za-z][A-Za-z .'-]{1,50})",
    ]

    candidates = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            message,
            flags=re.IGNORECASE,
        )

        for match in matches:

            candidate = normalize_candidate(match)

            if not candidate:
                continue

            words = candidate.lower().split()

            # Remove weather/time/conversation words
            # accidentally captured after city name.
            while words and words[-1] in IGNORED_WORDS:
                words.pop()

            if not words:
                continue

            candidate = " ".join(words)

            # Avoid accidentally treating a whole sentence
            # as a city.
            if len(words) > 4:
                continue

            candidates.append(candidate)

    # Remove duplicates while preserving order.
    unique_candidates = []

    for candidate in candidates:

        if candidate.lower() not in {
            item.lower()
            for item in unique_candidates
        }:
            unique_candidates.append(candidate)

    return unique_candidates


# ============================================================
# EXTRACT INDIVIDUAL ENGLISH WORDS
# ============================================================

def extract_word_candidates(message: str) -> list[str]:
    """
    Extract individual English words that could potentially
    be city names.

    Example:

        "Chennai weather tomorrow"

        -> ["Chennai"]
    """

    words = re.findall(
        r"[A-Za-z]{2,}",
        message,
    )

    candidates = []

    for word in words:

        normalized = word.lower()

        if normalized in IGNORED_WORDS:
            continue

        if len(normalized) < 3:
            continue

        candidates.append(word)

    return candidates


# ============================================================
# MULTILINGUAL CITY ALIASES
# ============================================================

def resolve_multilingual_location(
    message: str,
) -> Optional[dict]:
    """
    Resolve city names written in Indian languages.

    Handles cases such as:

        சென்னை
        சென்னையில்

        मुंबई
        मुंबई में

        दिल्ली
        दिल्ली में
    """

    # Extract Unicode portions from the message.
    unicode_parts = re.findall(
        r"[^\x00-\x7F]+",
        message,
    )

    for text_part in unicode_parts:

        text_part = text_part.strip()

        if not text_part:
            continue

        # ----------------------------------------------------
        # 1. Try exact alias
        # ----------------------------------------------------

        result = resolve_alias(text_part)

        if result:

            canonical_name = result.get(
                "canonical_name"
            )

            if canonical_name:

                city = resolve_city(
                    canonical_name
                )

                if city is not None:
                    return city

        # ----------------------------------------------------
        # 2. Try individual Unicode words
        # ----------------------------------------------------

        unicode_words = re.findall(
            r"[^\s,!?;:]+",
            text_part,
        )

        for word in unicode_words:

            word = word.strip()

            if not word:
                continue

            # Exact alias
            result = resolve_alias(word)

            if result:

                canonical_name = result.get(
                    "canonical_name"
                )

                if canonical_name:

                    city = resolve_city(
                        canonical_name
                    )

                    if city is not None:
                        return city

            # ------------------------------------------------
            # 3. Handle Tamil grammatical suffixes
            # ------------------------------------------------
            #
            # Example:
            #
            # "சென்னையில்"
            #
            # contains:
            #
            # "சென்னை"
            #
            # Therefore:
            #
            # சென்னையில் -> Chennai
            #
            # ------------------------------------------------

            tamil_aliases = [
                "சென்னை",
                "மும்பை",
                "டெல்லி",
                "கோயம்புத்தூர்",
                "மதுரை",
                "பெங்களூரு",
                "ஹைதராபாத்",
            ]

            for alias_candidate in tamil_aliases:

                if alias_candidate in word:

                    result = resolve_alias(
                        alias_candidate
                    )

                    if result:

                        canonical_name = result.get(
                            "canonical_name"
                        )

                        if canonical_name:

                            city = resolve_city(
                                canonical_name
                            )

                            if city is not None:
                                return city

    return None


# ============================================================
# MAIN LOCATION RESOLVER
# ============================================================

def resolve_location_from_message(
    message: str,
) -> Optional[dict]:
    """
    Resolve a city from a complete user message.

    Supports:

    English:
        "Chennai weather tomorrow"
        "Will it rain in Mumbai?"
        "Is Delhi safe for travel?"

    Hindi:
        "मुंबई में आज बारिश होगी?"

    Tamil:
        "சென்னையில் நாளைக்கு மழை பெய்யுமா?"

    Returns:
        City dictionary if found.
        None if no city can be safely resolved.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not message or not message.strip():
        return None

    # --------------------------------------------------------
    # STEP 1: English city extraction
    # --------------------------------------------------------

    candidates = extract_city_candidates(
        message
    )

    for candidate in candidates:

        city = resolve_city(candidate)

        if city is not None:
            return city

    # --------------------------------------------------------
    # STEP 2: Multilingual city resolution
    # --------------------------------------------------------

    city = resolve_multilingual_location(
        message
    )

    if city is not None:
        return city

    # --------------------------------------------------------
    # STEP 3: Individual English words
    # --------------------------------------------------------

    word_candidates = extract_word_candidates(
        message
    )

    for candidate in word_candidates:

        city = resolve_city(candidate)

        if city is not None:
            return city

    # --------------------------------------------------------
    # STEP 4: Nothing found
    # --------------------------------------------------------

    return None