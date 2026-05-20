import streamlit as st
import json
from modules.phrase_lookup import get_phrases, get_supported_languages, get_supported_categories
from modules.quiz_engine import generate_quiz
from modules.intent_router import route
from modules.llm_engine import get_llm_response, check_grammar
from modules.vocab_manager import get_vocabulary, get_vocab_categories, get_vocab_difficulties, search_vocabulary
from textwrap import dedent
st.set_page_config(page_title="LinguaBot", page_icon="🌍", layout="wide")

CATEGORY_ICONS = {
    "greetings": "Greetings",
    "numbers": "Numbers",
    "colors": "Colors",
    "food": "Food",
    "classroom": "Classroom",
    "travel": "Travel",
    "family": "Family",
    "days": "Days"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
            color: #0a2233;
    }

    .stApp {
        background-color: #f0f7fa;
            color: #0a2233;
    }

    section[data-testid="stSidebar"] {
        background-color: #0a2233;
        border-right: none;
    }

    section[data-testid="stSidebar"] * {
        color: #cce8f0 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #1a3a4a !important;
    }

    .page-title {
        font-size: 28px;
        font-weight: 600;
        color: #0a2233;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .page-subtitle {
        font-size: 14px;
        color: #6a9aaa;
        margin-bottom: 32px;
        font-weight: 400;
    }

    .phrase-card {
        background: white;
        border: 1px solid #d0eaf2;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 8px 0;
        transition: box-shadow 0.2s;
    }

    .phrase-card:hover {
        box-shadow: 0 4px 20px rgba(14, 116, 144, 0.10);
        border-color: #0e7490;
    }

    .phrase-original {
        font-size: 26px;
        font-weight: 600;
        color: #0a2233;
        letter-spacing: -0.3px;
    }

    .phrase-romanized {
        font-size: 13px;
        color: #7ab8c8;
        margin-top: 4px;
        font-style: italic;
    }

    .phrase-divider {
        border: none;
        border-top: 1px solid #e8f4f8;
        margin: 12px 0;
    }

    .phrase-english {
        font-size: 15px;
        color: #0e7490;
        font-weight: 500;
    }

    .quiz-phrase-box {
        background: white;
        border: 1px solid #d0eaf2;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
    }

    .quiz-phrase-text {
        font-size: 48px;
        font-weight: 700;
        color: #0a2233;
        letter-spacing: -1px;
    }

    .quiz-phrase-roman {
        font-size: 16px;
        color: #7ab8c8;
        margin-top: 8px;
        font-style: italic;
    }

    .score-card {
        background: white;
        border: 1px solid #d0eaf2;
        border-radius: 16px;
        padding: 48px;
        text-align: center;
    }

    .score-number {
        font-size: 64px;
        font-weight: 700;
        color: #0a2233;
        letter-spacing: -2px;
    }

    .score-label {
        font-size: 16px;
        color: #6a9aaa;
        margin-top: 8px;
    }

    .score-percent {
        font-size: 20px;
        font-weight: 600;
        color: #0e7490;
        margin-top: 12px;
    }

    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 14px;
        border: 1px solid #b0d8e8;
        background: white;
        color: #0a2233;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background: #0e7490;
        color: white;
        border-color: #0e7490;
    }

    .stButton > button[kind="primary"] {
        background: #0e7490;
        color: white;
        border-color: #0e7490;
    }

    .stButton > button[kind="primary"]:hover {
        background: #0a5f78;
    }

    div[data-testid="stProgress"] > div {
        background-color: #0e7490 !important;
    }

    /* Quiz options */
div[role="radiogroup"] > label {
    background-color: white !important;
    border: 2px solid #d0eaf2 !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #0a2233 !important;
    font-weight: 500;
}

/* Hover */
div[role="radiogroup"] > label:hover {
    border-color: #0e7490 !important;
    background-color: #f2fbff !important;
}

/* Selected option */
div[role="radiogroup"] > label:has(input:checked) {
    border-color: #0e7490 !important;
    background-color: #dff4fb !important;
    box-shadow: 0 0 0 1px #0e7490;
}

/* Text inside selected */
div[role="radiogroup"] > label:has(input:checked) p {
    color: #0a2233 !important;
    font-weight: 600;
}

/* Radio circle */
div[role="radiogroup"] svg {
    fill: #0e7490 !important;
}
/* Force visible radio text */
div[role="radiogroup"] label div {
    color: #0a2233 !important;
    opacity: 1 !important;
}

