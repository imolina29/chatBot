import re

def limpiar_texto_unicode(texto: str) -> str:
    """
    Elimina caracteres inválidos (surrogates, no imprimibles) que causan errores en UTF-8.
    """
    if not texto:
        return ""
    # Elimina surrogates y reemplaza por vacío
    texto_limpio = re.sub(r'[\ud800-\udfff]', '', texto)
    return texto_limpio