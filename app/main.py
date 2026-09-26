from fastapi import FastAPI

from app.routers import videojuegos, categoria, arriendos, clientes
from app.core.error_handlers import registrar_manejadores_errores


app = FastAPI(
    title="RetroGames API",
    description="API para la gestión de videojuegos, clientes, categorías y arriendos.",
    version="1.0.0"
)

# Manejo centralizado de errores
registrar_manejadores_errores(app)


# Registro de los routers
app.include_router(videojuegos.router)
app.include_router(categoria.router)
app.include_router(arriendos.router)
app.include_router(clientes.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "RetroGames API funcionando"
    }