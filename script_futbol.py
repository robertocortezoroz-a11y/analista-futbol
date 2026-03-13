import os
import requests
import google.generativeai as genai
from datetime import datetime

# --- TUS LLAVES CONFIGURADAS ---
RAPIDAPI_KEY = "94917fe064msh24444012bda73b4p1ce17djsncd71813fe0ae"
TELEGRAM_TOKEN = "8703979002:AAHt1k1_LF4D_vBsnNlhiqJAQfVArNdwmyM"
TELEGRAM_CHAT_ID = 5535233416
GEMINI_API_KEY = "AIzaSyCv82Op0LgqflzNM41sYQ8Me3eNDvgN8J8" # <--- ESTA ES LA ÚNICA QUE ME FALTA

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
    except:
        return None

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# Ejecución
datos = obtener_datos()
if datos:
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analiza estos datos de fútbol y dime 3 pronósticos de valor para hoy basados en equipos que no hayan perdido en sus últimos partidos: {datos}"
    
    try:
        resultado = model.generate_content(prompt)
        enviar_telegram("🚀 **PANEL DE HOY:**\n\n" + resultado.text)
        print("✅ Enviado!")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No hay datos")
