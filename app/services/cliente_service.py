from sqlalchemy.orm import Session

from app.domain.cliente import Cliente
from app.repositories import cliente_repository
from app.core.errors import ClienteNoEncontradoError, ClienteCorreoDuplicadoError


def obtener_clientes(db: Session) -> list[Cliente]:
    return cliente_repository.obtener_todos(db)


def obtener_cliente_por_id(db: Session, id_cliente: int) -> Cliente:
    cliente = cliente_repository.obtener_por_id(db, id_cliente)
    if cliente is None:
        raise ClienteNoEncontradoError(id_cliente)
    return cliente


def crear_cliente(db: Session, datos) -> Cliente:
    # Regla de negocio: no puede haber dos clientes con el mismo correo -> 409
    if cliente_repository.obtener_por_correo(db, datos.correo) is not None:
        raise ClienteCorreoDuplicadoError(datos.correo)

    # El ID real lo genera PostgreSQL al guardar (por eso se parte con 0).
    cliente = Cliente(
        id_cliente=0,
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        telefono=datos.telefono,
    )

    cliente = cliente_repository.crear(db, cliente)
    db.commit()
    return cliente


def actualizar_cliente(db: Session, id_cliente: int, datos) -> Cliente:
    cliente = obtener_cliente_por_id(db, id_cliente)  # ya lanza 404 si no existe

    if datos.correo is not None and datos.correo != cliente.correo:
        if cliente_repository.obtener_por_correo(db, datos.correo) is not None:
            raise ClienteCorreoDuplicadoError(datos.correo)
        cliente.correo = datos.correo

    if datos.nombre is not None:
        cliente.nombre = datos.nombre
    if datos.apellido is not None:
        cliente.apellido = datos.apellido
    if datos.telefono is not None:
        cliente.telefono = datos.telefono
    if datos.estado is not None:
        cliente.estado = datos.estado

    cliente = cliente_repository.actualizar(db, cliente)
    db.commit()
    return cliente


def eliminar_cliente(db: Session, id_cliente: int) -> Cliente:
    obtener_cliente_por_id(db, id_cliente)  # lanza 404 si no existe
    cliente = cliente_repository.eliminar(db, id_cliente)
    db.commit()
    return cliente
