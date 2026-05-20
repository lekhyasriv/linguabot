from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite"

SYSTEM_PROMPTS = {
    "japanese": "You are a friendly Japanese language tutor for college students. Keep responses short, clear and educational. Always show Japanese script with romanization and English translation.",
    "french": "You are a friendly French language tutor for college students. Keep responses short, clear and educational.",
    "german": "You are a friendly German language tutor for college students. Keep responses short, clear and educational.",
    "korean": "You are a friendly Korean language tutor for college students. Keep responses short, clear and educational. Always show Korean script with romanization and English translation.",
    "chinese": "You are a friendly Chinese language tutor for college students. Keep responses short, clear and educational. Always show Chinese characters with pinyin and English translation.",
    "russian": "You are a friendly Russian language tutor for college students. Keep responses short, clear and educational. Always show Cyrillic script with romanization and English translation.",
    "italian": "You are a friendly Italian language tutor for college students. Keep responses short, clear and educational.",
    "default": "You are a friendly multilingual language tutor for college students. Keep responses short, clear and educational."
}


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file.")

    return genai.Client(api_key=api_key)


def build_chat_prompt(user_input, language, chat_history=None):
    language = language.lower() if language else "default"
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["default"])

    history_text = ""
    if chat_history:
        for message in chat_history[-8:]:
            role = message.get("role", "user")
            content = message.get("content", "")
            history_text += f"{role}: {content}\n"

    return f"""
{system_prompt}

You are part of LinguaBot, a hybrid language-learning app.
The app has rule-based phrase practice and quizzes, but you power the chatbot.

Rules:
- Act like a helpful language tutor.
- Help with translation, grammar, vocabulary, pronunciation, and conversation.
- Keep answers beginner-friendly.
- If the student makes a mistake, correct it gently.
- If useful, give one short example.
- Do not give very long answers unless asked.

Conversation history:
{history_text}

Student: {user_input}

LinguaBot:
"""


def get_llm_response(user_input, language=None, chat_history=None):
    try:
        client = get_client()

        prompt = build_chat_prompt(
            user_input=user_input,
            language=language,
            chat_history=chat_history
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        error = str(e)

        if "429" in error:
            return "API quota exceeded. Please wait a little and try again."
        if "404" in error:
            return "Model not available. Please check your Gemini model name."
        return f"Something went wrong: {error}"


def check_grammar(sentence, language=None):
    try:
        client = get_client()

        language = language.lower() if language else "the selected language"

        prompt = f"""
You are LinguaBot, a friendly grammar tutor for English-speaking college students.

Target language being studied: {language}

Check the student's sentence in {language}.

Student sentence:
{sentence}

Important:
- Write your explanation in English.
- Only the corrected sentence and examples should be in {language}.
- If {language} uses a non-Latin script, include romanization.
- Keep the tone friendly and beginner-friendly.
- Do not write the whole response in {language}.

Your response must include:
1. Corrected sentence
2. Romanization or pronunciation if useful
3. English meaning
4. Short grammar explanation in English
5. One improved example sentence with English meaning
"""
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        error = str(e)

        if "429" in error:
            return "The AI grammar checker has reached its free usage limit. Please try again later."
        if "501" in error or "UNAVAILABLE" in error:
            return "The AI grammar checker is unavailable because the API key is invalid or missing."
        if "404" in error:
            return "The selected AI model is not available. Please check your Gemini model name."

        return f"Something went wrong: {error}"
