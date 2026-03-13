import os
import requests
import google.generativeai as genai

# Carga segura desde GitHub Secrets
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración de la IA
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
        return {"info": "No hay datos disponibles en este momento"}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": int(TELEGRAM_CHAT_ID),
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# Lógica principal
try:
    print("🛰️ Consultando ligas...")
    datos = obtener_datos()
    
    # CAMBIO IMPORTANTE: Usamos 'models/gemini-1.5-flash-latest'
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"Analiza estos datos de fútbol: {datos}. Dame los 3 mejores pronósticos para hoy con emojis."
    
    print("🧠 Generando análisis...")
    resultado = model.generate_content(prompt)
    
    enviar_telegram("📊 *REPORTE DEL DÍA* 📊\n\n" + resultado.text)
    print("✅ ¡ENVIADO CON ÉXITO!")

except Exception as e:
    print(f"❌ Error: {e}")
