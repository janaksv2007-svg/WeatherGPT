from app.language.detector import detect_language

tests = [
("What is the weather in Chennai?", "en"),
("சென்னையில் நாளைக்கு மழை பெய்யுமா?", "ta"),
("कल चेन्नई में बारिश होगी?", "hi"),
("చెన్నైలో రేపు వర్షం పడుతుందా?", "te"),
("ചെന്നൈയിൽ നാളെ മഴ പെയ്യുമോ?", "ml"),
("ಚೆನ್ನೈಯಲ್ಲಿ ನಾಳೆ ಮಳೆ ಬರುತ್ತದೆಯೇ?", "kn")
]

for message, expected in tests:
    result = detect_language(message)


    print("Message:", message)
    print("Detected:", result)
    print("Expected:", expected)
    print("PASS" if result == expected else "FAIL")
    print()

