from utils.logger import guardar_conversacion
import json
from datetime import datetime
import os

LOG_FILE = "historial_conversaciones.jsonl"

def guardar_conversacion(chat_id: int, pregunta: str, respuesta: str):
    conversacion = {
        "timestamp": datetime.now().isoformat(),
        "chat_id": chat_id,
        "pregunta": pregunta,
        "respuesta": respuesta
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(conversacion, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"⚠️ Error al guardar conversación: {e}")