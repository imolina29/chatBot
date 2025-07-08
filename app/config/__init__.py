import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")

# Asegúrate de cargar correctamente la lista de admins
ADMIN_CHAT_IDS = os.getenv("ADMIN_CHAT_IDS", "")
ADMIN_CHAT_IDS = [int(chat_id.strip()) for chat_id in ADMIN_CHAT_IDS.split(",") if chat_id.strip().isdigit()]

# Asegúrate de cargar correctamente la lista de asesores
ASESORES_CHAT_IDS = os.getenv("ASESORES_CHAT_IDS", "")
ASESORES_CHAT_IDS = [int(cid.strip()) for cid in ASESORES_CHAT_IDS.split(",") if cid.strip().isdigit()]