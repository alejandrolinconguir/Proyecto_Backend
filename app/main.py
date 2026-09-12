from fastapi import FastAPI
from app.routers import videojuegos

app = FastAPI(
    title="RetroGames API",
    description="API para la gestión de videojuegos, clientes, categorías y arriendos.",
    version="1.0.0"
)
app.include_router(videojuegos.router) 
#FastAPI, incorpora los endpoints que están definidos en videojuegos.py


@app.get("/")  # esto ya es una ruta end-point
#esto es como que cuando alguien use get o una solicitud se ejecuta la funcion de aca abajo 
def inicio():
    return {
        "mensaje": "RetroGames API funcionando"
    }