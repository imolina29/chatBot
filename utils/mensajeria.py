# app/utils/mensajeria.py
import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def enviar_mensaje(chat_id: int, texto: str) -> bool:
    try:
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"❌ Error enviando mensaje a {chat_id}: {e}")
        return False