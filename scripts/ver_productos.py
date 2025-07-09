# scripts/ver_productos.py

from app.db.init_db import SessionLocal
from app.db.models import Producto

def ver_productos():
    session = SessionLocal()
    try:
        productos = session.query(Producto).all()
        if not productos:
            print("📭 No hay productos registrados.")
            return

        print("\n📦 Lista de productos registrados:\n")
        for p in productos:
            print(f"""
🆔 ID: {p.id}
📄 Descripción: {p.descripcion_producto}
📦 Cantidad: {p.cantidad}
💰 Valor unitario: {p.valor_unitario:,.2f}
🛒 Valor venta: {p.valor_venta:,.2f}
{"-"*40}
            """)
    finally:
        session.close()

if __name__ == "__main__":
    ver_productos()