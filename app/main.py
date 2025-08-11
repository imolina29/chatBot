# app/main.py

from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.config import TELEGRAM_TOKEN, OPENAI_API_KEY
from utils.auth import verificar_autenticacion
from utils.logging_config import configurar_logs
from app.routes.telegram import router as telegram_router
from app.routes.product import router as productos_router
from app.services.telegram import registrar_comandos_telegram
from app.services.bot import enviar_mensaje
from app.services.bot import activar_bot, desactivar_bot
from app.db.init_db import init_db
from app.schemas import CompraItem
from typing import List
import traceback
from app.db.tienda import SessionLocal
from app.db.init_db import SessionLocal
from app.db.models import Producto
from app.routes import pedidos
from app.routes import email

import logging
import json
import sqlite3
from datetime import datetime

# -------------------- Configuración base --------------------
configurar_logs()
init_db()
app = FastAPI()

# -------------------- Middleware CORS (para frontend React) --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Routers --------------------

app.include_router(telegram_router)
app.include_router(productos_router)
app.include_router(pedidos.router)
app.include_router(email.router)

# -------------------- Validación de variables de entorno --------------------

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está definido en el archivo .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está definido en el archivo .env")

# -------------------- Registro automático de comandos --------------------

registrar_comandos_telegram()

# -------------------- Endpoints auxiliares --------------------

@app.get("/status")
def status():
    return {
        "status": "ok",
        "mensaje": "Servidor unificado (bot + frontend) funcionando correctamente"
    }

@app.post("/activar")
async def activar_bot_endpoint(request: Request):
    await verificar_autenticacion(request)
    activar_bot()
    logging.info("✅ Bot reactivado manualmente.")
    return {"status": "ok", "mensaje": "Bot reactivado"}

@app.post("/desactivar")
async def desactivar_bot_endpoint(request: Request):
    await verificar_autenticacion(request)
    desactivar_bot()
    logging.info("⛔ Bot desactivado manualmente.")
    return {"status": "ok", "mensaje": "Bot desactivado"}

# -------------------- Guardar conversaciones --------------------

HISTORIAL_PATH = "conversaciones.jsonl"

def guardar_conversacion(chat_id, user_input, respuesta):
    entrada = {
        "timestamp": datetime.now().isoformat(),
        "chat_id": chat_id,
        "mensaje_usuario": user_input,
        "respuesta_bot": respuesta
    }
    try:
        with open(HISTORIAL_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        logging.info(f"📝 Conversación guardada para chat_id {chat_id}")
    except Exception as e:
        logging.error(f"❌ Error al guardar conversación: {e}")

def activar_bot():
    global bot_activo
    bot_activo = True
    logging.info("✅ Bot activado manualmente desde endpoint.")

def desactivar_bot():
    global bot_activo
    bot_activo = False
    logging.info("⛔ Bot desactivado manualmente desde endpoint.")

# -------------------- Finalizar Compra: Descontar Stock --------------------

@app.post("/api/finalizar-compra")
def finalizar_compra(items: List[CompraItem]):
    print("📦 Datos recibidos en el backend:", items)
    db = SessionLocal()

    try:
        for item in items:
            print(f"🔍 Validando item: {item}")
            producto = db.query(Producto).filter(Producto.id == item.id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto con id {item.id} no encontrado")
            print(f"📊 Stock actual: {producto.stock}")

            if item.cantidad > producto.stock:
                raise HTTPException(status_code=400, detail=f"No hay suficiente stock para el producto ID {item.id}")

            producto.stock -= item.cantidad
            db.add(producto)

        db.commit()
        logging.info("✅ Compra finalizada y stock actualizado.")
        return {"mensaje": "Compra finalizada con éxito"}

    except Exception as e:
        db.rollback()
        logging.error(f"❌ Error al finalizar compra: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

    finally:
        db.close()