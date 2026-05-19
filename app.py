import streamlit as st
import json
from modules.phrase_lookup import get_phrases, get_supported_languages, get_supported_categories
from modules.quiz_engine import generate_quiz
from modules.intent_router import route
from modules.api_handler import get_ai_response

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

    .stRadio label {
        background: white;
        border: 1px solid #d0eaf2;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.15s;
    }

    .stRadio label:hover {
        border-color: #0e7490;
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
    }
</style>
""", unsafe_allow_html=True)

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
        "Conversation"
    ])

    st.divider()
    st.markdown('<div style="font-size:11px;color:#3a6a7a;margin-bottom:8px;">LANGUAGES</div>',
                unsafe_allow_html=True)
    langs_html = "".join(
        [f'<span class="lang-badge">{l.capitalize()}</span>' for l in get_supported_languages()])
    st.markdown(langs_html, unsafe_allow_html=True)

# ─── PHRASE PRACTICE ────────────────────────────────────────────
if mode == "Phrase Practice":
    st.markdown(
        f'<div class="page-title">{language.capitalize()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Select a topic to browse vocabulary</div>',
                unsafe_allow_html=True)

    categories = get_supported_categories(language)

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

    items = all_phrases[language][selected_category]
    cols2 = st.columns(2)
    for i, item in enumerate(items):
        with cols2[i % 2]:
            roman_html = f'<div class="phrase-romanized">{item["romanized"]}</div>' if item["romanized"] else ""
            st.markdown(f"""
            <div class="phrase-card">
                <div class="phrase-original">{item["phrase"]}</div>
                {roman_html}
                <hr class="phrase-divider">
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
            roman_html = f'<div class="quiz-phrase-roman">{q["romanized"]}</div>' if q["romanized"] else ""
            st.markdown(f"""
            <div class="quiz-phrase-box">
                <div style="font-size:12px;font-weight:600;letter-spacing:0.1em;color:#7ab8c8;margin-bottom:16px;text-transform:uppercase;">What does this mean?</div>
                <div class="quiz-phrase-text">{q["phrase"]}</div>
                {roman_html}
            </div>
            """, unsafe_allow_html=True)

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
elif mode == "Conversation":
    st.markdown(
        f'<div class="page-title">Conversation — {language.capitalize()}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Practice speaking with your AI tutor</div>',
                unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = f"Hello! I am your {language.capitalize()} tutor. Ask me anything — grammar, vocabulary, pronunciation, or simply have a conversation. How can I help you today?"
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        routed = route(user_input)
        if routed["use_api"]:
            response = get_ai_response(user_input, language)
        else:
            response = get_phrases(language, "greetings")

        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
