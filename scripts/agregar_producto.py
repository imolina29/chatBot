# scripts/agregar_producto.py

from app.db.init_db import SessionLocal
from app.db.models import Producto
import random

def agregar_producto():
    session = SessionLocal()

    try:
        descripcion = input("📦 Descripción del producto: ")
        valor_venta = float(input("💰 Valor de venta: "))
        cantidad = int(input("📦 Cantidad en stock: "))
        valor_unitario = float(input("💲 Valor unitario: "))

        producto = Producto(
            descripcion_producto=descripcion,
            valor_venta=valor_venta,
            cantidad=cantidad,
            valor_unitario=valor_unitario
        )

        session.add(producto)
        session.commit()
        print("✅ Producto agregado correctamente.")

    except Exception as e:
        print(f"❌ Error al agregar el producto: {e}")
        session.rollback()

    finally:
        session.close()

def agregar_productos_dummy():
    session = SessionLocal()
    nombres = [
        "Camiseta blanca", "Zapatos deportivos", "Pantalón jeans", "Gorra negra", "Sudadera azul",
        "Bolso de cuero", "Perfume floral", "Reloj digital", "Lentes de sol", "Chaqueta impermeable",
        "Sandalias cómodas", "Bufanda de lana", "Guantes térmicos", "Pijama de algodón", "Camisa formal",
        "Vestido de verano", "Botas de montaña", "Cinturón de cuero", "Gafas de lectura", "Maleta de viaje"
    ]

    try:
        for nombre in nombres:
            producto = Producto(
                descripcion_producto=nombre,
                cantidad=random.randint(5, 50),
                valor_unitario=round(random.uniform(10.0, 80.0), 2),
                valor_venta=round(random.uniform(90.0, 200.0), 2)
            )
            session.add(producto)

        session.commit()
        print("✅ 20 productos dummy agregados correctamente.")

    except Exception as e:
        print(f"❌ Error al agregar productos dummy: {e}")
        session.rollback()

    finally:
        session.close()

if __name__ == "__main__":
    agregar_producto()
   #agregar_productos_dummy()