# utils/comandos.py
import logging
from utils.creditos import obtener_creditos_openai
from app.config import ADMIN_CHAT_ID

# Esta variable la importamos del main (o podrías mover la lógica aquí si prefieres)
bot_activo = True

def set_bot_activo(valor: bool):
    global bot_activo
    bot_activo = valor

def get_bot_activo():
    return bot_activo

# Handler para /estado
def comando_estado(chat_id: int) -> str:
    return "✅ El bot está activo." if get_bot_activo() else "🚫 El bot está desactivado temporalmente."

# Handler para /ayuda
def comando_ayuda(chat_id: int) -> str:
    return (
        "📖 *Comandos disponibles:*\n"
        "/estado - Ver estado del bot\n"
        "/ayuda - Mostrar esta ayuda\n"
        "/reactivar - Reactivar el bot (solo admin)"
    )

# Handler para /reactivar
def comando_reactivar(chat_id: int) -> str:
    if str(chat_id) == str(ADMIN_CHAT_ID):
        set_bot_activo(True)
        return "✅ Bot reactivado manualmente por el administrador."
    else:
        return "❌ No tienes permisos para usar este comando."

#handler para /creditos de openAI
def comando_creditos(chat_id: int) -> str:
    try:
         return obtener_creditos_openai()
    
    except Exception as e:
        logging.error(f"Error al consultar créditos: {e}")
        return "❌ No se pudo obtener la información de créditos en este momento."
    
# Diccionario de comandos
comandos_handler = {
    "/estado": comando_estado,
    "/ayuda": comando_ayuda,
    "/reactivar": comando_reactivar,
    "/creditos": comando_creditos
}

# Función que maneja cualquier comando recibido
def manejar_comando(comando: str, chat_id: int) -> str:
    handler = comandos_handler.get(comando)
    if handler:
        return handler(chat_id)
    else:
        return "🤖 Comando no reconocido. Usa /ayuda para ver las opciones disponibles."