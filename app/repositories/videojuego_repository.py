from sqlalchemy import select
from sqlalchemy.orm import Session

# Aqui importamos la clase que esta creada dentro del domain
from app.domain.videojuego import Videojuego
from app.infrastructure.models import VideojuegoORM


# Convierte una fila de la base de datos (ORM) en la entidad de dominio.
def _a_dominio(fila: VideojuegoORM) -> Videojuego:
    return Videojuego(
        id_videojuego=fila.id_videojuego,
        titulo=fila.titulo,
        plataforma=fila.plataforma,
        año_lanzamiento=fila.año_lanzamiento,
        id_categoria=fila.id_categoria,
        estado=fila.estado,
    )


# Se ordena por ID para que el listado siempre salga en el mismo orden
# (la base de datos no garantiza orden si no se pide).
def obtener_todos(db: Session) -> list[Videojuego]:
    filas = db.scalars(
        select(VideojuegoORM).order_by(VideojuegoORM.id_videojuego)
    ).all()
    return [_a_dominio(fila) for fila in filas]


def crear(db: Session, videojuego: Videojuego) -> Videojuego:
    fila = VideojuegoORM(
        titulo=videojuego.titulo,
        plataforma=videojuego.plataforma,
        año_lanzamiento=videojuego.año_lanzamiento,
        id_categoria=videojuego.id_categoria,
        estado=videojuego.estado,
    )
    db.add(fila)
    db.flush()  # PostgreSQL genera el ID
    videojuego.id_videojuego = fila.id_videojuego
    return videojuego


# Busca por ID; si no lo encuentra devuelve None
def obtener_por_id(db: Session, id_videojuego: int):
    fila = db.get(VideojuegoORM, id_videojuego)
    if fila is None:
        return None
    return _a_dominio(fila)


# Busca por su ID y guarda los datos nuevos del videojuego.
def actualizar(db: Session, videojuego_actualizado: Videojuego):
    fila = db.get(VideojuegoORM, videojuego_actualizado.id_videojuego)
    if fila is None:
        return None
    fila.titulo = videojuego_actualizado.titulo
    fila.plataforma = videojuego_actualizado.plataforma
    fila.año_lanzamiento = videojuego_actualizado.año_lanzamiento
    fila.id_categoria = videojuego_actualizado.id_categoria
    fila.estado = videojuego_actualizado.estado
    db.flush()
    return videojuego_actualizado


def eliminar(db: Session, id_videojuego: int):
    fila = db.get(VideojuegoORM, id_videojuego)
    # Si no encuentra la ID devuelve None
    if fila is None:
        return None
    videojuego = _a_dominio(fila)
    db.delete(fila)
    db.flush()  # si tiene arriendos, la base de datos lo rechaza (RESTRICT)
    return videojuego
