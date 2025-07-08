# state.py
usuarios_en_espera = set()

def agregar_usuario_espera(chat_id: int):
    usuarios_en_espera.add(chat_id)

def quitar_usuario_espera(chat_id: int):
    usuarios_en_espera.discard(chat_id)

def esta_en_espera(chat_id: int) -> bool:
    return chat_id in usuarios_en_espera