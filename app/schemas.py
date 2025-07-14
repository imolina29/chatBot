from pydantic import BaseModel
from typing import Optional

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