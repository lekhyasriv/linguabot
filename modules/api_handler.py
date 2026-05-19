from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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


def get_ai_response(user_input, language=None):
    try:
        system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["default"])

        full_prompt = f"{system_prompt}\n\nStudent says: {user_input}"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return response.text

    except Exception as e:
        error = str(e)
        if "429" in error:
            return "⚠️ API quota exceeded. Please wait a moment and try again!"
        elif "404" in error:
            return "⚠️ Model not available. Please check your API settings."
        else:
            return f"⚠️ Something went wrong: {error}"
