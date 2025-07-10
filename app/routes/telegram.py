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
    obtener_cliente,
    obtener_cliente_en_conversacion
)
from app.config import ASESORES_CHAT_IDS
from app.config.constants import ASESOR_CHAT_ID
from app.config import ADMIN_CHAT_IDS
from app.db.registrar import registrar_conversacion
from app.db.database import get_db_session

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    logging.info("Mensaje recibido: %s", data)

    mensaje = data.get("message", {})
    chat_id = mensaje.get("chat", {}).get("id")
    texto = mensaje.get("text", "")

    if not chat_id or not texto:
        logging.warning("\u274c Mensaje sin chat_id o texto v\u00e1lido.")
        return {"status": "error"}

    # --- 1. Si el asesor responde ---
    if chat_id in ASESORES_CHAT_IDS:
        if ":" in texto:
            try:
                partes = texto.split(":", 1)
                id_usuario = int(partes[0].strip())
                respuesta = partes[1].strip()

                enviar_mensaje(id_usuario, f"\ud83e\uddd1\u200d\ud83d\udcbc Asesor: {respuesta}")
                asignar_asesor(id_usuario, chat_id)
                guardar_conversacion(id_usuario, texto, "Respuesta del asesor")
                registrar_conversacion(id_usuario, respuesta_bot=respuesta)
                return {"status": "ok"}

            except Exception as e:
                logging.error(f"\u274c Error reenviando respuesta del asesor: {e}")
                enviar_mensaje(chat_id, "\u274c Formato incorrecto. Usa:\n\n`<ID_usuario>: respuesta`")
                return {"status": "error"}

        else:
            cliente_id = obtener_cliente(chat_id)
            if cliente_id:
                enviar_mensaje(cliente_id, f"\ud83e\uddd1\u200d\ud83d\udcbc Asesor: {texto}")
                guardar_conversacion(cliente_id, texto, "Respuesta del asesor")
                registrar_conversacion(cliente_id, respuesta_bot=texto)
                return {"status": "ok"}
            else:
                enviar_mensaje(chat_id, "\u26a0\ufe0f No hay un usuario asignado. Usa /responder <id_usuario> o responde con <id>: mensaje.")
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
                enviar_mensaje(admin_id, f"\ud83d\udcde Usuario {chat_id} ha solicitado hablar con un asesor.")
            return {"status": "ok"}

        elif texto.strip().lower() == "/cerrar":
            if chat_id in ASESORES_CHAT_IDS:
                cliente_id = obtener_cliente(chat_id)
                if cliente_id:
                    cerrar_conversacion(cliente_id)
                    enviar_mensaje(cliente_id, "\u2705 La conversaci\u00f3n ha sido cerrada por el asesor.")
                    enviar_mensaje(chat_id, f"\u2705 Conversaci\u00f3n con el usuario {cliente_id} cerrada correctamente.")
                else:
                    enviar_mensaje(chat_id, "\u26a0\ufe0f No tienes un cliente asignado actualmente.")
            else:
                asesor_id = obtener_asesor(chat_id)
                cerrar_conversacion(chat_id)
                enviar_mensaje(chat_id, "\u2705 La conversaci\u00f3n ha sido cerrada.")
                if asesor_id:
                    enviar_mensaje(asesor_id, f"\ud83d\udd15 El usuario {chat_id} ha cerrado la conversaci\u00f3n.")

            guardar_conversacion(chat_id, texto, "Cierre de conversaci\u00f3n")
            return {"status": "ok"}  # \ud83d\udd1d Prevenir pasos duplicados

        elif texto.strip().lower() == "/usuarios" and chat_id in ASESORES_CHAT_IDS:
            if conversaciones_activas:
                lista = "\n".join([f"\ud83d\udc64 Usuario activo: {uid}" for uid in conversaciones_activas.keys()])
                enviar_mensaje(chat_id, f"\ud83d\udccb Usuarios en conversaci\u00f3n activa:\n\n{lista}")
            else:
                enviar_mensaje(chat_id, "\ud83d\udcdc No hay usuarios activos actualmente.")
            return {"status": "ok"}

        elif texto.strip().lower().startswith("/responder ") and chat_id in ASESORES_CHAT_IDS:
            try:
                partes = texto.split()
                if len(partes) != 2:
                    raise ValueError("Formato incorrecto")

                id_usuario = int(partes[1].strip())

                if id_usuario not in conversaciones_activas:
                    enviar_mensaje(chat_id, f"\u26a0\ufe0f El usuario {id_usuario} no tiene una conversaci\u00f3n activa.")
                else:
                    asignar_asesor(id_usuario, chat_id)
                    enviar_mensaje(
                        chat_id,
                        f"\u270f\ufe0f Puedes responder escribiendo el siguiente mensaje:\n\n{id_usuario}: Tu respuesta aqu\u00ed"
                    )
            except Exception:
                enviar_mensaje(chat_id, "\u274c Uso incorrecto. Formato correcto:\n/responder <id_usuario>")
        return {"status": "ok"}

    # --- 3. Cliente con conversaci\u00f3n activa ---
    if chat_id not in ASESORES_CHAT_IDS:
        if esta_activa(chat_id):
            asesor_id = obtener_asesor(chat_id)
            if asesor_id:
                reenviar_al_asesor(chat_id, texto)
                guardar_conversacion(chat_id, texto, "Mensaje del cliente (dirigido al asesor)")
                registrar_conversacion(chat_id, mensaje_usuario=texto)
                return {"status": "ok"}  # \ud83d\udd1d No continuar con l\u00f3gica de productos

    # --- 4. B\u00fasqueda de productos sin conversaci\u00f3n activa ---
    if not texto.startswith("/") and chat_id not in ASESORES_CHAT_IDS and not esta_activa(chat_id):
        try:
            from app.services.productos import buscar_productos
            from app.db.database import SessionLocal
            db = SessionLocal()
            productos = buscar_productos(texto, db)

            if productos:
                respuesta = "\ud83d\udd0e Productos encontrados:\n\n"
                for producto in productos:
                    respuesta += (
                        f"\ud83d\udce6 {producto.descripcion_producto}\n"
                        f"\ud83d\udcb0 Precio: ${producto.valor_venta:.2f}\n\n"
                    )
            else:
                respuesta = "\ud83d\ude15 No encontr\u00e9 ning\u00fan producto con ese nombre. Puedes intentar con otra palabra o escribir /productos."

            enviar_mensaje(chat_id, respuesta)
            registrar_conversacion(chat_id, mensaje_usuario=texto, respuesta_bot=respuesta)
            return {"status": "ok"}

        except Exception as e:
            logging.warning(f"\u274c Error al buscar productos: {e}")
            reenviar_al_asesor(chat_id, texto)
            return {"status": "ok"}

    # --- 5. Fallback final ---
    respuesta = manejar_comando("/ayuda", chat_id)
    enviar_mensaje(chat_id, "\ud83e\udd16 No hay una conversaci\u00f3n activa. Usa /asesor para hablar con alguien o /ayuda para ver opciones.")
    registrar_conversacion(chat_id, mensaje_usuario=texto, respuesta_bot=respuesta)
    return {"status": "ok"}