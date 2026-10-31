from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.categoria import Categoria
from app.infrastructure.models import CategoriaORM


def _a_dominio(fila: CategoriaORM) -> Categoria:
    return Categoria(
        id_categoria=fila.id_categoria,
        nombre=fila.nombre,
        descripcion=fila.descripcion,
        edad_minima=fila.edad_minima,
        estado=fila.estado,
    )


class CategoriaRepository:
    """
    Repository de Categoria: maneja el acceso a la base de datos.

    No contiene lógica de negocio, solo operaciones de guardar/buscar/
    listar/eliminar. Recibe la sesión de la base de datos en cada método.
    """

    def crear(self, db: Session, categoria: Categoria) -> Categoria:
        fila = CategoriaORM(
            nombre=categoria.nombre,
            descripcion=categoria.descripcion,
            edad_minima=categoria.edad_minima,
            estado=categoria.estado,
        )
        db.add(fila)
        db.flush()  # PostgreSQL genera el ID
        categoria.id_categoria = fila.id_categoria
        return categoria

    def listar(self, db: Session) -> list[Categoria]:
        filas = db.scalars(
            select(CategoriaORM).order_by(CategoriaORM.id_categoria)
        ).all()
        return [_a_dominio(fila) for fila in filas]

    def buscar_por_id(self, db: Session, id_categoria: int) -> Optional[Categoria]:
        fila = db.get(CategoriaORM, id_categoria)
        if fila is None:
            return None
        return _a_dominio(fila)

    def buscar_por_nombre(self, db: Session, nombre: str) -> Optional[Categoria]:
        """Usado por el service para verificar duplicados (case-insensitive)."""
        nombre_normalizado = nombre.strip().lower()
        fila = db.scalars(
            select(CategoriaORM).where(
                func.lower(func.trim(CategoriaORM.nombre)) == nombre_normalizado
            )
        ).first()
        if fila is None:
            return None
        return _a_dominio(fila)

    def actualizar(self, db: Session, categoria: Categoria) -> Categoria:
        fila = db.get(CategoriaORM, categoria.id_categoria)
        if fila is None:
            raise ValueError(f"Categoria con id {categoria.id_categoria} no encontrada")
        fila.nombre = categoria.nombre
        fila.descripcion = categoria.descripcion
        fila.edad_minima = categoria.edad_minima
        fila.estado = categoria.estado
        db.flush()
        return categoria

    def eliminar(self, db: Session, id_categoria: int) -> bool:
        fila = db.get(CategoriaORM, id_categoria)
        if fila is None:
            return False
        db.delete(fila)
        db.flush()  # si tiene videojuegos, la base de datos lo rechaza (RESTRICT)
        return True


# Instancia única que usan los services (el estado ya no vive aquí,
# vive en la base de datos).
categoria_repository = CategoriaRepository()
