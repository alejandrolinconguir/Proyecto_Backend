"""
Registra los exception handlers globales de FastAPI para que TODA la API
(no solo Cliente) responda errores con el mismo formato:

{
  "error": {
    "code": "CLIENTE_NO_ENCONTRADO",
    "message": "No existe un cliente con el ID solicitado",
    "details": []
  }
}
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError


def _formato_error(code: str, message: str, details: list | None = None) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
        }
    }


def registrar_manejadores_errores(app: FastAPI) -> None:
    """Llamar UNA vez desde main.py, después de crear la instancia de FastAPI:

        from app.core.error_handlers import registrar_manejadores_errores
        registrar_manejadores_errores(app)
    """

    @app.exception_handler(AppError)
    async def manejar_app_error(request: Request, exc: AppError):
        # Cubre 404 / 409 / 400 (y cualquier otra excepción de negocio
        # que se agregue a futuro), según lo defina cada excepción.
        return JSONResponse(
            status_code=exc.status_code,
            content=_formato_error(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def manejar_error_validacion(request: Request, exc: RequestValidationError):
        # 422: errores de validación de Pydantic (body, query params, etc.)
        detalles = [
            {
                "campo": ".".join(str(parte) for parte in error["loc"] if parte != "body"),
                "mensaje": error["msg"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=_formato_error(
                "ERROR_VALIDACION",
                "Los datos enviados no son válidos",
                detalles,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def manejar_http_exception(request: Request, exc: StarletteHTTPException):
        # Red de seguridad para HTTPException "crudas" que algún endpoint
        # todavía lance directamente, para que ni siquiera esas rompan
        # el formato uniforme.
        return JSONResponse(
            status_code=exc.status_code,
            content=_formato_error("ERROR_HTTP", str(exc.detail)),
        )
