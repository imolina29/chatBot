# app/routes/product.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db_session
from app.db.models import Producto
from pydantic import BaseModel

router = APIRouter(prefix="/api/productos", tags=["productos"])

# Schemas
class ProductoSchema(BaseModel):
    descripcion_producto: str
    cantidad: int
    valor_unitario: float
    valor_venta: float
    categoria: Optional[str] = "General"
    stock: Optional[int] = 0
    activo: Optional[bool] = True

class ProductoUpdateSchema(ProductoSchema):
    pass

class ProductoResponseSchema(ProductoSchema):
    id: int
    class Config:
        orm_mode = True


# Crear producto
@router.post("/", response_model=dict)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db_session)):
    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "✅ Producto creado correctamente", "producto_id": nuevo.id}


# Listar todos los productos
@router.get("/", response_model=List[ProductoResponseSchema])
def listar_productos(db: Session = Depends(get_db_session)):
    productos = db.query(Producto).all()
    return productos


# Obtener producto por ID
@router.get("/{producto_id}", response_model=ProductoResponseSchema)
def obtener_producto(producto_id: int, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


# Actualizar producto
@router.put("/{producto_id}", response_model=dict)
def actualizar_producto(producto_id: int, datos: ProductoUpdateSchema, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in datos.dict().items():
        setattr(producto, key, value)
    db.commit()
    return {"mensaje": "✏️ Producto actualizado correctamente"}


# Eliminar producto
@router.delete("/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "🗑️ Producto eliminado"}