import os
import requests

# Datos de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def test_telegram():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": str(CHAT_ID), 
        "text": "🚩 PRUEBA DE CONEXIÓN: Si ves esto, ¡Telegram y GitHub ya son amigos! El problema es solo la configuración de la IA."
    }
    response = requests.post(url, json=payload)
    return response.status_code

print("🚀 Iniciando prueba de fuego...")
resultado = test_telegram()

if resultado == 200:
    print("✅ ¡MENSAJE ENVIADO! Revisa tu celular.")
else:
    print(f"❌ Error de Telegram: {resultado}. Revisa tus Secrets.")
