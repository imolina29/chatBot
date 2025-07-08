import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Lista de chat_id de asesores
ASESORES_CHAT_IDS = list(map(int, os.getenv("ASESORES_CHAT_IDS", "").split(",")))

# Archivo temporal para almacenar las conversaciones activas
CONVERSACIONES_FILE = "conversaciones_activas.json"

# Cargar conversaciones activas desde archivo
def cargar_conversaciones():
    if not os.path.exists(CONVERSACIONES_FILE):
        return {}
    try:
        with open(CONVERSACIONES_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.warning(f"⚠️ No se pudo cargar archivo de conversaciones: {e}")
        return {}

# Guardar conversaciones activas en archivo
def guardar_conversaciones(data):
    try:
        with open(CONVERSACIONES_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"❌ Error guardando conversaciones activas: {e}")

# Verifica si el chat_id es de un asesor autorizado
def es_asesor(chat_id: int) -> bool:
    return chat_id in ASESORES_CHAT_IDS

# Registrar una nueva conversación activa
def registrar_conversacion_activa(chat_id_usuario: int):
    conversaciones = cargar_conversaciones()

    # Buscar un asesor disponible
    for asesor_id in ASESORES_CHAT_IDS:
        if str(asesor_id) not in conversaciones.values():
            conversaciones[str(chat_id_usuario)] = asesor_id
            guardar_conversaciones(conversaciones)
            logging.info(f"📞 Solicitud de asesor humano por chat_id: {chat_id_usuario}")
            return asesor_id

    logging.warning("⚠️ No hay asesores disponibles.")
    return None

# Obtener el chat_id del usuario que está conversando con el asesor
def obtener_usuario_para_asesor(chat_id_asesor: int):
    conversaciones = cargar_conversaciones()
    for usuario_id, asesor_id in conversaciones.items():
        if int(asesor_id) == chat_id_asesor:
            return int(usuario_id)
    return None

# Cerrar conversación activa para un asesor
def cerrar_conversacion_activa(chat_id_asesor: int):
    conversaciones = cargar_conversaciones()
    nueva_data = {
        usuario_id: asesor_id
        for usuario_id, asesor_id in conversaciones.items()
        if int(asesor_id) != chat_id_asesor
    }
    guardar_conversaciones(nueva_data)
    logging.info(f"📴 Conversación cerrada para asesor {chat_id_asesor}")