# main.py limpio y optimizado

from fastapi import FastAPI, Request
import requests
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# -------------------- Configuración --------------------

logging.basicConfig(
    level=logging.INFO,  # Puedes cambiar a DEBUG si necesitas
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot_log.log", encoding="utf-8")
    ]
)

app = FastAPI()
load_dotenv(dotenv_path=".env", override=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está definido en el archivo .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definido en el archivo .env")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------- Endpoints --------------------

@app.get("/status")
def status():
    return {"status": "ok", "mensaje": "Servidor del bot funcionando correctamente"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    message = data.get("message", {}).get("text")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    logging.info(f"Mensaje recibido: {message} de chat_id: {chat_id}")

    if message and chat_id:
        respuesta = await generar_respuesta(message)
        enviar_mensaje_telegram(chat_id, respuesta)
    return {"status": "ok"}

# -------------------- Funciones auxiliares --------------------

async def generar_respuesta(user_input):
    context = cargar_contexto()
    prompt = f"Contexto del negocio:\n{context}\n\nUsuario: {user_input}\nAsistente:"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error al consultar OpenAI: {e}")
        return "Lo siento, hubo un problema al generar la respuesta."

def enviar_mensaje_telegram(chat_id, texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto}

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"Error al enviar mensaje: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Error al enviar mensaje a Telegram: {e}")

def cargar_contexto():
    try:
        with open("contexto_negocio.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.warning("Archivo contexto_negocio.txt no encontrado. Usando contexto por defecto.")
        return "Somos un ecommerce que vende ropa y accesorios. Hacemos envíos a todo el país."

# -------------------- Utilidad para configurar webhook --------------------

def configurar_webhook():
    ngrok_url = "https://673d-2800-e2-1b00-133d-88ca-c9fb-b302-510.ngrok-free.app"
    webhook_url = f"{ngrok_url}/webhook"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

    try:
        response = requests.post(url, data={"url": webhook_url})
        response_json = response.json()
        logging.info(f"Webhook configurado: {response_json}")
    except Exception as e:
        logging.error(f"Error al configurar webhook: {e}")