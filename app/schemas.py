from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, EmailStr
from typing import List

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

class ProductoCompra(BaseModel):
    id: int
    cantidad: int

class ClienteCreate(BaseModel):
    numero_identificacion: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str
    ciudad: str
    direccion: str
    codigo_postal: str
    referencia: str
    guardar_datos: bool

class RegistroPedido(BaseModel):
    cliente: ClienteCreate
    productos: List[ProductoCompra]