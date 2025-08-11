import os
import re
import html
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime
from utils.mensajeria import enviar_mensaje
from utils.conversaciones import conversaciones_activas, cerrar_conversacion, reenviar_al_asesor
from app.db.tienda import SessionLocal
from app.services.productos import buscar_productos

load_dotenv()

# --- Configuración de entorno y API ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
ASESOR_CHAT_ID = os.getenv("ASESOR_CHAT_ID")  # Opcional

# --- Estado del bot ---
bot_activo = True

# ==============================
# 🧱 FUNCIONES UTILITARIAS
# ==============================

def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto eliminando caracteres invisibles o problemáticos,
    y asegurando que esté en formato seguro para Telegram.
    """
    if not texto:
        return ""

    # Reemplaza espacios invisibles y limpia caracteres extraños
    texto = texto.replace('\u200b', '')  # Zero-width space
    texto = re.sub(r'[^\x00-\x7F\u00A1-\uFFFF]+', '', texto)  # Elimina caracteres no UTF-8 válidos

    # Opcional: escapa caracteres conflictivos si se usa Markdown
    texto = texto.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace('`', '\\`')
    
    return texto.strip()

def enviar_mensaje(chat_id: int, texto: str) -> bool:
    """
    Envía un mensaje a un chat específico usando la API de Telegram.
    Retorna True si el mensaje fue enviado con éxito, False si falló.
    """
    try:
        texto_limpio = limpiar_texto(texto)

        if not texto_limpio:
            logging.warning(f"⚠️ Texto vacío o inválido. No se envía mensaje a {chat_id}")
            return False

        payload = {
            "chat_id": chat_id,
            "text": texto_limpio,
            "parse_mode": "Markdown",  # Asegúrate de que el texto esté escapado si usas esto
        }

        logging.debug(f"📤 Enviando mensaje a {chat_id}: {texto_limpio}")
        
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"❌ Error HTTP al enviar mensaje a {chat_id}: {http_err} - {response.text}")
    except Exception as e:
        logging.error(f"❌ Error general enviando mensaje a {chat_id}: {e}")
    return False


def notificar_error(chat_id: int, error: Exception):
    logging.error(f"🚨 Error en el bot para chat_id {chat_id}: {error}")


# ==============================
# 🤖 COMANDOS DEL BOT
# ==============================

def manejar_comando(comando: str, chat_id: int) -> str:
    global bot_activo
    comando = normalizar_comando(comando)

    if comando == "/ayuda":
        return (
            "🤖 *¡Hola! Estoy aquí para ayudarte.*\n\n"
            "Puedes escribirme directamente para consultar por productos. Ejemplos:\n"
            "• *¿Tienes relojes?*\n"
            "• *Vendes perfumes?*\n\n"
            "📌 También puedes usar estos comandos:\n"
            "🛍️ /productos – Ver productos disponibles\n"
            "🕒 /horarios – Horario de atención\n"
            "🚚 /envios – Información sobre envíos\n"
            "💸 /costos – Costos de envío\n"
            "🧑‍💼 /asesor – Hablar con un asesor humano\n"
            "❌ /cerrar – Finalizar la conversación actual"
        )

    elif comando == "/estado":
        activos = list(conversaciones_activas.keys())
        if not activos:
            return "🔍 No hay conversaciones activas en este momento."
        listado = "\n".join([f"• Usuario ID: `{uid}`" for uid in activos])
        return f"📊 Conversaciones activas ({len(activos)}):\n{listado}"

    elif comando == "/cerrar":
        cerrar_conversacion(chat_id)
        return "👋 Conversación cerrada. Usa /asesor si deseas volver a iniciar una."

    elif comando == "/reactivar":
        bot_activo = True
        logging.info("🔁 Bot reactivado manualmente por comando /reactivar.")
        return "🔁 Bot reactivado exitosamente."

    elif comando == "/horarios":
        return "🕒 Nuestro horario es de lunes a sábado de 8:00 a.m. a 6:00 p.m."

    elif comando == "/productos":
        return "📦 Contamos con los siguientes productos: Relojes originales, Perfumes, Gafas y más. Puedes preguntarme directamente por alguno."

    elif comando == "/envios":
        return "🚚 Realizamos envíos a todo el país. Tiempo estimado: 2 a 3 días hábiles."

    elif comando == "/costos":
        return "💰 Los costos de envío dependen de la transportadora y el destino. Pregunta y te ayudamos con gusto."

    elif comando == "/asesor":
        logging.info(f"📞 Solicitud de asesor humano por chat_id: {chat_id}")
        mensaje = f"👤 El usuario *{chat_id}* ha solicitado atención personalizada."
        if ASESOR_CHAT_ID:
            try:
                enviar_mensaje(int(ASESOR_CHAT_ID), mensaje)
            except Exception as e:
                logging.warning(f"⚠️ Error notificando al asesor: {e}")
        return "🧑‍💼 En breve un asesor te contactará por este mismo chat."

    elif comando.startswith("/responder "):
        partes = comando.split()
        if len(partes) == 2 and partes[1].isdigit():
            id_usuario = int(partes[1])
            conversaciones_activas[id_usuario] = True
            return (
                f"✏️ Puedes responder escribiendo el siguiente mensaje:\n\n"
                f"{id_usuario}: Tu respuesta aquí"
            )
        else:
            return "❌ Uso incorrecto de /responder. Ejemplo: /responder 123456789"

    else:
        return "❓ Comando no reconocido. Usa /ayuda para ver las opciones disponibles."
    
# ==============================
# 🔁 FUNCIONES AUXILIARES
# ==============================

def normalizar_comando(comando: str) -> str:
    return comando.lower().strip()

def responder_fallback(chat_id: int, mensaje_usuario: str) -> str:
    logging.info(f"🤷 Respuesta fallback para chat_id: {chat_id} – mensaje: {mensaje_usuario}")
    return (
        "🤖 Lo siento, no comprendí tu mensaje.\n"
        "Puedes usar /ayuda para ver las opciones disponibles, o escribe /asesor para hablar con un humano."
    )
def generar_respuesta(chat_id: int, mensaje_usuario: str) -> str:
    try:
        db = SessionLocal()
        respuesta = buscar_productos(mensaje_usuario, db)
        db.close()
        return respuesta
    except Exception as e:
        logging.error(f"❌ Error buscando producto: {e}")
        return responder_fallback(chat_id, mensaje_usuario)
    
def activar_bot():
    global bot_activo
    bot_activo = True
    logging.info("✅ Bot activado manualmente desde endpoint.")

def desactivar_bot():
    global bot_activo
    bot_activo = False
    logging.info("⛔ Bot desactivado manualmente desde endpoint.")