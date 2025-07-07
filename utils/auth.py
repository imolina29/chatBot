from fastapi import Request, HTTPException
from app.config import API_SECRET_KEY

async def verificar_autenticacion(request: Request):
    token = request.headers.get("X-API-Key")
    if not token or token != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="No autorizado")