import os
import requests
import google.generativeai as genai

# GitHub llenará esto automáticamente con tus Secrets
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración del motor de IA
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": int(TELEGRAM_CHAT_ID),
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# Ejecución principal
try:
    print("🛰️ Consultando datos de fútbol...")
    datos = obtener_datos()
    
    # Usamos el modelo correcto: 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Analiza estos datos de ligas populares: {datos}. Dime los 3 partidos más interesantes de hoy con un pronóstico breve. Usa emojis."
    
    print("🧠 Generando análisis con IA...")
    resultado = model.generate_content(prompt)
    
    enviar_telegram("🤖 *MI ANALISTA IA* ⚽\n\n" + resultado.text)
    print("✅ ¡Mensaje enviado a Telegram!")

except Exception as e:
    print(f"❌ Error durante el proceso: {e}")
