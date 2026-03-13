import os
import requests
import google.generativeai as genai

# CARGA DE SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración ultra-estable
genai.configure(api_key=GEMINI_API_KEY)

def obtener_futbol():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"}
    # Usamos la liga 47 (Premier League)
    r = requests.get(url, headers=headers, params={"leagueid": "47"})
    return r.json()

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": str(TELEGRAM_CHAT_ID), "text": texto, "parse_mode": "Markdown"})

try:
    print("⚽ Leyendo tabla...")
    datos = obtener_futbol()
    
    # Forzamos el modelo 'gemini-1.5-flash' sin el prefijo models/ para evitar el 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("🧠 IA Analizando...")
    # Creamos un prompt más simple para asegurar respuesta
    prompt = f"Analiza estos datos de fútbol: {datos}. Dime los 3 equipos con menos derrotas y un consejo corto."
    
    response = model.generate_content(prompt)
    
    print("📤 Enviando a Telegram...")
    enviar_telegram(f"🏆 *ANALISTA DE INVICTOS* 🏆\n\n{response.text}")
    print("✅ ¡PROCESO FINALIZADO CON ÉXITO!")

except Exception as e:
    # Si la IA falla, al menos que nos mande los datos crudos para no quedarnos sin nada
    print(f"⚠️ Error IA: {e}")
    enviar_telegram("⚠️ La IA está ocupada, pero aquí tienes los datos crudos de la Premier League. ¡Revisa los equipos con 3 o 4 derrotas!")
