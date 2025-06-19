from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Template filters
@app.template_filter('get_flag_emoji')
def get_flag_emoji(language):
    flags = {
        'english': '🇬🇧',
        'french': '🇫🇷',
        'spanish': '🇪🇸',
        'german': '🇩🇪',
        'italian': '🇮🇹',
        'hindi': '🇮🇳',
        'japanese': '🇯🇵'
    }
    return flags.get(language, '🌐')

@app.template_filter('get_localized_greeting')
def get_localized_greeting(language):
    greetings = {
        'english': 'Hello! Ready to learn?',
        'french': 'Bonjour! Prêt à apprendre?',
        'spanish': '¡Hola! ¿Listo para aprender?',
        'german': 'Hallo! Bereit zu lernen?',
        'italian': 'Ciao! Pronto ad imparare?',
        'hindi': 'नमस्ते! सीखने के लिए तैयार?',
        'japanese': 'こんにちは！学ぶ準備はできましたか？'
    }
    return greetings.get(language, 'Hello!')

LANGUAGE_DATA = {
    "english": {
        "prompt": "You are LangBot, a friendly English tutor...",
        "theme": "london",
        "icon": "🏰",
        "welcome": "Welcome to LangBot!",
        "colors": ["#012169", "#C8102E", "#FFFFFF"],
        "font": "'Times New Roman', serif"
    },
    "french": {
        "prompt": "Vous êtes LangBot, un tuteur français sympathique...",
        "theme": "paris",
        "icon": "🗼",
        "welcome": "Bienvenue sur LangBot!",
        "colors": ["#0055A4", "#FFFFFF", "#EF4135"],
        "font": "'Playfair Display', serif"
    },
    "spanish": {
        "prompt": "Eres LangBot, un tutor de español amable...",
        "theme": "madrid",
        "icon": "🎸",
        "welcome": "¡Bienvenido a LangBot!",
        "colors": ["#AA151B", "#F1BF00", "#AA151B"],
        "font": "'Montserrat', sans-serif"
    },
    "german": {
        "prompt": "Sie sind LangBot, ein freundlicher Deutschlehrer...",
        "theme": "berlin",
        "icon": "🏛️",
        "welcome": "Willkommen bei LangBot!",
        "colors": ["#000000", "#DD0000", "#FFCE00"],
        "font": "'Roboto', sans-serif"
    },
    "italian": {
        "prompt": "Sei LangBot, un simpatico tutor di italiano...",
        "theme": "rome",
        "icon": "🏛️",
        "welcome": "Benvenuto su LangBot!",
        "colors": ["#009246", "#FFFFFF", "#CE2B37"],
        "font": "'Palatino', serif"
    },
    "hindi": {
        "prompt": "आप LangBot हैं, एक मिलनसार हिंदी शिक्षक...",
        "theme": "delhi",
        "icon": "🕌",
        "welcome": "LangBot में आपका स्वागत है!",
        "colors": ["#FF9933", "#FFFFFF", "#138808"],
        "font": "'Poppins', sans-serif"
    },
    "japanese": {
        "prompt": "あなたはLangBot、親切な日本語のチューターです...",
        "theme": "tokyo",
        "icon": "🗾",
        "welcome": "LangBotへようこそ！",
        "colors": ["#BC002D", "#FFFFFF", "#BC002D"],
        "font": "'Noto Sans JP', sans-serif"
    }
}

@app.route("/")
def index():
    return render_template("landing.html", 
                         languages=LANGUAGE_DATA.keys(),
                         LANGUAGE_DATA=LANGUAGE_DATA)  # Add this line

@app.route("/chat/<language>")
def chat_interface(language):
    if language not in LANGUAGE_DATA:
        language = "english"
    return render_template("chat.html", lang_data=LANGUAGE_DATA[language], language=language)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    language = data.get("language", "english").lower()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": LANGUAGE_DATA[language]["prompt"]},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                               headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)