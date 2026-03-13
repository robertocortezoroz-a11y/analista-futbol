import os
import requests
import google.generativeai as genai

# CARGA DE LLAVES DESDE SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos_futbol():
    # Usamos el endpoint que ya probamos con éxito
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    querystring = {"leagueid": "47"} # Premier League
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": int(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# Lógica Principal
try:
    print("🛰️ Consultando tabla de posiciones...")
    datos = obtener_datos_futbol()
    
    # AJUSTE: Usamos 'gemini-1.5-flash-latest' que es el nombre más estable
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"Analiza estos datos de la Premier League: {datos}. Identifica a los equipos con menos derrotas (invictos) y dame 3 pronósticos rápidos con emojis para mi canal de Telegram."
    
    print("🧠 Analizando con IA...")
    resultado = model.generate_content(prompt)
    
    cuerpo_mensaje = "📊 *REPORTE DE INVICTOS HOY* 📊\n\n" + resultado.text
    enviar_telegram(cuerpo_mensaje)
    print("✅ ¡Mensaje enviado con éxito!")

except Exception as e:
    print(f"❌ Ocurrió un error: {e}")
