
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")