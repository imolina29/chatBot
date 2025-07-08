# app/utils/conversaciones.py

from typing import Dict
from datetime import datetime
import logging

from app.config.constants import ASESOR_CHAT_ID
from app.services.bot import enviar_mensaje  # Solo uno, el válido

conversaciones_activas: Dict[int, bool] = {}

def guardar_conversacion(chat_id: int, mensaje: str, contexto: str):
    """
    Guarda o loguea una conversación con propósito de trazabilidad.
    """
    logging.info(f"[{datetime.now()}] ({contexto}) {chat_id}: {mensaje}")

def cerrar_conversacion(chat_id: int):
    """
    Cierra la conversación con un usuario.
    """
    conversaciones_activas.pop(chat_id, None)
    enviar_mensaje(chat_id, "✅ La conversación ha sido cerrada. ¡Gracias por comunicarte!")

def reenviar_al_asesor(chat_id: int, texto: str):
    """
    Reenvía automáticamente al asesor el mensaje del usuario.
    """
    try:
        mensaje = f"🆕 Mensaje de usuario {chat_id}: {texto}"
        enviar_mensaje(ASESOR_CHAT_ID, mensaje)
    except Exception as e:
        logging.error(f"❌ Error reenviando al asesor: {e}")

def activar_conversacion(chat_id: int):
    conversaciones_activas[chat_id] = True

def esta_activa(chat_id: int) -> bool:
    return conversaciones_activas.get(chat_id, False)

def cerrar_conversacion(chat_id: int):
    conversaciones_activas.pop(chat_id, None)

# Diccionarios para emparejar cliente con asesor y viceversa
emparejamientos = {}
emparejamientos_inverso = {}

def asignar_asesor(cliente_id: int, asesor_id: int):
    emparejamientos[cliente_id] = asesor_id
    emparejamientos_inverso[asesor_id] = cliente_id
    conversaciones_activas[cliente_id] = True

def obtener_asesor(cliente_id: int) -> int:
    return emparejamientos.get(cliente_id)

def obtener_cliente(asesor_id: int) -> int:
    for cliente, asesor in emparejamientos.items():
        if asesor == asesor_id:
            return cliente
    return None

def eliminar_emparejamiento(chat_id: int):
    emparejamientos.pop(chat_id, None)
    # eliminar también si es asesor
    clientes = [k for k, v in emparejamientos.items() if v == chat_id]
    for c in clientes:
        emparejamientos.pop(c, None)

def cerrar_conversacion(cliente_id: int):
    asesor_id = emparejamientos.pop(cliente_id, None)
    if asesor_id:
        emparejamientos_inverso.pop(asesor_id, None)
    conversaciones_activas.pop(cliente_id, None)

def esta_activa(cliente_id: int) -> bool:
    return cliente_id in conversaciones_activas