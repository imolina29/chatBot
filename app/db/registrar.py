# app/db/registrar.py

from datetime import datetime
from app.db.models import Conversacion
from app.db.init_db import SessionLocal
from utils.strings import limpiar_texto_unicode

def registrar_conversacion(chat_id: int, mensaje_usuario: str = "", respuesta_bot: str = ""):
    db = SessionLocal()
    try:
        mensaje_usuario = limpiar_texto_unicode(mensaje_usuario)
        respuesta_bot = limpiar_texto_unicode(respuesta_bot)
        nueva_conversacion = Conversacion(
            chat_id=chat_id,
            mensaje_usuario=mensaje_usuario,
            respuesta_bot=respuesta_bot,
            timestamp=datetime.now()
        )
        db.add(nueva_conversacion)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error al registrar conversación: {e}")
    finally:
        db.close()