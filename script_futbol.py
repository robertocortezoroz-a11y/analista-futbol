import os
import requests
import google.generativeai as genai

# CARGA DE LLAVES
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    querystring = {"leagueid": "47"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": str(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    return r.status_code

try:
    print("🛰️ Consultando tabla de posiciones...")
    datos_futbol = obtener_datos()
    
    # IMPORTANTE: Nombre del modelo con el prefijo 'models/'
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"Analiza estos datos de la Premier League: {datos_futbol}. Identifica equipos con pocas derrotas y dame 3 pronósticos con emojis."
    
    print("🧠 Generando análisis con Gemini...")
    # Usamos la configuración por defecto para evitar errores de versión
    resultado = model.generate_content(prompt)
    
    print("📤 Enviando a Telegram...")
    status = enviar_telegram("📊 *REPORTE DE HOY* 📊\n\n" + resultado.text)
    
    if status == 200:
        print("✅ ¡TODO FUNCIONÓ! Revisa tu Telegram.")
    else:
        print(f"⚠️ Telegram dio error {status}. Verifica tu Chat ID.")

except Exception as e:
    print(f"❌ Error detectado: {e}")
