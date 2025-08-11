# app/routes/email.py
import smtplib
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os

router = APIRouter()

class Producto(BaseModel):
    nombre: str
    cantidad: int
    precio: float

class Cliente(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    ciudad: str
    referencia: str
    codigoPostal: str

class PedidoEmail(BaseModel):
    cliente: Cliente
    productos: List[Producto]
    total: float

@router.post("/enviar-resumen")
def enviar_resumen(pedido: PedidoEmail):
    cliente = pedido.cliente
    productos = pedido.productos
    total = pedido.total

    productos_texto = "\n".join([
        f"- {p.nombre} x {p.cantidad} = ${p.precio * p.cantidad:.2f}"
        for p in productos
    ])

    contenido = f"""\
Gracias por tu compra, {cliente.nombre}!

Resumen de tu pedido:

{productos_texto}

Total: ${total:.2f}

Datos de envío:
Dirección: {cliente.direccion}, {cliente.ciudad}
Referencia: {cliente.referencia}
Código Postal: {cliente.codigoPostal}
Teléfono: {cliente.telefono}
"""

    msg = MIMEText(contenido)
    msg["Subject"] = "Resumen de tu pedido"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = cliente.email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_APP_PASSWORD"))
            server.send_message(msg)
        return {"mensaje": "Correo enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))