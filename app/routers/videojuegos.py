from fastapi import APIRouter, Query #el Query Porque los parámetros que queremos recibir vienen desde la URL.
from app.schemas.videojuego import (VideojuegoCreate,VideojuegoUpdate,VideojuegoResponse,VideojuegoPaginadoResponse)
from app.services import videojuego_service


router = APIRouter( #esta parte le dice al FastAPI que estos end-point son del recuerso videojuegos
    prefix="/videojuegos",
    tags=["Videojuegos"]
)


@router.get("/", response_model=VideojuegoPaginadoResponse)
def obtener_videojuegos(
    id_categoria: int | None = Query(None, gt=0), #el usuario puede mandar cate pero no es obligatorio :v
    plataforma: str | None = Query(None),
    estado: str | None = Query(None),                #los demas parametros nos ayudan a defenir mas opciones para ordenar
    orden: str | None = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100)    #aqui mostra 1 por pagina y solo seran un total de 100
):

    return videojuego_service.obtener_videojuegos(
        id_categoria=id_categoria,
        plataforma=plataforma,
        estado=estado,
        orden=orden,
        pagina=pagina,
        limite=limite
    )


#aqui crea una ruta GET que recibe un ID desde la URL
@router.get("/{id_videojuego}", response_model=VideojuegoResponse)
def obtener_videojuego(id_videojuego: int):
    return videojuego_service.obtener_videojuego_por_id(id_videojuego)
#recive el numero y manda la ID al Service



#aqui le esta diciendo la estructura que debe seguir y pues el lo que devolvera cuando salga bn
@router.post("/", response_model=VideojuegoResponse, status_code=201)
def crear_videojuego(datos: VideojuegoCreate):
    return videojuego_service.crear_videojuego(datos)

#El Json que es manda se guarda aqui
@router.patch("/{id_videojuego}", response_model=VideojuegoResponse)
def actualizar_videojuego(id_videojuego: int, datos: VideojuegoUpdate):
    return videojuego_service.actualizar_videojuego(id_videojuego, datos)


@router.delete("/{id_videojuego}", status_code = 204)
def eliminar_videojuego(id_videojuego: int):
    return videojuego_service.eliminar_videojuego(id_videojuego)