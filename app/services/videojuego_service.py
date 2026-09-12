from app.domain.videojuego import Videojuego
from app.repositories import videojuego_repository

def obtener_videojuegos():
    return videojuego_repository.obtener_todos() #obtenemos la info

#service le solicita al repository el videojuego
def obtener_videojuego_por_id(id_videojuego: int):
    return videojuego_repository.obtener_por_id(id_videojuego)


def crear_videojuego(datos):            #esto se hace apra que no sea desde el 0
    nuevo_id = len(videojuego_repository.obtener_todos()) + 1

    videojuego = Videojuego(
        id_videojuego=nuevo_id,
        titulo=datos.titulo,
        plataforma=datos.plataforma,
        genero=datos.genero,
        anio_lanzamiento=datos.anio_lanzamiento,
        estado=datos.estado
    )

    return videojuego_repository.crear(videojuego)