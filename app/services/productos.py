from sqlalchemy.orm import Session
from app.db.models import Producto
from typing import List
from sqlalchemy import or_

def buscar_productos(texto_usuario: str, db: Session) -> List[Producto]:
    texto_busqueda = texto_usuario.lower().strip()
    palabras = texto_busqueda.split()

    # Creamos una lista de condiciones: una por cada palabra
    condiciones = [Producto.descripcion_producto.ilike(f"%{palabra}%") for palabra in palabras]

    productos = db.query(Producto).filter(or_(*condiciones)).all()

    return productos