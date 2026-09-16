from typing import Optional

from app.domain.cliente import Cliente

clientes: list[Cliente] = []  # la "base de datos" en memoria


def obtener_todos() -> list[Cliente]:
    return clientes


def obtener_por_id(id_cliente: int) -> Optional[Cliente]:
    for cliente in clientes:
        if cliente.id_cliente == id_cliente:
            return cliente
    return None


def obtener_por_correo(correo: str) -> Optional[Cliente]:
    for cliente in clientes:
        if cliente.correo == correo:
            return cliente
    return None


def crear(cliente: Cliente) -> Cliente:
    clientes.append(cliente)
    return cliente


def actualizar(cliente_actualizado: Cliente) -> Optional[Cliente]:
    for i, cliente in enumerate(clientes):
        if cliente.id_cliente == cliente_actualizado.id_cliente:
            clientes[i] = cliente_actualizado
            return cliente_actualizado
    return None


def eliminar(id_cliente: int) -> Optional[Cliente]:
    for i, cliente in enumerate(clientes):
        if cliente.id_cliente == id_cliente:
            return clientes.pop(i)
    return None
