import random
from modules.phrase_lookup import load_phrases


def generate_quiz(language, category, num_questions=3):
    phrases = load_phrases()
    language = language.lower()
    category = category.lower()

    if language not in phrases or category not in phrases[language]:
        return None

    items = phrases[language][category]

    if len(items) < 2:
        return None

    # Collect wrong options from SAME category across ALL languages
    same_category_translations = []
    for lang in phrases:
        if category in phrases[lang]:
            for i in phrases[lang][category]:
                same_category_translations.append(i["translation"])
    same_category_translations = list(set(same_category_translations))

    questions = []
    selected = random.sample(items, min(num_questions, len(items)))

    for item in selected:
        correct = item["translation"]
        wrong_pool = [t for t in same_category_translations if t != correct]

        # If still not enough, pull from other categories as last resort
        if len(wrong_pool) < 3:
            for lang in phrases:
                for cat in phrases[lang]:
                    for i in phrases[lang][cat]:
                        if i["translation"] != correct and i["translation"] not in wrong_pool:
                            wrong_pool.append(i["translation"])

        if len(wrong_pool) < 3:
            return None

        wrong_options = random.sample(wrong_pool, 3)
        options = wrong_options + [correct]
        random.shuffle(options)

        questions.append({
            "phrase": item["phrase"],
            "romanized": item.get("romanized", ""),
            "correct": correct,
            "options": options
        })

    return questions
