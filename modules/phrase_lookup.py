import json
import os


def load_phrases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "phrases.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_phrases(language, category):
    phrases = load_phrases()
    language = language.lower()
    category = category.lower()

    if language not in phrases:
        return f"Sorry, {language} is not supported yet."

    if category not in phrases[language]:
        return f"No phrases found for category: {category}"

    result = f"\n📚 {category.upper()} phrases in {language.capitalize()}:\n"
    result += "-" * 40 + "\n"

    for item in phrases[language][category]:
        result += f"🗣  {item['phrase']}\n"
        if item['romanized']:
            result += f"   ({item['romanized']})\n"
        result += f"   ✅ {item['translation']}\n\n"

    return result


def get_supported_languages():
    phrases = load_phrases()
    return list(phrases.keys())


def get_supported_categories(language):
    phrases = load_phrases()
    language = language.lower()
    if language in phrases:
        return list(phrases[language].keys())
    return []
