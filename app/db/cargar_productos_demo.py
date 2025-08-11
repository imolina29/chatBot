# app/db/cargar_productos_demo.py

from app.db.tienda import SessionLocal
from app.db.models import Producto

def cargar_productos_demo():
    db = SessionLocal()

    productos = [
        # Gafas
        Producto(descripcion_producto="Gafas de sol polarizadas", cantidad=30, valor_unitario=10.0, valor_venta=25.99, categoria="Gafas", stock=30),
        Producto(descripcion_producto="Gafas de lectura antirreflejo", cantidad=20, valor_unitario=8.0, valor_venta=19.99, categoria="Gafas", stock=20),
        Producto(descripcion_producto="Gafas estilo vintage", cantidad=15, valor_unitario=12.5, valor_venta=29.99, categoria="Gafas", stock=15),

        # Relojes
        Producto(descripcion_producto="Reloj deportivo resistente al agua", cantidad=25, valor_unitario=18.0, valor_venta=39.99, categoria="Relojes", stock=25),
        Producto(descripcion_producto="Reloj clásico de cuero", cantidad=12, valor_unitario=22.0, valor_venta=49.99, categoria="Relojes", stock=12),

        # Ropa hombre
        Producto(descripcion_producto="Camiseta básica algodón", cantidad=40, valor_unitario=5.0, valor_venta=12.99, categoria="Ropa de hombre", stock=40),
        Producto(descripcion_producto="Pantalón jeans slim fit", cantidad=30, valor_unitario=15.0, valor_venta=34.99, categoria="Ropa de hombre", stock=30),
        Producto(descripcion_producto="Chaqueta impermeable liviana", cantidad=10, valor_unitario=20.0, valor_venta=49.99, categoria="Ropa de hombre", stock=10),

        # Ropa mujer
        Producto(descripcion_producto="Blusa estampada de verano", cantidad=35, valor_unitario=6.0, valor_venta=15.99, categoria="Ropa de mujer", stock=35),
        Producto(descripcion_producto="Falda midi con vuelo", cantidad=18, valor_unitario=10.0, valor_venta=24.99, categoria="Ropa de mujer", stock=18),
        Producto(descripcion_producto="Vestido largo casual", cantidad=20, valor_unitario=13.0, valor_venta=32.99, categoria="Ropa de mujer", stock=20),

        # Calzado
        Producto(descripcion_producto="Zapatillas deportivas unisex", cantidad=22, valor_unitario=18.0, valor_venta=39.99, categoria="Calzado", stock=22),
        Producto(descripcion_producto="Botas impermeables", cantidad=14, valor_unitario=25.0, valor_venta=59.99, categoria="Calzado", stock=14),
        Producto(descripcion_producto="Sandalias de cuero", cantidad=16, valor_unitario=12.0, valor_venta=29.99, categoria="Calzado", stock=16),

        # Accesorios
        Producto(descripcion_producto="Mochila urbana resistente", cantidad=30, valor_unitario=10.0, valor_venta=24.99, categoria="Accesorios", stock=30),
        Producto(descripcion_producto="Cinturón de cuero", cantidad=28, valor_unitario=6.5, valor_venta=14.99, categoria="Accesorios", stock=28),
        Producto(descripcion_producto="Bufanda tejida", cantidad=20, valor_unitario=4.0, valor_venta=11.99, categoria="Accesorios", stock=20),
        Producto(descripcion_producto="Gorra deportiva", cantidad=25, valor_unitario=5.0, valor_venta=12.99, categoria="Accesorios", stock=25),
        Producto(descripcion_producto="Bolso de mano elegante", cantidad=10, valor_unitario=15.0, valor_venta=39.99, categoria="Accesorios", stock=10),
    ]

    try:
        db.add_all(productos)
        db.commit()
        print("✅ Productos ficticios insertados correctamente.")
    except Exception as e:
        db.rollback()
        print("❌ Error al insertar productos:", e)
    finally:
        db.close()

if __name__ == "__main__":
    cargar_productos_demo()