from fastapi import APIRouter
from app.schemas.videojuego import VideojuegoCreate
from app.services import videojuego_service


router = APIRouter( #esta parte le dice al FastAPI que estos end-point son del recuerso videojuegos
    prefix="/videojuegos",
    tags=["Videojuegos"]
)


@router.get("/")  #este seria iugal al GET /videojuego/
def obtener_videojuegos():
    return videojuego_service.obtener_videojuegos()


#aqui crea una ruta GET que recibe un ID desde la URL
@router.get("/{id_videojuego}")
def obtener_videojuego(id_videojuego: int):
    return videojuego_service.obtener_videojuego_por_id(id_videojuego)
#recive el numero y manda la ID al Service


@router.post("/")      #mismo aqui POST /videojuegos/
def crear_videojuego(datos: VideojuegoCreate):
    return videojuego_service.crear_videojuego(datos)