from fastapi import APIRouter, HTTPException
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services.categoria_service import (
    categoria_service,
    CategoriaYaExisteError,
    CategoriaNoEncontradaError,
)


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.get("/", response_model=list[CategoriaResponse])
def obtener_categorias():
    return categoria_service.listar_categorias()


@router.get("/{id_categoria}", response_model=CategoriaResponse)
def obtener_categoria(id_categoria: int):
    try:
        return categoria_service.obtener_categoria(id_categoria)
    except CategoriaNoEncontradaError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(datos: CategoriaCreate):
    try:
        return categoria_service.crear_categoria(datos)
    except CategoriaYaExisteError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar_categoria(id_categoria: int, datos: CategoriaUpdate):
    try:
        return categoria_service.actualizar_categoria(id_categoria, datos)
    except CategoriaNoEncontradaError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except CategoriaYaExisteError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.delete("/{id_categoria}", status_code=204)
def eliminar_categoria(id_categoria: int):
    try:
        categoria_service.eliminar_categoria(id_categoria)
    except CategoriaNoEncontradaError as error:
        raise HTTPException(status_code=404, detail=str(error))