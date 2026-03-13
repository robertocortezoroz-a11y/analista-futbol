import os
import requests
import google.generativeai as genai
from datetime import datetime

# CONFIGURACIÓN SEGURA (GitHub leerá esto de tus Secrets)
RAPIDAPI_KEY = os.getenv("94917fe064msh24444012bda73b4p1ce17djsncd71813fe0ae")
GEMINI_API_KEY = os.getenv("AIzaSyCMTXjUq9PYbLBDQrCHiY6XFT0WaJ8XbAk")
TELEGRAM_TOKEN = os.getenv("8703979002:AAHt1k1_LF4D_vBsnNlhiqJAQfVArNdwmyM")
TELEGRAM_CHAT_ID = os.getenv("5535233416")

genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers).json()
    return response

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # Aseguramos que el Chat ID sea tratado como número
    payload = {"chat_id": int(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# Ejecución
try:
    datos = obtener_datos()
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analiza estos datos de fútbol: {datos}. Identifica 3 partidos interesantes para hoy y mañana con picks de valor."
    
    resultado = model.generate_content(prompt)
    enviar_telegram("🤖 *REPORTE DE IA:* \n\n" + resultado.text)
    print("✅ Todo salió bien")
except Exception as e:
    print(f"❌ Error: {e}")
