from fastapi import FastAPI

app = FastAPI(
    title="RetroGames API",
    description="API para la gestión de videojuegos, clientes, categorías y arriendos.",
    version="1.0.0"
)


@app.get("/")  #esto es como que cuando alguien use get o una solicitud se ejecuta la funcion de aca abajo 
def inicio():
    return {
        "mensaje": "RetroGames API funcionando"
    }