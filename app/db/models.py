from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from datetime import datetime
from app.db.tienda import Base
from sqlalchemy.orm import relationship

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
    categoria = Column(String, default="General")
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)

    items = relationship("ItemPedido", back_populates="producto")

class Cliente(Base):
    __tablename__ = "clientes"

    numero_identificacion = Column(String, primary_key=True)
    nombres = Column(String)
    apellidos = Column(String)
    correo = Column(String)
    telefono = Column(String)
    ciudad = Column(String)
    direccion = Column(String)
    codigo_postal = Column(String)
    referencia = Column(String)

    pedidos = relationship("Pedido", back_populates="cliente")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(String, ForeignKey("clientes.numero_identificacion"))
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)

    cliente = relationship("Cliente", back_populates="pedidos")
    items = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "items_pedido"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto", back_populates="items")