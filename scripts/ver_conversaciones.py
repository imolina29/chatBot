# scripts/ver_conversaciones.py

from app.db.tienda import SessionLocal
from app.db.models import Conversacion

def mostrar_conversaciones():
    db = SessionLocal()
    conversaciones = db.query(Conversacion).order_by(Conversacion.timestamp.desc()).limit(10).all()
    
    if not conversaciones:
        print("No hay conversaciones registradas aún.")
        return

    for conv in conversaciones:
        print(f"🗨️ Chat ID: {conv.chat_id}")
        print(f"📝 Mensaje usuario: {conv.mensaje_usuario}")
        print(f"🤖 Respuesta bot: {conv.respuesta_bot}")
        print(f"🕒 Fecha y hora: {conv.timestamp}")
        print("-" * 40)

    db.close()

if __name__ == "__main__":
    mostrar_conversaciones()