/* Selected text */
div[role="radiogroup"] label:has(input:checked) div {
    color: #0a2233 !important;
    font-weight: 600 !important;
}

    .sidebar-brand {
        font-size: 20px;
        font-weight: 600;
        color: white;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }

    .sidebar-tagline {
        font-size: 12px;
        color: #4a7a8a;
        margin-bottom: 24px;
    }

    .lang-badge {
        display: inline-block;
        background: #0e7490;
        color: #cce8f0;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 999px;
        margin: 2px;
    }

    .category-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        color: #6a9aaa;
        margin-bottom: 16px;
        text-transform: uppercase;
    }

    .stChatMessage p {
        color: #0a2233 !important;
    }

    .stChatMessage {
        color: #0a2233 !important;
    }

    [data-testid="stChatMessageContent"] p {
        color: #0a2233 !important;
    }

    [data-testid="stChatMessageContent"] {
        color: #0a2233 !important;
    }

    .stMarkdown p {
        color: #0a2233 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ─── START SCREEN ───────────────────────────────────────────────
# ─── START SCREEN ───────────────────────────────────────────────
if "app_started" not in st.session_state:
    st.session_state.app_started = False

if not st.session_state.app_started:
    st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 18%, rgba(125, 211, 252, 0.28), transparent 18%),
        radial-gradient(circle at 80% 28%, rgba(56, 189, 248, 0.20), transparent 24%),
        linear-gradient(135deg, #082f49 0%, #0c4a6e 42%, #075985 100%);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 0rem;
}

