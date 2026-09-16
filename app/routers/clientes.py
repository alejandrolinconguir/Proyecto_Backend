from fastapi import APIRouter, status

from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services import cliente_service

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/", response_model=list[ClienteResponse])
def obtener_clientes():
    return cliente_service.obtener_clientes()


@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener_cliente(id_cliente: int):
    return cliente_service.obtener_cliente_por_id(id_cliente)


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCreate):
    return cliente_service.crear_cliente(datos)


@router.patch("/{id_cliente}", response_model=ClienteResponse)
def actualizar_cliente(id_cliente: int, datos: ClienteUpdate):
    return cliente_service.actualizar_cliente(id_cliente, datos)


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(id_cliente: int):
    cliente_service.eliminar_cliente(id_cliente)
