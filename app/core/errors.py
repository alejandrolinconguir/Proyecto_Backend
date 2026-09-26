from typing import Any, Optional


class AppError(Exception):
    status_code: int = 400
    code: str = "ERROR_GENERICO"

    def __init__(self, message: str, details: Optional[list[Any]] = None):
        self.message = message
        self.details = details or []
        super().__init__(message)


# Errores genéricos reutilizables
class NoEncontradoError(AppError):
    status_code = 404
    code = "RECURSO_NO_ENCONTRADO"


class ConflictoError(AppError):
    status_code = 409
    code = "CONFLICTO"


class SolicitudInvalidaError(AppError):
    status_code = 400
    code = "SOLICITUD_INVALIDA"


# Errores de videojuegos
class VideojuegoNoEncontradoError(NoEncontradoError):
    code = "VIDEOJUEGO_NO_ENCONTRADO"


class CategoriaNoEncontradaError(NoEncontradoError):
    code = "CATEGORIA_NO_ENCONTRADA"


# Errores de categorías
class CategoriaYaExisteError(ConflictoError):
    code = "CATEGORIA_YA_EXISTE"


class ParametroInvalidoError(SolicitudInvalidaError):
    code = "PARAMETRO_INVALIDO"


# Errores de clientes
class ClienteNoEncontradoError(NoEncontradoError):
    code = "CLIENTE_NO_ENCONTRADO"

    def __init__(self, id_cliente: int):
        super().__init__(
            f"No existe un cliente con el ID solicitado ({id_cliente})"
        )


class ClienteCorreoDuplicadoError(ConflictoError):
    code = "CLIENTE_CORREO_DUPLICADO"

    def __init__(self, correo: str):
        super().__init__(
            f"Ya existe un cliente registrado con el correo '{correo}'"
        )


# Errores de arriendos
class ArriendoNoEncontradoError(NoEncontradoError):
    code = "ARRIENDO_NO_ENCONTRADO"


class VideojuegoNoDisponibleError(ConflictoError):
    code = "VIDEOJUEGO_NO_DISPONIBLE"


class ClienteTieneArriendoActivoError(ConflictoError):
    code = "CLIENTE_TIENE_ARRIENDO_ACTIVO"


class FechaDevolucionInvalidaError(SolicitudInvalidaError):
    code = "FECHA_DEVOLUCION_INVALIDA"


class VideojuegoNoEncontradoEnArriendoError(NoEncontradoError):
    code = "VIDEOJUEGO_NO_ENCONTRADO"
