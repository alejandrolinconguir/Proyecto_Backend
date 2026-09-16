"""
Excepciones de negocio de la API RetroGames.

Cada excepción sabe qué código HTTP le corresponde y qué "code" uniforme
debe devolver en el body de error. Los routers/services solo tienen que
lanzar la excepción correcta; el formateo de la respuesta lo hace el
handler global registrado en app/core/error_handlers.py.
"""
from typing import Any, Optional


class AppError(Exception):
    """Excepción base para todos los errores de negocio del proyecto."""

    status_code: int = 400
    code: str = "ERROR_GENERICO"

    def __init__(self, message: str, details: Optional[list[Any]] = None):
        self.message = message
        self.details = details or []
        super().__init__(message)


# --- Categorías genéricas reutilizables por cualquier módulo (Videojuego,
# Categoría, Arriendo, etc.), no solo Cliente ---

class NoEncontradoError(AppError):
    """Usar cuando un recurso solicitado por ID no existe -> 404."""
    status_code = 404
    code = "RECURSO_NO_ENCONTRADO"


class ConflictoError(AppError):
    """Usar cuando la operación choca con el estado actual de los datos
    (ej. un valor único duplicado) -> 409."""
    status_code = 409
    code = "CONFLICTO"


class SolicitudInvalidaError(AppError):
    """Usar para reglas de negocio simples que no son un problema de
    formato de datos (eso ya lo cubre la validación 422) -> 400."""
    status_code = 400
    code = "SOLICITUD_INVALIDA"


# --- Excepciones específicas del módulo Cliente ---

class ClienteNoEncontradoError(NoEncontradoError):
    code = "CLIENTE_NO_ENCONTRADO"

    def __init__(self, id_cliente: int):
        super().__init__(f"No existe un cliente con el ID solicitado ({id_cliente})")


class ClienteCorreoDuplicadoError(ConflictoError):
    code = "CLIENTE_CORREO_DUPLICADO"

    def __init__(self, correo: str):
        super().__init__(f"Ya existe un cliente registrado con el correo '{correo}'")
