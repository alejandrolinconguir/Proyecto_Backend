from typing import Any, Optional

class AppError(Exception):

    status_code: int = 400
    code: str = "ERROR_GENERICO"

    def __init__(self, message: str, details: Optional[list[Any]] = None):
        self.message = message
        self.details = details or []
        super().__init__(message)

#Categorías genéricas reutilizables por cualquier módulo (Videojuego, Categoría, Arriendo, etc.), no solo Cliente 

class NoEncontradoError(AppError):

    status_code = 404
    code = "RECURSO_NO_ENCONTRADO"


class ConflictoError(AppError):

    status_code = 409
    code = "CONFLICTO"


class SolicitudInvalidaError(AppError):

    status_code = 400
    code = "SOLICITUD_INVALIDA"


#Excepciones específicas del módulo Cliente

class ClienteNoEncontradoError(NoEncontradoError):
    code = "CLIENTE_NO_ENCONTRADO"

    def __init__(self, id_cliente: int):
        super().__init__(f"No existe un cliente con el ID solicitado ({id_cliente})")


class ClienteCorreoDuplicadoError(ConflictoError):
    code = "CLIENTE_CORREO_DUPLICADO"

    def __init__(self, correo: str):
        super().__init__(f"Ya existe un cliente registrado con el correo '{correo}'")
