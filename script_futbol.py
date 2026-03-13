import os
import requests
import google.generativeai as genai

# CARGA DE SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
    print("⚽ Obteniendo datos...")
    datos = obtener_datos()
    
    # Probamos nombres de modelos uno por uno hasta que uno funcione
    modelos_a_probar = ['gemini-pro', 'models/gemini-1.5-flash-latest', 'models/gemini-1.5-pro']
    resultado = None
    
    for nombre_modelo in modelos_a_probar:
        try:
            print(f"🤖 Intentando con: {nombre_modelo}...")
            model = genai.GenerativeModel(nombre_modelo)
            resultado = model.generate_content(f"Analiza estos datos de fútbol y dime los 3 mejores invictos con emojis: {datos}")
            if resultado:
                break
        except:
            print(f"❌ {nombre_modelo} falló, probando el siguiente...")
            continue

    if resultado:
        print("📤 Enviando a Telegram...")
        status = enviar_telegram("📊 *REPORTE DE HOY* 📊\n\n" + resultado.text)
        if status == 200:
            print("✅ ¡LOGRADO! Revisa tu Telegram.")
        else:
            print(f"⚠️ Telegram error {status}. Revisa tu Chat ID.")
    else:
        print("❌ Ningún modelo de Google respondió.")

except Exception as e:
    print(f"❌ Error final: {e}")
