from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.arriendo import Arriendo
from app.infrastructure.models import ArriendoORM


def _a_dominio(fila: ArriendoORM) -> Arriendo:
    return Arriendo(
        id_arriendo=fila.id_arriendo,
        id_cliente=fila.id_cliente,
        id_videojuego=fila.id_videojuego,
        fecha_arriendo=fila.fecha_arriendo,
        fecha_devolucion=fila.fecha_devolucion,
        estado=fila.estado,
    )


class ArriendoRepository:
    """Repository de Arriendo usando la base de datos (PostgreSQL)."""

    def crear(self, db: Session, arriendo: Arriendo) -> Arriendo:
        fila = ArriendoORM(
            id_cliente=arriendo.id_cliente,
            id_videojuego=arriendo.id_videojuego,
            fecha_arriendo=arriendo.fecha_arriendo,
            fecha_devolucion=arriendo.fecha_devolucion,
            estado=arriendo.estado,
        )
        db.add(fila)
        db.flush()  # PostgreSQL genera el ID
        arriendo.id_arriendo = fila.id_arriendo
        return arriendo

    def listar(self, db: Session) -> list[Arriendo]:
        filas = db.scalars(
            select(ArriendoORM).order_by(ArriendoORM.id_arriendo)
        ).all()
        return [_a_dominio(fila) for fila in filas]

    def buscar_por_id(self, db: Session, id_arriendo: int) -> Optional[Arriendo]:
        fila = db.get(ArriendoORM, id_arriendo)
        if fila is None:
            return None
        return _a_dominio(fila)

    def buscar_activo_por_cliente(
        self, db: Session, id_cliente: int
    ) -> Optional[Arriendo]:
        fila = db.scalars(
            select(ArriendoORM).where(
                ArriendoORM.id_cliente == id_cliente,
                ArriendoORM.estado == "Activo",
            )
        ).first()
        if fila is None:
            return None
        return _a_dominio(fila)

    def actualizar(self, db: Session, arriendo: Arriendo) -> Optional[Arriendo]:
        fila = db.get(ArriendoORM, arriendo.id_arriendo)
        if fila is None:
            return None
        fila.fecha_arriendo = arriendo.fecha_arriendo
        fila.fecha_devolucion = arriendo.fecha_devolucion
        fila.estado = arriendo.estado
        db.flush()
        return arriendo

    def eliminar(self, db: Session, id_arriendo: int) -> Optional[Arriendo]:
        fila = db.get(ArriendoORM, id_arriendo)
        if fila is None:
            return None
        arriendo = _a_dominio(fila)
        db.delete(fila)
        db.flush()
        return arriendo


arriendo_repository = ArriendoRepository()
