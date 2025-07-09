# app/routes/telegram.py

from fastapi import APIRouter, Request
import logging
from app.services.bot import (
    manejar_comando,
    enviar_mensaje
)
from utils.conversaciones import esta_activa
from app.services.history import guardar_conversacion
from utils.conversaciones import (
    conversaciones_activas,
    guardar_conversacion,
    cerrar_conversacion,
    reenviar_al_asesor,
    activar_conversacion,
    asignar_asesor,
    obtener_asesor,
    obtener_cliente
)
from app.config import ASESORES_CHAT_IDS
from app.config.constants import ASESOR_CHAT_ID
from app.config import ADMIN_CHAT_IDS
from app.db.registrar import registrar_conversacion

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    logging.info(f"📨 Mensaje recibido: {data}")

    mensaje = data.get("message", {})
    chat_id = mensaje.get("chat", {}).get("id")
    texto = mensaje.get("text", "")

    if not chat_id or not texto:
        logging.warning("❌ Mensaje sin chat_id o texto válido.")
        return {"status": "error"}

    # --- 1. Si el asesor responde ---
    if chat_id in ASESORES_CHAT_IDS:
        if ":" in texto:
            try:
                partes = texto.split(":", 1)
                id_usuario = int(partes[0].strip())
                respuesta = partes[1].strip()

                enviar_mensaje(id_usuario, f"🧑‍💼 Asesor: {respuesta}")
                asignar_asesor(id_usuario, chat_id)
                guardar_conversacion(id_usuario, texto, "Respuesta del asesor")
                registrar_conversacion(id_usuario, respuesta_bot=respuesta)
                enviar_mensaje(chat_id, f"✅ Mensaje enviado a {id_usuario}:{respuesta}")
                return {"status": "ok"}

            except Exception as e:
                logging.error(f"❌ Error reenviando respuesta del asesor: {e}")
                enviar_mensaje(chat_id, "❌ Formato incorrecto. Usa:\n\n`<ID_usuario>: respuesta`")
                return {"status": "error"}

        else:
            cliente_id = obtener_cliente(chat_id)
            if cliente_id:
                enviar_mensaje(cliente_id, f"🧑‍💼 Asesor: {texto}")
                guardar_conversacion(cliente_id, texto, "Respuesta del asesor")
                registrar_conversacion(cliente_id, respuesta_bot=texto)
                return {"status": "ok"}
            else:
                enviar_mensaje(chat_id, "⚠️ No hay un usuario asignado. Usa /responder <id_usuario> o responde con <id>: mensaje.")
                return {"status": "ok"}

    # --- 2. Comandos del usuario ---
    if texto.startswith("/"):
        respuesta = manejar_comando(texto, chat_id)
        enviar_mensaje(chat_id, respuesta)

        registrar_conversacion(chat_id, mensaje_usuario=texto, respuesta_bot=respuesta)

        if texto.strip().lower() == "/asesor":
            conversaciones_activas[chat_id] = True
            guardar_conversacion(chat_id, texto, "Solicitud de asesor")

            for admin_id in ADMIN_CHAT_IDS:
                enviar_mensaje(admin_id, f"📞 Usuario {chat_id} ha solicitado hablar con un asesor.")

        elif texto.strip().lower() == "/cerrar":
            cerrar_conversacion(chat_id)
            guardar_conversacion(chat_id, texto, "Cierre de conversación")

        elif texto.strip().lower() == "/usuarios" and chat_id in ASESORES_CHAT_IDS:
            if conversaciones_activas:
                lista = "\n".join([f"👤 Usuario activo: {uid}" for uid in conversaciones_activas.keys()])
                enviar_mensaje(chat_id, f"📋 Usuarios en conversación activa:\n\n{lista}")
            else:
                enviar_mensaje(chat_id, "📜 No hay usuarios activos actualmente.")
            return {"status": "ok"}

        elif texto.strip().lower().startswith("/responder ") and chat_id in ASESORES_CHAT_IDS:
            try:
                partes = texto.split()
                if len(partes) != 2:
                    raise ValueError("Formato incorrecto")

                id_usuario = int(partes[1].strip())

                if id_usuario not in conversaciones_activas:
                    enviar_mensaje(chat_id, f"⚠️ El usuario {id_usuario} no tiene una conversación activa.")
                else:
                    asignar_asesor(id_usuario, chat_id)
                    enviar_mensaje(
                        chat_id,
                        f"✏️ Puedes responder escribiendo el siguiente mensaje:\n\n{id_usuario}: Tu respuesta aquí"
                    )
            except Exception:
                enviar_mensaje(chat_id, "❌ Uso incorrecto. Formato correcto:\n/responder <id_usuario>")
            return {"status": "ok"}

# --- 3. Conversación activa con asesor ---
    if chat_id not in ASESORES_CHAT_IDS:  # Es un cliente hablando
        if esta_activa(chat_id):
            logging.info(f"💬 Usuario {chat_id} escribió: {texto}")
            guardar_conversacion(chat_id, texto, "Mensaje del usuario")

            registrar_conversacion(chat_id, mensaje_usuario=texto)

            asesor_id = obtener_asesor(chat_id)
            if asesor_id:
                enviar_mensaje(asesor_id, f"👤 Usuario {chat_id} dijo:\n{texto}")
            else:
                reenviar_al_asesor(chat_id, texto)  # fallback por si no hay emparejamiento
        else:
            enviar_mensaje(
                chat_id,
                "🤖 No hay una conversación activa. Usa /asesor para hablar con alguien o /ayuda para ver opciones."
            )
            registrar_conversacion(chat_id, mensaje_usuario=texto, respuesta_bot="No hay conversación activa.")
        return {"status": "ok"}

    # --- 4. Fallback cuando no hay conversación ---
    respuesta = manejar_comando("/ayuda", chat_id)
    enviar_mensaje(chat_id, "🤖 No hay una conversación activa. Usa /asesor para hablar con alguien o /ayuda para ver opciones.")
    registrar_conversacion(chat_id, mensaje_usuario=texto, respuesta_bot=respuesta)
    return {"status": "ok"}