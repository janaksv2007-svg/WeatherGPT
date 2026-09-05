from app.location.multilingual_database import (
    initialize_database,
    insert_alias,
)


CITY_ALIASES = [
    # Tamil
    ("சென்னை", "Chennai", "ta"),
    ("மும்பை", "Mumbai", "ta"),
    ("டெல்லி", "Delhi", "ta"),
    ("கோயம்புத்தூர்", "Coimbatore", "ta"),
    ("மதுரை", "Madurai", "ta"),
    ("பெங்களூரு", "Bengaluru", "ta"),
    ("ஹைதராபாத்", "Hyderabad", "ta"),

    # Hindi
    ("चेन्नई", "Chennai", "hi"),
    ("मुंबई", "Mumbai", "hi"),
    ("दिल्ली", "Delhi", "hi"),
    ("कोयंबटूर", "Coimbatore", "hi"),
    ("मदुरै", "Madurai", "hi"),
    ("बेंगलुरु", "Bengaluru", "hi"),
    ("हैदराबाद", "Hyderabad", "hi"),

    # Telugu
    ("చెన్నై", "Chennai", "te"),
    ("ముంబై", "Mumbai", "te"),
    ("ఢిల్లీ", "Delhi", "te"),
    ("కోయంబత్తూరు", "Coimbatore", "te"),
    ("మధురై", "Madurai", "te"),
    ("బెంగళూరు", "Bengaluru", "te"),
    ("హైదరాబాద్", "Hyderabad", "te"),

    # Malayalam
    ("ചെന്നൈ", "Chennai", "ml"),
    ("മുംബൈ", "Mumbai", "ml"),
    ("ഡൽഹി", "Delhi", "ml"),
    ("കോയമ്പത്തൂർ", "Coimbatore", "ml"),
    ("മധുരൈ", "Madurai", "ml"),
    ("ബെംഗളൂരു", "Bengaluru", "ml"),
    ("ഹൈദരാബാദ്", "Hyderabad", "ml"),

    # Kannada
    ("ಚೆನ್ನೈ", "Chennai", "kn"),
    ("ಮುಂಬೈ", "Mumbai", "kn"),
    ("ದೆಹಲಿ", "Delhi", "kn"),
    ("ಕೊಯಮತ್ತೂರು", "Coimbatore", "kn"),
    ("ಮದುರೈ", "Madurai", "kn"),
    ("ಬೆಂಗಳೂರು", "Bengaluru", "kn"),
    ("ಹೈದರಾಬಾದ್", "Hyderabad", "kn"),
]


initialize_database()

for alias, canonical_name, language in CITY_ALIASES:
    insert_alias(alias, canonical_name, language)

print(f"Inserted {len(CITY_ALIASES)} multilingual city aliases.")