from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.schemas.error import respuestas_error
from app.services import cliente_service

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/", response_model=list[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    return cliente_service.obtener_clientes(db)


@router.get(
    "/{id_cliente}",
    response_model=ClienteResponse,
    responses=respuestas_error(404, 422),
)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return cliente_service.obtener_cliente_por_id(db, id_cliente)


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    responses=respuestas_error(409, 422),
)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    return cliente_service.crear_cliente(db, datos)


@router.patch(
    "/{id_cliente}",
    response_model=ClienteResponse,
    responses=respuestas_error(404, 409, 422),
)
def actualizar_cliente(id_cliente: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    return cliente_service.actualizar_cliente(db, id_cliente, datos)


@router.delete(
    "/{id_cliente}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=respuestas_error(404, 409, 422),
)
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente_service.eliminar_cliente(db, id_cliente)
