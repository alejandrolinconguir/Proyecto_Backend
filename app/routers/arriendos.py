from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.schemas.arriendo import ArriendoCreate, ArriendoUpdate, ArriendoResponse
from app.schemas.error import respuestas_error
from app.services.arriendo_service import arriendo_service


router = APIRouter(prefix="/arriendos", tags=["Arriendos"])


@router.get("/", response_model=list[ArriendoResponse])
def obtener_arriendos(db: Session = Depends(get_db)):
    return arriendo_service.listar_arriendos(db)


@router.get(
    "/{id_arriendo}",
    response_model=ArriendoResponse,
    responses=respuestas_error(404, 422),
)
def obtener_arriendo(id_arriendo: int, db: Session = Depends(get_db)):
    return arriendo_service.obtener_arriendo(db, id_arriendo)


@router.post(
    "/",
    response_model=ArriendoResponse,
    status_code=201,
    responses=respuestas_error(404, 409, 422),
)
def crear_arriendo(datos: ArriendoCreate, db: Session = Depends(get_db)):
    return arriendo_service.crear_arriendo(db, datos)


@router.patch(
    "/{id_arriendo}",
    response_model=ArriendoResponse,
    responses=respuestas_error(400, 404, 422),
)
def actualizar_arriendo(id_arriendo: int, datos: ArriendoUpdate, db: Session = Depends(get_db)):
    return arriendo_service.actualizar_arriendo(db, id_arriendo, datos)


@router.delete(
    "/{id_arriendo}",
    status_code=204,
    responses=respuestas_error(404, 422),
)
def eliminar_arriendo(id_arriendo: int, db: Session = Depends(get_db)):
    arriendo_service.eliminar_arriendo(db, id_arriendo)
