from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import videojuegos, categoria
from app.services.videojuego_service import (VideojuegoNoEncontradoError,
    CategoriaNoEncontradaError as CategoriaVideojuegoNoEncontradaError)
from app.services.categoria_service import (CategoriaNoEncontradaError as CategoriaServiceNoEncontradaError,
    CategoriaYaExisteError)
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="RetroGames API",
    description="API para la gestión de videojuegos, clientes, categorías y arriendos.",
    version="1.0.0"
)

# Maneja los errores cuando no existe un videojuego solicitado
@app.exception_handler(VideojuegoNoEncontradoError)
async def videojuego_no_encontrado_handler(
    request: Request,
    exc: VideojuegoNoEncontradoError              #FastAPI automáticamente lo transforma en HTTP 404
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "VIDEOJUEGO_NOT_FOUND",
                "message": str(exc),
                "details": []
            }
        }
    )


# Maneja los errores cuando se intenta usar una categoría inexistente
@app.exception_handler(CategoriaVideojuegoNoEncontradaError)
async def categoria_no_encontrada_handler(
    request: Request,
    exc: CategoriaVideojuegoNoEncontradaError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "CATEGORIA_NOT_FOUND",
                "message": str(exc),
                "details": []
            }
        }
    )

# Maneja los errores cuando se busca una categoría que no existe
@app.exception_handler(CategoriaServiceNoEncontradaError)
async def categoria_service_no_encontrada_handler(
    request: Request,
    exc: CategoriaServiceNoEncontradaError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "CATEGORIA_NOT_FOUND",
                "message": str(exc),
                "details": []
            }
        }
    )


# Maneja los conflictos cuando se intenta crear una categoría duplicada
@app.exception_handler(CategoriaYaExisteError)
async def categoria_ya_existe_handler(
    request: Request,
    exc: CategoriaYaExisteError
):
    return JSONResponse(
        status_code=409,
        content={
            "error": {
                "code": "CATEGORIA_ALREADY_EXISTS",
                "message": str(exc),
                "details": []
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validacion_handler(request: Request, exc: RequestValidationError):
    detalles = []

    for error in exc.errors():
        detalles.append({
            "campo": ".".join(str(parte) for parte in error["loc"]),
            "mensaje": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Los datos enviados no son válidos",
                "details": detalles
            }
        }
    )

app.include_router(videojuegos.router) 
app.include_router(categoria.router)
#FastAPI, incorpora los endpoints que están definidos en videojuegos.py


@app.get("/")  # esto ya es una ruta end-point
#esto es como que cuando alguien use get o una solicitud se ejecuta la funcion de aca abajo 
def inicio():
    return {
        "mensaje": "RetroGames API funcionando"
    }