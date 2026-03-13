import os
import requests
import google.generativeai as genai
from datetime import datetime

# Cargar llaves desde los Secrets de GitHub
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def obtener_invictos():
    hoy = datetime.now().strftime('%Y-%m-%d')
    ligas = [39, 140, 135, 78, 61] # Premier, LaLiga, Serie A, Bundesliga, Ligue 1
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}
    
    hallazgos = []

    for liga in ligas:
        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={hoy}&league={liga}"
        partidos = requests.get(url, headers=headers).json().get('response', [])
        
        for p in partidos:
            for side in ['home', 'away']:
                team = p['teams'][side]
                # Consultar forma (últimos 5)
                url_f = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?team={team['id']}&last=5"
                historial = requests.get(url_f, headers=headers).json().get('response', [])
                
                # Lógica: ¿Cero derrotas en los últimos 4?
                derrotas = 0
                for h in historial[:4]:
                    win_home = h['teams']['home']['winner']
                    win_away = h['teams']['away']['winner']
                    # Si el equipo era local y perdió, o era visitante y perdió
                    if (h['teams']['home']['id'] == team['id'] and win_home is False and win_away is True) or \
                       (h['teams']['away']['id'] == team['id'] and win_away is False and win_home is True):
                        derrotas += 1
                
                if derrotas == 0 and len(historial) >= 4:
                    hallazgos.append(f"🔥 {team['name']} (Invicto en 4+ partidos)")

    return hallazgos

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

# Ejecución
señales = obtener_invictos()
if señales:
    resumen = "🚨 *EQUIPOS INVICTOS HOY:*\n\n" + "\n".join(señales)
    # Aquí Gemini le da el toque final
    model = genai.GenerativeModel('gemini-1.5-flash')
    analisis = model.generate_content(f"Analiza estas señales de equipos invictos y crea un panel de apuestas de valor para hoy: {resumen}")
    enviar_telegram(analisis.text)
else:
    enviar_telegram("ℹ️ Hoy no se detectaron equipos invictos (4+ partidos) en las ligas principales.")
