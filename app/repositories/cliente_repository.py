from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.cliente import Cliente
from app.infrastructure.models import ClienteORM


# Convierte una fila de la base de datos (ORM) en la entidad de dominio.
def _a_dominio(fila: ClienteORM) -> Cliente:
    return Cliente(
        id_cliente=fila.id_cliente,
        nombre=fila.nombre,
        apellido=fila.apellido,
        correo=fila.correo,
        telefono=fila.telefono,
        estado=fila.estado,
    )


def obtener_todos(db: Session) -> list[Cliente]:
    filas = db.scalars(select(ClienteORM).order_by(ClienteORM.id_cliente)).all()
    return [_a_dominio(fila) for fila in filas]


def obtener_por_id(db: Session, id_cliente: int) -> Optional[Cliente]:
    fila = db.get(ClienteORM, id_cliente)
    if fila is None:
        return None
    return _a_dominio(fila)


def obtener_por_correo(db: Session, correo: str) -> Optional[Cliente]:
    fila = db.scalars(select(ClienteORM).where(ClienteORM.correo == correo)).first()
    if fila is None:
        return None
    return _a_dominio(fila)


def crear(db: Session, cliente: Cliente) -> Cliente:
    fila = ClienteORM(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        correo=cliente.correo,
        telefono=cliente.telefono,
        estado=cliente.estado,
    )
    db.add(fila)
    db.flush()  # PostgreSQL genera el ID
    cliente.id_cliente = fila.id_cliente
    return cliente


def actualizar(db: Session, cliente_actualizado: Cliente) -> Optional[Cliente]:
    fila = db.get(ClienteORM, cliente_actualizado.id_cliente)
    if fila is None:
        return None
    fila.nombre = cliente_actualizado.nombre
    fila.apellido = cliente_actualizado.apellido
    fila.correo = cliente_actualizado.correo
    fila.telefono = cliente_actualizado.telefono
    fila.estado = cliente_actualizado.estado
    db.flush()
    return cliente_actualizado


def eliminar(db: Session, id_cliente: int) -> Optional[Cliente]:
    fila = db.get(ClienteORM, id_cliente)
    if fila is None:
        return None
    cliente = _a_dominio(fila)
    db.delete(fila)
    db.flush()  # si tiene arriendos, la base de datos lo rechaza (RESTRICT)
    return cliente
