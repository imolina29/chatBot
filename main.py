# Estructura base para MVP gratuito - Asistente Virtual por Telegram

# ------------------------------------
# Requisitos:
# - FastAPI (API Backend)
# - Telegram Bot (como canal gratuito)
# - OpenAI (GPT-3.5 o 4 con créditos)
# - ChromaDB (para contexto personalizado)
# - Uvicorn (para ejecutar servidor)
# ------------------------------------

from fastapi import FastAPI, Request
import requests
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Configurar logging (consola + archivo)
logging.basicConfig(
    level=logging.DEBUG,  # Nivel de log en modo desarrollo
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot_log.log", encoding="utf-8")
    ]
)

load_dotenv()

app = FastAPI()

# Configurar claves API desde .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validar variables de entorno necesarias
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está definido en .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definido en .env")

# Inicializar cliente OpenAI una vez
client = OpenAI(api_key=OPENAI_API_KEY)

# Endpoint de prueba de salud
@app.get("/status")
def status():
    return {"status": "ok", "mensaje": "Servidor del bot funcionando correctamente"}

# Webhook de Telegram
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

# Función para generar respuesta usando OpenAI GPT
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
        respuesta = response.choices[0].message.content.strip()
        logging.info(f"Respuesta generada: {respuesta}")
        return respuesta
    except Exception as e:
        logging.error(f"Error al consultar OpenAI: {e}")
        return "Lo siento, hubo un problema al generar la respuesta. Por favor intenta más tarde."

# Enviar mensaje a Telegram
def enviar_mensaje_telegram(chat_id, texto):
    logging.debug(f"Token usado: {TELEGRAM_TOKEN}")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": texto
    }

    # Logs de depuración
    logging.info(f"Preparando envío a chat_id {chat_id} con texto: {texto}")
    logging.debug(f"URL: {url}")
    logging.debug(f"Payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"❌ Error al enviar mensaje a Telegram: {response.status_code} - {response.text}")
        else:
            logging.info(f"✅ Mensaje enviado correctamente a chat_id {chat_id}")
    except Exception as e:
        logging.exception(f"⚠️ Excepción al intentar enviar mensaje a Telegram: {e}")

# Cargar contexto desde archivo plano (simula base de conocimiento)
def cargar_contexto():
    try:
        with open("contexto_negocio.txt", "r", encoding="utf-8") as file:
            contexto = file.read()
            logging.info("Contexto cargado correctamente")
            return contexto
    except FileNotFoundError:
        logging.warning("Archivo contexto_negocio.txt no encontrado. Usando contexto por defecto.")
        return "Somos un ecommerce que vende ropa y accesorios. Hacemos envíos a todo el país."

# ------------------------------------
# Script para configurar webhook automáticamente
# ------------------------------------

def configurar_webhook():
    ngrok_url = "https://673d-2800-e2-1b00-133d-88ca-c9fb-b302-510.ngrok-free.app"
    webhook_url = f"{ngrok_url}/webhook"
    print("Webhook final:", webhook_url)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    response = requests.post(url, data={"url": webhook_url})
    logging.info(f"Webhook configurado: {response.json()}")

# ------------------------------------
# Archivo adicional: contexto_negocio.txt
# ------------------------------------
# (Ejemplo de contenido para simular RAG personalizado por cliente)
# """
# - Vendemos ropa para hombres y mujeres.
# - Tenemos envío gratis desde $50.
# - Aceptamos pagos con tarjeta, transferencia y contra entrega.
# - Cambios y devoluciones hasta 10 días.
# - WhatsApp: +123456789
# """

# ------------------------------------
# Instrucciones para correr:
# 1. Crear bot en Telegram (BotFather) y obtener TOKEN.
# 2. Crear archivo .env o exportar TELEGRAM_TOKEN y OPENAI_API_KEY.
# 3. Ejecutar: uvicorn main:app --reload --port 8000
# 4. Exponer el puerto con ngrok: ngrok http 8000
# 5. Ejecutar: configurar_webhook() para registrar el webhook