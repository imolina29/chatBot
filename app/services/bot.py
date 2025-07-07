# app/services/bot.py

import logging
from openai import OpenAI
from app.config import OPENAI_API_KEY, ADMIN_CHAT_ID
from app.services.telegram import enviar_mensaje_telegram

client = OpenAI(api_key=OPENAI_API_KEY)
bot_activo = True  # Estado global temporal

# -------------------- Contexto del negocio --------------------

def cargar_contexto() -> str:
    try:
        with open("contexto_negocio.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.warning("⚠️ contexto_negocio.txt no encontrado. Usando contexto por defecto.")
        return "Somos un ecommerce que vende ropa y accesorios. Hacemos envíos a todo el país."

# -------------------- Generador de respuestas --------------------

async def generar_respuesta(user_input: str) -> str:
    global bot_activo

    if not bot_activo:
        return "⚠️ El servicio está suspendido temporalmente por mantenimiento."

    contexto = cargar_contexto()
    prompt = f"Contexto del negocio:\n{contexto}\n\nUsuario: {user_input}\nAsistente:"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        respuesta = response.choices[0].message.content.strip()
        logging.info(f"✅ Respuesta generada: {respuesta}")
        return respuesta

    except Exception as e:
        logging.error(f"❌ Error al generar respuesta: {e}")

        if "insufficient_quota" in str(e).lower() or "you exceeded your current quota" in str(e).lower():
            bot_activo = False
            alerta = "⚠️ Bot desactivado por superar el límite de créditos de OpenAI."
            enviar_mensaje_telegram(ADMIN_CHAT_ID, alerta)
            return "⚠️ El servicio no está disponible. Estamos solucionando el problema."

        return "❌ Ocurrió un error. Por favor, intenta más tarde."

# -------------------- Comandos de Telegram --------------------

def manejar_comando(comando: str, chat_id: int) -> str:
    comando = comando.lower().strip()
    global bot_activo

    if comando == "/ayuda":
        return (
            "📌 *Comandos disponibles:*\n"
            "/creditos – Info sobre creditos\n"
            "/horarios – Info sobre horarios tienda\n"
            "/productos – Muestra los productos disp\n"
            "/envios – Info sobre envios"
        )
    elif comando == "/estado":
        return "✅ El bot está activo." if bot_activo else "🚫 El bot está desactivado temporalmente."
    elif comando == "/reactivar":
        bot_activo = True
        logging.info("🔁 Bot reactivado manualmente por comando /reactivar.")
        return "🔁 Bot reactivado exitosamente."
    else:
        return "❓ Comando no reconocido. Usa /ayuda para ver los comandos disponibles."


def responder_fallback(mensaje: str) -> str:
    mensaje = mensaje.lower().strip()

    respuestas = {
        "productos": "🛍 Tenemos Relojs, perfumes y accesorios. Escríbenos para más detalles.",
        "envíos": "📦 Realizamos envíos a todo el país en 2-5 días hábiles.",
        "horarios": "🕒 Atendemos de lunes a sabado, de 9:00 a 18:00.",
        "ayuda": "🤖 Usa palabras como: productos, envíos, horarios. GPT está temporalmente inactivo.",
    }

    for clave, respuesta in respuestas.items():
        if clave in mensaje:
            return respuesta

    return "⚠️ Por el momento solo puedo responder sobre productos, envíos u horarios. Intenta con una de esas palabras clave."

# -------------------- Control manual del bot --------------------

def activar_bot():
    global bot_activo
    bot_activo = True
    logging.info("✅ Bot activado manualmente.")

def desactivar_bot():
    global bot_activo
    bot_activo = False
    logging.info("⛔ Bot desactivado manualmente.")