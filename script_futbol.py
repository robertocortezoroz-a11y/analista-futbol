import os
import requests
import google.generativeai as genai

# CARGA DE SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# CONFIGURACIÓN
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    # Consultamos la Premier League (ID 47)
    response = requests.get(url, headers=headers, params={"leagueid": "47"})
    return response.json()

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": str(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

try:
    print("⚽ Obteniendo datos de fútbol...")
    datos = obtener_datos()
    
    # IMPORTANTE: Usamos 'gemini-1.5-flash' a secas, es el más compatible ahora
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Analiza estos datos de fútbol: {datos}. Dime quiénes son los invictos y dame un pick con emojis."
    
    print("🤖 Generando análisis con la nueva API Key...")
    respuesta = model.generate_content(prompt)
    
    print("📤 Enviando a Telegram...")
    enviar_telegram(f"🏆 *REPORTE RECIÉN SALIDO* 🏆\n\n{respuesta.text}")
    
    print("✅ ¡ESTO ES UN GOLAZO! Revisa tu Telegram.")

except Exception as e:
    print(f"❌ Error con la nueva llave: {e}")
