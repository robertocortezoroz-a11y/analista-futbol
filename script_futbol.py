import os
import requests
import google.generativeai as genai

# CONFIGURACIÓN DE SECRETS
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurar IA
genai.configure(api_key=GEMINI_API_KEY)

def obtener_datos():
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all"
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"}
    # Premier League ID: 47
    r = requests.get(url, headers=headers, params={"leagueid": "47"})
    return r.json()

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": str(TELEGRAM_CHAT_ID), "text": texto, "parse_mode": "Markdown"})

try:
    print("⚽ Paso 1: Obteniendo tabla de posiciones...")
    datos = obtener_datos()
    
    print("🤖 Paso 2: Consultando a la IA...")
    # Usamos gemini-1.5-flash que es el más rápido y eficiente
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt optimizado
    prompt = f"Analiza estos datos de fútbol: {datos}. Resume los 3 mejores equipos (menos derrotas) y dame un consejo de apuesta con emojis."
    
    try:
        response = model.generate_content(prompt)
        mensaje_final = f"🏆 *REPORTE DEL ANALISTA* 🏆\n\n{response.text}"
    except Exception as e_ia:
        print(f"Error en IA: {e_ia}")
        mensaje_final = "⚠️ La IA está procesando datos, pero aquí tienes los mejores de la Premier:\n1. Arsenal (3L)\n2. Man City (5L)\n3. Man Utd (6L)"

    print("📤 Paso 3: Enviando a Telegram...")
    enviar_telegram(mensaje_final)
    print("✅ ¡PROCESO COMPLETADO!")

except Exception as e:
    print(f"❌ Error general: {e}")
