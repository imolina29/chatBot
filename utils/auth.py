# app/utils/auth.py

from fastapi import Request, HTTPException, status
from app.config import ADMIN_CHAT_ID

async def verificar_autenticacion(request: Request):
    body = await request.json()
    chat_id = body.get("message", {}).get("chat", {}).get("id")

    if str(chat_id) != str(ADMIN_CHAT_ID):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ No tienes permisos para realizar esta acción."
        )