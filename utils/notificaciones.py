import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def notificar_asesor(chat_id_usuario: int, mensaje_usuario: str):
    mensaje = (
        f"📩 *Solicitud de asesor humano*\n"
        f"👤 Chat ID: `{chat_id_usuario}`\n"
        f"💬 Comando: `{mensaje_usuario}`\n"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Error notificando al asesor: {e}")