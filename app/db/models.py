from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime
from .database import Base

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, index=True)
    mensaje_usuario = Column(Text)
    respuesta_bot = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion_producto = Column(String(255), nullable=False)
    cantidad = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    valor_venta = Column(Float, nullable=False)
        # ✅ Nuevas columnas
    categoria = Column(String, default="General")
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)