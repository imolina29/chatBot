# app/utils/storage.py

import json
import logging
from datetime import datetime

HISTORIAL_PATH = "conversaciones.jsonl"

def guardar_conversacion(chat_id: int, user_input: str, respuesta: str) -> None:
    entrada = {
        "timestamp": datetime.now().isoformat(),
        "chat_id": chat_id,
        "mensaje_usuario": user_input,
        "respuesta_bot": respuesta
    }

    try:
        with open(HISTORIAL_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        logging.info(f"📝 Conversación guardada para chat_id {chat_id}")
    except Exception as e:
        logging.error(f"❌ Error al guardar conversación: {e}")