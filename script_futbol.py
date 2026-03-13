import os
import requests
import google.generativeai as genai

# CARGA DE LLAVES
RAPIDAPI_KEY = os.getenv("94917fe064msh24444012bda73b4p1ce17djsncd71813fe0ae")
GEMINI_API_KEY = os.getenv("AIzaSyCMTXjUq9PYbLBDQrCHiY6XFT0WaJ8XbAk")
TELEGRAM_TOKEN = os.getenv("8703979002:AAHt1k1_LF4D_vBsnNlhiqJAQfVArNdwmyM")
TELEGRAM_CHAT_ID = os.getenv("5535233416")

# Verificación de seguridad (esto saldrá en el Log de GitHub)
if not GEMINI_API_KEY:
    print("❌ ERROR: No se encontró la GEMINI_API_KEY en los Secrets")
else:
    print(f"✅ Llave Gemini detectada (empieza por: {GEMINI_API_KEY[:5]}...)")

genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    # Usaremos un endpoint que sabemos que funciona para probar
    url = "https://free-api-live-football-data.p.rapidapi.com/api-v1/get-popular-leagues"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return {"error": "No se pudo conectar a la API de fútbol"}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": int(TELEGRAM_CHAT_ID), "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# EJECUCIÓN
try:
    print("🛰️ Iniciando escaneo...")
    datos = obtener_datos()
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Analiza estos datos de fútbol: {datos}. Dame los 3 mejores partidos para apostar hoy con una breve explicación."
    
    resultado = model.generate_content(prompt)
    enviar_telegram("🤖 *ANALISTA IA:* \n\n" + resultado.text)
    print("🚀 ¡Mensaje enviado!")
except Exception as e:
    print(f"❌ Error final: {e}")
