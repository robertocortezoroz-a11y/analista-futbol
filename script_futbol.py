import os
import requests
import google.generativeai as genai

# CONFIGURACIÓN SEGURA: GitHub sacará los valores de tus 'Secrets'
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Conectamos con la Inteligencia Artificial
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    # Consultamos los partidos del día
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return {"error": "No se pudo obtener datos de la API"}

def enviar_telegram(mensaje):
    # Enviamos el reporte a tu celular
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": int(TELEGRAM_CHAT_ID), 
        "text": mensaje, 
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# EL PROCESO DE ANÁLISIS
try:
    print("🛰️ Buscando partidos...")
    datos_futbol = obtener_datos()
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        f"Analiza estos partidos: {datos_futbol}. "
        "Dime cuáles son los 3 mejores para apostar hoy. "
        "Usa emojis y que se vea muy profesional para Telegram."
    )
    
    respuesta = model.generate_content(prompt)
    
    enviar_telegram("📊 *REPORTE DE VALOR* 📊\n\n" + respuesta.text)
    print("✅ ¡Reporte enviado con éxito a Telegram!")

except Exception as e:
    print(f"❌ Ocurrió un error: {e}")
