import os
import requests
import google.generativeai as genai

# --- CONFIGURACIÓN CON TUS LLAVES ---
RAPIDAPI_KEY = "94917fe064msh24444012bda73b4p1ce17djsncd71813fe0ae"
TELEGRAM_TOKEN = "8703979002:AAHt1k1_LF4D_vBsnNlhiqJAQfVArNdwmyM"
TELEGRAM_CHAT_ID = 5535233416
GEMINI_API_KEY = "AIzaSyCv82Op0LgqflzNM41sYQ8Me3eNDvgN8J8"

genai.configure(api_key=GEMINI_API_KEY)

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    print(f"Respuesta Telegram: {r.status_code}")

def iniciar():
    print("🚀 Iniciando escaneo de valor...")
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY, 
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        datos = response.json()
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analiza estos datos de fútbol: {datos}. Dime 3 pronósticos de equipos invictos o con alta probabilidad de ganar hoy. Formato: Partido - Pronóstico - Justificación breve."
        
        resultado = model.generate_content(prompt)
        enviar_telegram(f"📊 **ANÁLISIS DE HOY**\n\n{resultado.text}")
        print("✅ Proceso completado con éxito")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    iniciar()
