# app/services/telegram.py

import logging
import requests
from app.config import TELEGRAM_TOKEN, NGROK_URL

def enviar_mensaje_telegram(chat_id: int, texto: str) -> None:
    """
    Envía un mensaje de texto a un usuario o grupo en Telegram.

    Args:
        chat_id (int): ID del chat de Telegram.
        texto (str): Contenido del mensaje.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto,
        "parse_mode": "Markdown",  # Permite formato enriquecido
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"❌ Error al enviar mensaje: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.exception(f"❌ Excepción al enviar mensaje a Telegram: {e}")


def registrar_comandos_telegram() -> None:
    """
    Registra los comandos disponibles para el bot en Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setMyCommands"
    comandos = [
        {"command": "ayuda", "description": "Muestra los comandos disponibles"},
        {"command": "estado", "description": "Indica si el bot está activo"},
        {"command": "creditos", "description": "Muestra informaicion de los creditos"},
        {"command": "productos", "description": "Qué vendemos"},
        {"command": "envios", "description": "Tiempos y costos de envío"},
        {"command": "horarios", "description": "Horario de atención"},
        {"command": "reactivar", "description": "Reactiva el bot (solo admin)"},
    ]

    try:
        response = requests.post(url, json={"commands": comandos})
        if response.status_code == 200:
            logging.info("✅ Comandos registrados exitosamente en Telegram.")
        else:
            logging.warning(f"⚠️ Error al registrar comandos: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"❌ Excepción al registrar comandos de Telegram: {e}")


def configurar_webhook() -> None:
    """
    Configura el webhook de Telegram con la URL pública (ej. desde ngrok).
    """
    webhook_url = f"{NGROK_URL}/webhook"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

    try:
        response = requests.post(url, data={"url": webhook_url})
        response_json = response.json()
        logging.info(f"✅ Webhook configurado correctamente: {response_json}")
    except requests.RequestException as e:
        logging.error(f"❌ Error al configurar webhook de Telegram: {e}")