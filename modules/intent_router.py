import re

INTENT_PATTERNS = {
    "quiz": [
        r"quiz", r"test me", r"question", r"practice test",
        r"ask me", r"examine me"
    ],
    "phrase": [
        r"phrase", r"how (do i|to) say", r"what is .* in",
        r"show me", r"give me", r"greetings", r"classroom"
    ],
    "vocabulary": [
        r"vocab", r"word", r"meaning", r"define",
        r"what does .* mean", r"translate"
    ],
    "grammar": [
        r"grammar", r"correct my", r"is this correct",
        r"check my", r"fix my", r"mistake"
    ],
    "conversation": [
        r"chat", r"talk", r"conversation", r"speak",
        r"let's practice", r"practice with me"
    ]
}

SUPPORTED_LANGUAGES = [
    "japanese", "french", "german",
    "korean", "chinese", "russian", "italian"
]


def detect_language(text):
    text = text.lower()
    for lang in SUPPORTED_LANGUAGES:
        if lang in text:
            return lang
    return None


def detect_intent(text):
    text = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent
    return "conversation"


def route(user_input):
    intent = detect_intent(user_input)
    language = detect_language(user_input)

    return {
        "intent": intent,
        "language": language,
        "use_api": intent in ["conversation", "grammar"],
        "user_input": user_input
    }
