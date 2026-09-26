from fastapi import APIRouter

from app.schemas.arriendo import ArriendoCreate, ArriendoUpdate, ArriendoResponse
from app.services.arriendo_service import arriendo_service


router = APIRouter(prefix="/arriendos", tags=["Arriendos"])


@router.get("/", response_model=list[ArriendoResponse])
def obtener_arriendos():
    return arriendo_service.listar_arriendos()


@router.get("/{id_arriendo}", response_model=ArriendoResponse)
def obtener_arriendo(id_arriendo: int):
    return arriendo_service.obtener_arriendo(id_arriendo)


@router.post("/", response_model=ArriendoResponse, status_code=201)
def crear_arriendo(datos: ArriendoCreate):
    return arriendo_service.crear_arriendo(datos)


@router.patch("/{id_arriendo}", response_model=ArriendoResponse)
def actualizar_arriendo(id_arriendo: int, datos: ArriendoUpdate):
    return arriendo_service.actualizar_arriendo(id_arriendo, datos)


@router.delete("/{id_arriendo}", status_code=204)
def eliminar_arriendo(id_arriendo: int):
    arriendo_service.eliminar_arriendo(id_arriendo)
