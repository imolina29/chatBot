# main.py limpio y optimizado

from app.config import TELEGRAM_TOKEN, OPENAI_API_KEY, NGROK_URL, ADMIN_CHAT_ID
from fastapi import FastAPI, Request
import requests
import logging
from dotenv import load_dotenv
from openai import OpenAI

# -------------------- Configuración --------------------

# Variable global para controlar estado del bot
bot_activo = True

logging.basicConfig(
    level=logging.INFO,  # Puedes cambiar a DEBUG si necesitas
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot_log.log", encoding="utf-8")
    ]
)

app = FastAPI()

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

@app.post("/activar")
def activar_bot():
    global bot_activo
    bot_activo = True
    logging.info("✅ Bot reactivado manualmente.")
    return {"status": "ok", "mensaje": "Bot reactivado."}

@app.post("/desactivar")
def desactivar_bot():
    global bot_activo
    bot_activo = False
    logging.info("⛔ Bot desactivado manualmente.")
    return {"status": "ok", "mensaje": "Bot desactivado."}

@app.get("/status")
def status():
    return {
        "status": "ok",
        "bot_activo": bot_activo,
        "mensaje": "Servidor del bot funcionando correctamente"
    }

# -------------------- Funciones auxiliares --------------------
# ID del admin para alertas

async def generar_respuesta(user_input):
    global bot_activo
    if not bot_activo:
        return "El servicio se encuentra temporalmente suspendido por mantenimiento."

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

        # Verificar si es por créditos agotados
        if "insufficient_quota" in str(e).lower() or "You exceeded your current quota" in str(e):
            bot_activo = False
            alerta = "⚠️ El bot ha sido desactivado temporalmente por exceder el límite de créditos de OpenAI."
            enviar_mensaje_telegram(ADMIN_CHAT_ID, alerta)
            return "⚠️ Actualmente el servicio no está disponible. Estamos solucionando el inconveniente."
        
        return "Lo siento, hubo un problema al generar la respuesta. Por favor intenta más tarde."

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
    webhook_url = f"{NGROK_URL}/webhook"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"

    try:
        response = requests.post(url, data={"url": webhook_url})
        response_json = response.json()
        logging.info(f"Webhook configurado: {response_json}")
    except Exception as e:
        logging.error(f"Error al configurar webhook: {e}")