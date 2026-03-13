import os
import requests
import google.generativeai as genai
from datetime import datetime

# Cargar llaves desde los Secrets de GitHub
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def obtener_datos():
    # Usando la nueva API: Free API Live Football Data
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    print("🛰️ Consultando ligas populares...")
    response = requests.get(url, headers=headers).json()
    return response

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

# Ejecución principal
try:
    datos = obtener_datos()
    
    # Le pedimos a Gemini que filtre los invictos de esos datos
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analiza estos datos de fútbol: {datos}
    Identifica equipos que jueguen hoy viernes o mañana sábado que vengan con rachas de 4+ partidos sin perder.
    Crea un panel de valor con: Partido, Recomendación (Doble oportunidad o Hándicap) y Justificación breve.
    Si no encuentras rachas claras, indica los 3 partidos más seguros de las ligas principales.
    """
    
    resultado = model.generate_content(prompt)
    enviar_telegram("📊 *PANEL DE VALOR GENERADO:* \n\n" + resultado.text)
    print("✅ ¡Mensaje enviado a Telegram!")

except Exception as e:
    print(f"❌ Error: {e}")
