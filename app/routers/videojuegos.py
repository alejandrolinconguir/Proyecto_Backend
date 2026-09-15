from fastapi import APIRouter
from app.schemas.videojuego import VideojuegoCreate, VideojuegoUpdate, VideojuegoResponse
from app.services import videojuego_service


router = APIRouter( #esta parte le dice al FastAPI que estos end-point son del recuerso videojuegos
    prefix="/videojuegos",
    tags=["Videojuegos"]
)


@router.get("/", response_model=list[VideojuegoResponse]) #esto le dice a la API
#Este endpoint devuelve una lista de objetos que tienen la estructura de VideojuegoResponse
def obtener_videojuegos():
    return videojuego_service.obtener_videojuegos()


#aqui crea una ruta GET que recibe un ID desde la URL
@router.get("/{id_videojuego}", response_model=VideojuegoResponse)
def obtener_videojuego(id_videojuego: int):
    return videojuego_service.obtener_videojuego_por_id(id_videojuego)
#recive el numero y manda la ID al Service


@router.post("/")      #mismo aqui POST /videojuegos/
def crear_videojuego(datos: VideojuegoCreate):
    return videojuego_service.crear_videojuego(datos)

#El Json que es manda se guarda aqui
@router.patch("/{id_videojuego}", response_model=VideojuegoResponse)
def actualizar_videojuego(id_videojuego: int, datos: VideojuegoUpdate):
    return videojuego_service.actualizar_videojuego(id_videojuego, datos)



@router.delete("/{id_videojuego}")
def eliminar_videojuego(id_videojuego: int):
    return videojuego_service.eliminar_videojuego(id_videojuego)