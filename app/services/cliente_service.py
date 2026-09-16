from app.domain.cliente import Cliente
from app.repositories import cliente_repository
from app.core.errors import ClienteNoEncontradoError, ClienteCorreoDuplicadoError


def obtener_clientes() -> list[Cliente]:
    return cliente_repository.obtener_todos()


def obtener_cliente_por_id(id_cliente: int) -> Cliente:
    cliente = cliente_repository.obtener_por_id(id_cliente)
    if cliente is None:
        raise ClienteNoEncontradoError(id_cliente)
    return cliente


def crear_cliente(datos) -> Cliente:
    # Regla de negocio: no puede haber dos clientes con el mismo correo -> 409
    if cliente_repository.obtener_por_correo(datos.correo) is not None:
        raise ClienteCorreoDuplicadoError(datos.correo)

    nuevo_id = len(cliente_repository.obtener_todos()) + 1

    cliente = Cliente(
        id_cliente=nuevo_id,
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        telefono=datos.telefono,
    )

    return cliente_repository.crear(cliente)


def actualizar_cliente(id_cliente: int, datos) -> Cliente:
    cliente = obtener_cliente_por_id(id_cliente)  # ya lanza 404 si no existe

    if datos.correo is not None and datos.correo != cliente.correo:
        if cliente_repository.obtener_por_correo(datos.correo) is not None:
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

    return cliente_repository.actualizar(cliente)


def eliminar_cliente(id_cliente: int) -> Cliente:
    obtener_cliente_por_id(id_cliente)  # lanza 404 si no existe
    return cliente_repository.eliminar(id_cliente)
