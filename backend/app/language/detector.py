import re

def detect_language(text: str) -> str:
    if not text:
        return "en"


    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta"

    if re.search(r"[\u0C00-\u0C7F]", text):
        return "te"

    if re.search(r"[\u0D00-\u0D7F]", text):
        return "ml"

    if re.search(r"[\u0C80-\u0CFF]", text):
        return "kn"

    if re.search(r"[\u0900-\u097F]", text):
        return "hi"

    return "en"

