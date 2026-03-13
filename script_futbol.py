import os
import requests
import google.generativeai as genai

# CARGA SEGURA DESDE GITHUB SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)

def obtener_invictos():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    querystring = {"leagueid": "47"} # ID 47 es la Premier League
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        return f"Error API: {e}"

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": int(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# EJECUCIÓN
try:
    print("⚽ Obteniendo tabla de posiciones...")
    tabla = obtener_invictos()
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = (
        f"Analiza esta tabla de posiciones: {tabla}. "
        "Busca los equipos con menos derrotas (invictos o casi invictos). "
        "Redacta un reporte corto para Telegram con emojis, mencionando al equipo más sólido "
        "y dándome un pronóstico de racha para su próximo juego."
    )
    
    print("🧠 Gemini analizando datos...")
    respuesta = model.generate_content(prompt)
    
    enviar_telegram("🏆 *REPORTE DE INVICTOS* 🏆\n\n" + respuesta.text)
    print("✅ ¡Enviado a Telegram!")

except Exception as e:
    print(f"❌ Error: {e}")
