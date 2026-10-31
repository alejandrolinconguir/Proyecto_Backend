from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    CategoriaPaginadaResponse,
)
from app.schemas.error import respuestas_error
from app.services.categoria_service import categoria_service


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.get(
    "/",
    response_model=CategoriaPaginadaResponse,
    responses=respuestas_error(400, 422),
)
def obtener_categorias(
    estado: Optional[str] = None,
    ordenar_por: str = "id_categoria",
    direccion: str = "asc",
    pagina: int = 1,
    limite: int = 20,
    db: Session = Depends(get_db),
):
    """
    Lista categorías con filtrado, ordenamiento y paginación.

    Ejemplo: GET /categorias/?estado=Activa&ordenar_por=nombre&direccion=asc&pagina=1&limite=10
    """
    # Los parámetros inválidos los valida el service y devuelven 400 con el
    # formato de error del proyecto (se manejan en core/error_handlers.py).
    return categoria_service.listar_categorias_paginadas(
        db,
        estado=estado,
        ordenar_por=ordenar_por,
        direccion=direccion,
        pagina=pagina,
        limite=limite,
    )


@router.get(
    "/{id_categoria}",
    response_model=CategoriaResponse,
    responses=respuestas_error(404, 422),
)
def obtener_categoria(id_categoria: int, db: Session = Depends(get_db)):
    return categoria_service.obtener_categoria(db, id_categoria)


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=201,
    responses=respuestas_error(409, 422),
)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_service.crear_categoria(db, datos)


@router.put(
    "/{id_categoria}",
    response_model=CategoriaResponse,
    responses=respuestas_error(404, 409, 422),
)
def actualizar_categoria(id_categoria: int, datos: CategoriaUpdate, db: Session = Depends(get_db)):
    return categoria_service.actualizar_categoria(db, id_categoria, datos)


@router.delete(
    "/{id_categoria}",
    status_code=204,
    responses=respuestas_error(404, 409, 422),
)
def eliminar_categoria(id_categoria: int, db: Session = Depends(get_db)):
    categoria_service.eliminar_categoria(db, id_categoria)
