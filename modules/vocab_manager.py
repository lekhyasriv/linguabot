import os
import pandas as pd


VOCAB_COLUMNS = [
    "language",
    "word",
    "romanized",
    "meaning",
    "category",
    "difficulty",
    "example",
    "example_translation"
]


def load_vocabulary():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "vocabulary.csv")

    if not os.path.exists(path):
        return pd.DataFrame(columns=VOCAB_COLUMNS)

    return pd.read_csv(path)


def get_vocabulary(language, category=None, difficulty=None):
    vocab = load_vocabulary()

    if vocab.empty:
        return vocab

    language = language.lower()
    filtered = vocab[vocab["language"].str.lower() == language]

    if category and category != "All":
        filtered = filtered[
            filtered["category"].str.lower() == category.lower()
        ]

    if difficulty and difficulty != "All":
        filtered = filtered[
            filtered["difficulty"].str.lower() == difficulty.lower()
        ]

    return filtered.reset_index(drop=True)


def get_vocab_categories(language):
    vocab = get_vocabulary(language)

    if vocab.empty:
        return []

    return sorted(vocab["category"].dropna().unique().tolist())


def get_vocab_difficulties(language):
    vocab = get_vocabulary(language)

    if vocab.empty:
        return []

    return sorted(vocab["difficulty"].dropna().unique().tolist())


def search_vocabulary(language, query):
    vocab = get_vocabulary(language)

    if vocab.empty or not query.strip():
        return vocab.iloc[0:0]

    query = query.lower().strip()

    mask = (
        vocab["word"].astype(str).str.lower().str.contains(query, na=False)
        | vocab["romanized"].astype(str).str.lower().str.contains(query, na=False)
        | vocab["meaning"].astype(str).str.lower().str.contains(query, na=False)
        | vocab["example"].astype(str).str.lower().str.contains(query, na=False)
        | vocab["example_translation"].astype(str).str.lower().str.contains(query, na=False)
    )

    return vocab[mask].reset_index(drop=True)
