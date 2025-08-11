from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.tienda import get_db_session
from app import schemas
from app.db import models

router = APIRouter()

@router.post("/api/registrar-pedido")
def registrar_pedido(data: schemas.RegistroPedido, db: Session = Depends(get_db_session)):
    cliente_data = data.cliente

    # Guardar cliente si no existe y desea guardar datos
    if cliente_data.guardar_datos:
        cliente_existente = db.query(models.Cliente).filter_by(numero_identificacion=cliente_data.numero_identificacion).first()
        if not cliente_existente:
            nuevo_cliente = models.Cliente(**cliente_data.dict(exclude={'guardar_datos'}))
            db.add(nuevo_cliente)

    # Calcular total
    total = 0
    for item in data.productos:
        producto = db.query(models.Producto).filter_by(id=item.id).first()
        if not producto or producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Producto ID {item.id} no disponible")
        total += producto.valor_venta * item.cantidad
        producto.stock -= item.cantidad

    # Crear pedido
    pedido = models.Pedido(
        cliente_id=cliente_data.numero_identificacion,
        total=total
    )
    db.add(pedido)
    db.commit()
    return {"mensaje": "Pedido registrado correctamente", "total": total}