from fastapi import APIRouter
from app.schemas.categoria import (CategoriaCreate,CategoriaUpdate,CategoriaResponse)
from app.services.categoria_service import categoria_service


router = APIRouter(prefix="/categorias",tags=["Categorias"])

@router.get("/", response_model=list[CategoriaResponse])
def obtener_categorias():
    return categoria_service.listar_categorias()


@router.get("/{id_categoria}", response_model=CategoriaResponse)
def obtener_categoria(id_categoria: int):
    return categoria_service.obtener_categoria(id_categoria)


@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(datos: CategoriaCreate):
    return categoria_service.crear_categoria(datos)


@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar_categoria(id_categoria: int, datos: CategoriaUpdate):
    return categoria_service.actualizar_categoria(id_categoria, datos)


@router.delete("/{id_categoria}", status_code=204)
def eliminar_categoria(id_categoria: int):
    categoria_service.eliminar_categoria(id_categoria)