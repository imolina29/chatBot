# app/utils/auth.py

from fastapi import Request, HTTPException, status
from app.config import ADMIN_CHAT_IDS

async def verificar_autenticacion(request: Request):
    """
    Extrae el chat_id del cuerpo del request y valida si es un administrador.
    """
    try:
        data = await request.json()
        chat_id = data.get("message", {}).get("chat", {}).get("id")
        if int(chat_id) not in ADMIN_CHAT_IDS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a esta funcionalidad."
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solicitud inválida o faltan datos."
        )