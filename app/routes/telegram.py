# app/routes/telegram.py

from fastapi import APIRouter, Request
import logging
from app.services.bot import responder_fallback
from app.services.history import guardar_conversacion
from app.services.bot import generar_respuesta, manejar_comando
from app.services.telegram import enviar_mensaje_telegram

router = APIRouter()
global bot_activo
@router.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    logging.info(f"📨 Mensaje recibido: {message} de chat_id: {chat_id}")

    if message and chat_id:
        if message.startswith("/"):
            respuesta = manejar_comando(message, chat_id)
        else:
            if bot_activo:
                respuesta = await generar_respuesta(message)
            else:
                respuesta = responder_fallback(message)

        enviar_mensaje_telegram(chat_id, respuesta)
        guardar_conversacion(chat_id, message, respuesta)

    return {"status": "ok"}