from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.tienda import get_db_session
from app.db.models import Producto
from pydantic import BaseModel

router = APIRouter(prefix="/api/productos", tags=["productos"])

# ----------------------------- SCHEMAS -----------------------------

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

class CompraItem(BaseModel):
    id: int
    cantidad: int

# ----------------------------- ENDPOINTS -----------------------------

@router.post("/", response_model=dict)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db_session)):
    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "✅ Producto creado correctamente", "producto_id": nuevo.id}


@router.get("/", response_model=List[ProductoResponseSchema])
def listar_productos(db: Session = Depends(get_db_session)):
    productos = db.query(Producto).all()
    print(f"📦 Productos encontrados: {len(productos)}")
    return productos


@router.get("/{producto_id}", response_model=ProductoResponseSchema)
def obtener_producto(producto_id: int, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=dict)
def actualizar_producto(producto_id: int, datos: ProductoUpdateSchema, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in datos.dict().items():
        setattr(producto, key, value)
    db.commit()
    return {"mensaje": "✏️ Producto actualizado correctamente"}


@router.delete("/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "🗑️ Producto eliminado"}

# -------------------- FINALIZAR COMPRA --------------------

@router.post("/finalizar-compra")
def finalizar_compra(items: List[CompraItem], db: Session = Depends(get_db_session)):
    errores = []
    productos_actualizados = []

    for item in items:
        producto = db.query(Producto).filter(Producto.id == item.id).first()

        if not producto:
            errores.append(f"❌ Producto con ID {item.id} no encontrado")
            continue

        if producto.stock < item.cantidad:
            errores.append(f"⚠️ Stock insuficiente para '{producto.descripcion_producto}' (disponible: {producto.stock})")
            continue

        # Descontar stock
        producto.stock -= item.cantidad
        productos_actualizados.append({
            "id": producto.id,
            "descripcion": producto.descripcion_producto,
            "cantidad_comprada": item.cantidad,
            "stock_restante": producto.stock
        })
        db.add(producto)

    if errores:
        raise HTTPException(status_code=400, detail=errores)

    db.commit()
    return {
        "message": "✅ Compra finalizada exitosamente",
        "productos": productos_actualizados
    }

# -------------------- VALIDAR STOCK INDIVIDUAL --------------------

@router.get("/validar-stock/{producto_id}")
def validar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db_session)):
    producto = db.query(Producto).get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < cantidad:
        return {"disponible": False, "stock": producto.stock, "mensaje": "Stock insuficiente"}
    return {"disponible": True, "stock": producto.stock, "mensaje": "Stock suficiente"}