.start-screen {
    min-height: 76vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-card {
    position: relative;
    z-index: 2;
    max-width: 760px;
    padding: 54px 52px 48px;
    border-radius: 26px;
    background: rgba(2, 20, 33, 0.62);
    border: 1px solid rgba(186, 230, 253, 0.34);
    box-shadow: 0 34px 90px rgba(0, 0, 0, 0.32);
    backdrop-filter: blur(18px);
}

.ocean-badge {
    width: 90px;
    height: 90px;
    margin: 0 auto 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 46px;
    background: linear-gradient(145deg, #0ea5e9, #075985);
    box-shadow: 0 18px 44px rgba(14, 165, 233, 0.30);
}

.title {
    font-size: 64px;
    font-weight: 900;
    color: #e0f7ff;
    margin-bottom: 10px;
    line-height: 1;
}

.subtitle {
    font-size: 20px;
    color: #7dd3fc;
    font-weight: 800;
    margin-bottom: 18px;
}

.description {
    font-size: 16px;
    color: #c7f2ff;
    max-width: 620px;
    line-height: 1.75;
    margin: auto;
}

.bubble {
    position: absolute;
    border-radius: 50%;
    background: rgba(186, 230, 253, 0.16);
    border: 2px solid rgba(186, 230, 253, 0.35);
}

.b1 { width: 78px; height: 78px; left: 9%; top: 15%; }
.b2 { width: 42px; height: 42px; right: 18%; top: 23%; }
.b3 { width: 120px; height: 120px; right: 9%; bottom: 13%; }
.b4 { width: 34px; height: 34px; left: 19%; bottom: 18%; }

.wave {
    position: absolute;
    left: -10%;
    bottom: -105px;
    width: 120%;
    height: 235px;
    background: linear-gradient(90deg, #075985, #0284c7, #0891b2);
    border-radius: 50% 50% 0 0;
    opacity: 0.45;
}

.wave.two {
    bottom: -140px;
    background: linear-gradient(90deg, #082f49, #075985, #0e7490);
    opacity: 0.72;
}

div.stButton > button {
    background: linear-gradient(135deg, #075985, #0e7490) !important;
    color: white !important;
    border: 1px solid rgba(186, 230, 253, 0.45) !important;
    border-radius: 999px !important;
    height: 56px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    box-shadow: 0 16px 34px rgba(8, 47, 73, 0.46) !important;
}
</style>

<div class="start-screen">
    <div class="bubble b1"></div>
    <div class="bubble b2"></div>
    <div class="bubble b3"></div>
    <div class="bubble b4"></div>

    <div class="wave"></div>
    <div class="wave two"></div>

    <div class="hero-card">
        <div class="ocean-badge">🌊</div>
        <div class="title">LinguaBot</div>
        <div class="subtitle">Hybrid AI Language Learning Platform</div>
        <div class="description">
            Practice phrases, build vocabulary, use flashcards, take quizzes,
            check grammar, and chat with an AI-powered language tutor.
        </div>
    </div>
</div>
""")

    center = st.columns([2, 1, 2])
    with center[1]:
        if st.button("Get Started", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()

    st.stop()
# ─── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">LinguaBot</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Language learning, reimagined</div>',
                unsafe_allow_html=True)
    st.divider()

    language = st.selectbox(
        "Language",
        get_supported_languages(),
        format_func=lambda x: x.capitalize()
    )

    mode = st.selectbox("Mode", [
        "Phrase Practice",
        "Quiz Mode",
        "Conversation",
        "Grammar Checker",
        "Vocabulary Builder",
        "Flashcards"
    ])

    st.divider()
    st.markdown('<div style="font-size:11px;color:#3a6a7a;margin-bottom:8px;">LANGUAGES</div>',
                unsafe_allow_html=True)
    langs_html = "".join(
        [f'<span class="lang-badge">{l.capitalize()}</span>' for l in get_supported_languages()])
    st.markdown(langs_html, unsafe_allow_html=True)

# ─── HOME ───────────────────────────────────────────────────────
if mode == "Home":
    st.markdown(
        '<div class="page-title">LinguaBot</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">A hybrid language-learning app powered by rules, vocabulary data, and AI tutoring</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="quiz-phrase-box">
        <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;color:#7ab8c8;margin-bottom:16px;text-transform:uppercase;">
            Currently learning
        </div>
        <div class="quiz-phrase-text">{language.capitalize()}</div>
        <div class="quiz-phrase-roman">
            Choose a mode below to begin practicing
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="phrase-card">
            <div class="phrase-original" style="font-size:22px;">Learn</div>
            <div class="phrase-english">Browse phrases and vocabulary from curated datasets.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Learning", type="primary", use_container_width=True):
            st.session_state.selected_mode = "Phrase Practice"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="phrase-card">
            <div class="phrase-original" style="font-size:22px;">Practice</div>
            <div class="phrase-english">Use quizzes and flashcards to test your memory.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Practice Now", use_container_width=True):
            st.session_state.selected_mode = "Quiz Mode"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="phrase-card">
            <div class="phrase-original" style="font-size:22px;">Ask AI</div>
            <div class="phrase-english">Chat with an AI tutor and check grammar naturally.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Tutor", use_container_width=True):
            st.session_state.selected_mode = "Conversation"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("Vocabulary Builder", use_container_width=True):
            st.session_state.selected_mode = "Vocabulary Builder"
            st.rerun()

    with col5:
        if st.button("Flashcards", use_container_width=True):
            st.session_state.selected_mode = "Flashcards"
            st.rerun()

    with col6:
        if st.button("Grammar Checker", use_container_width=True):
            st.session_state.selected_mode = "Grammar Checker"
            st.rerun()


# ─── PHRASE PRACTICE ────────────────────────────────────────────
elif mode == "Phrase Practice":
    st.markdown(
        f'<div class="page-title">{language.capitalize()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Select a topic to browse vocabulary</div>',
                unsafe_allow_html=True)

    categories = get_supported_categories(language.lower())

    if "selected_cat" not in st.session_state:
        st.session_state.selected_cat = categories[0]

    cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        with cols[i]:
            label = CATEGORY_ICONS.get(cat, cat.capitalize())
            if st.button(label, key=f"cat_{cat}", use_container_width=True):
                st.session_state.selected_cat = cat

    st.markdown("<br>", unsafe_allow_html=True)

    selected_category = st.session_state.selected_cat
    st.markdown(
        f'<div class="category-label">{CATEGORY_ICONS.get(selected_category, selected_category)}</div>', unsafe_allow_html=True)

    with open("data/phrases.json", "r", encoding="utf-8") as f:
        all_phrases = json.load(f)

    items = all_phrases[language.lower()][selected_category]
    cols2 = st.columns(2)
    for i, item in enumerate(items):
        with cols2[i % 2]:
            roman_html = f'<div class="phrase-romanized">{item["romanized"]}</div>' if item["romanized"] else ""
            st.markdown(f"""
            <div class="phrase-card">
                <div class="phrase-original">{item["phrase"]}</div>
                {roman_html}
                <div class="phrase-english">{item["translation"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── QUIZ MODE ──────────────────────────────────────────────────
elif mode == "Quiz Mode":
    st.markdown(
        f'<div class="page-title">Quiz — {language.capitalize()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Test your vocabulary knowledge</div>',
                unsafe_allow_html=True)

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if not st.session_state.quiz_data:
        col1, col2 = st.columns([2, 1])
        with col1:
            categories = get_supported_categories(language)
            category = st.selectbox(
                "Topic",
                categories,
                format_func=lambda x: CATEGORY_ICONS.get(x, x.capitalize())
            )
        with col2:
            num_questions = st.slider(
                "Questions", min_value=3, max_value=10, value=5)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Begin Quiz", type="primary"):
            questions = generate_quiz(language, category, num_questions)
            if questions:
                st.session_state.quiz_data = questions
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.rerun()
            else:
                st.warning("Not enough phrases in this category for a quiz.")

    else:
        questions = st.session_state.quiz_data
        idx = st.session_state.quiz_index

        if idx < len(questions):
            st.progress(idx / len(questions),
                        text=f"Question {idx + 1} of {len(questions)}")
            st.markdown("<br>", unsafe_allow_html=True)

            q = questions[idx]

            roman_html = ""
            if q["romanized"]:
                roman_html = f'<div class="quiz-phrase-roman">{q["romanized"]}</div>'

            question_html = f"""
            <div class="quiz-phrase-box">
            <div style="font-size:13px;font-weight:700;color:#0e7490;margin-bottom:10px;">Question {idx + 1} of {len(questions)}</div>
            <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;color:#7ab8c8;margin-bottom:16px;text-transform:uppercase;">What does this mean?</div>
            <div class="quiz-phrase-text">{q["phrase"]}</div>
            {roman_html}
            </div>
            """

            st.markdown(question_html, unsafe_allow_html=True)

            answer = st.radio(
                "", q["options"], key=f"q_{idx}", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Submit", type="primary"):
                if answer == q["correct"]:
                    st.success("Correct")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"Incorrect — the answer is: {q['correct']}")
                st.session_state.quiz_index += 1
                st.rerun()

        else:
            total = len(questions)
            score = st.session_state.quiz_score
            percentage = int((score / total) * 100)

            if score == total:
                st.balloons()

            st.markdown(f"""
            <div class="score-card">
                <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;color:#7ab8c8;margin-bottom:16px;text-transform:uppercase;">Quiz Complete</div>
                <div class="score-number">{score}/{total}</div>
                <div class="score-percent">{percentage}%</div>
                <div class="score-label">{'Outstanding' if score == total else 'Great effort' if percentage >= 70 else 'Keep practicing'}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Try Again", type="primary"):
                st.session_state.quiz_data = None
                st.rerun()

# ─── CONVERSATION ───────────────────────────────────────────────
# ─── CONVERSATION ───────────────────────────────────────────────
elif mode == "Conversation":
    st.markdown(
        f'<div class="page-title">Conversation — {language.capitalize()}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Practice speaking with your AI tutor</div>',
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_language" not in st.session_state:
        st.session_state.chat_language = language

    if st.session_state.chat_language != language:
        st.session_state.messages = []
        st.session_state.chat_language = language

    if not st.session_state.messages:
        welcome = (
            f"Hello! I am your {language.capitalize()} tutor. "
            "Ask me anything about grammar, vocabulary, pronunciation, "
            "translation, or start a conversation."
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome}
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("LinguaBot is thinking..."):
                response = get_llm_response(
                    user_input=user_input,
                    language=language,
                    chat_history=st.session_state.messages
                )
                st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )


# ─── GRAMMAR CHECKER ────────────────────────────────────────────
elif mode == "Grammar Checker":
    st.markdown(
        f'<div class="page-title">Grammar Checker — {language.capitalize()}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Write a sentence and get corrections with explanation</div>',
        unsafe_allow_html=True
    )

    sentence = st.text_area(
        "Enter your sentence",
        placeholder=f"Type a sentence in {language.capitalize()}...",
        height=140
    )

    if st.button("Check Grammar", type="primary"):
        if not sentence.strip():
            st.warning("Please enter a sentence first.")
        else:
            with st.spinner("Checking grammar..."):
                result = check_grammar(sentence, language)

            st.markdown("### Result")
            st.markdown(result)

# ─── VOCABULARY BUILDER ─────────────────────────────────────────
elif mode == "Vocabulary Builder":
    st.markdown(
        f'<div class="page-title">Vocabulary Builder — {language.capitalize()}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Browse, search, and learn useful vocabulary</div>',
        unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search vocabulary",
        placeholder="Search word, meaning, romanization, or example..."
    )

    categories = ["All"] + get_vocab_categories(language)
    difficulties = ["All"] + get_vocab_difficulties(language)

    col1, col2 = st.columns(2)

    with col1:
        selected_vocab_category = st.selectbox("Category", categories)

    with col2:
        selected_difficulty = st.selectbox("Difficulty", difficulties)

    if search_query.strip():
        vocab = search_vocabulary(language, search_query)
    else:
        vocab = get_vocabulary(
            language=language,
            category=selected_vocab_category,
            difficulty=selected_difficulty
        )

    if vocab.empty:
        st.info("No vocabulary found for this selection yet.")
    else:
        st.markdown(
            f'<div class="category-label">{len(vocab)} words found</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(2)

        for i, row in vocab.iterrows():
            with cols[i % 2]:
                romanized = str(row.get("romanized", "")).strip()

                roman_html = ""
                if romanized and romanized.lower() != "nan":
                    roman_html = f'<div class="phrase-romanized">{romanized}</div>'

                card_html = f"""
<div class="phrase-card">
<div class="phrase-original">{row["word"]}</div>
{roman_html}
<div class="phrase-english">{row["meaning"]}</div>
<hr class="phrase-divider">
<div style="font-size:14px;color:#0a2233;margin-bottom:4px;">{row["example"]}</div>
<div style="font-size:13px;color:#7ab8c8;font-style:italic;margin-bottom:4px;">{row["example_romanized"]}</div>
<div style="font-size:13px;color:#6a9aaa;">{row["example_translation"]}</div>
<div style="font-size:11px;color:#7ab8c8;margin-top:10px;text-transform:uppercase;">{row["category"]} · {row["difficulty"]}</div>
</div>
"""

                st.markdown(card_html, unsafe_allow_html=True)
# ─── FLASHCARDS ─────────────────────────────────────────────────
elif mode == "Flashcards":
    st.markdown(
        f'<div class="page-title">Flashcards — {language.capitalize()}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Practice vocabulary one card at a time</div>',
        unsafe_allow_html=True
    )

    categories = ["All"] + get_vocab_categories(language)

    selected_flashcard_category = st.selectbox(
        "Category",
        categories,
        key="flashcard_category"
    )

    vocab = get_vocabulary(
        language=language,
        category=selected_flashcard_category,
        difficulty="All"
    )

    if vocab.empty:
        st.info("No flashcards found for this selection yet.")
    else:
        if "flashcard_index" not in st.session_state:
            st.session_state.flashcard_index = 0

        if "show_flashcard_answer" not in st.session_state:
            st.session_state.show_flashcard_answer = False

        if "flashcard_language" not in st.session_state:
            st.session_state.flashcard_language = language

        if "flashcard_category_selected" not in st.session_state:
            st.session_state.flashcard_category_selected = selected_flashcard_category

        if (
            st.session_state.flashcard_language != language
            or st.session_state.flashcard_category_selected != selected_flashcard_category
        ):
            st.session_state.flashcard_index = 0
            st.session_state.show_flashcard_answer = False
            st.session_state.flashcard_language = language
            st.session_state.flashcard_category_selected = selected_flashcard_category

        total_cards = len(vocab)
        current_index = st.session_state.flashcard_index % total_cards
        card = vocab.iloc[current_index]

        romanized = str(card.get("romanized", "")).strip()
        roman_html = ""

        if romanized and romanized.lower() != "nan":
            roman_html = f'<div class="phrase-romanized">{romanized}</div>'

        st.progress(
            (current_index + 1) / total_cards,
            text=f"Card {current_index + 1} of {total_cards}"
        )

        st.markdown(f"""
        <div class="quiz-phrase-box">
            <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;color:#7ab8c8;margin-bottom:16px;text-transform:uppercase;">
                Vocabulary Card
            </div>
            <div class="quiz-phrase-text">{card["word"]}</div>
            {roman_html}
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.show_flashcard_answer:
            st.markdown(f"""
            <div class="phrase-card">
                <div class="phrase-english">{card["meaning"]}</div>
                <hr class="phrase-divider">
                <div style="font-size:14px;color:#0a2233;margin-bottom:4px;">
                    {card["example"]}
                </div>
                <div style="font-size:13px;color:#7ab8c8;font-style:italic;margin-bottom:4px;">
                    {card["example_romanized"]}
                </div>
                <div style="font-size:13px;color:#6a9aaa;">
                    {card["example_translation"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Previous", use_container_width=True):
                st.session_state.flashcard_index = (
                    st.session_state.flashcard_index - 1
                ) % total_cards
                st.session_state.show_flashcard_answer = False
                st.rerun()

        with col2:
            if st.button("Show Answer", type="primary", use_container_width=True):
                st.session_state.show_flashcard_answer = True
                st.rerun()

        with col3:
            if st.button("Next", use_container_width=True):
                st.session_state.flashcard_index = (
                    st.session_state.flashcard_index + 1
                ) % total_cards
                st.session_state.show_flashcard_answer = False
                st.rerun()
