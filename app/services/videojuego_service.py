from app.domain.videojuego import Videojuego
from app.repositories import videojuego_repository

def obtener_videojuegos():
    return videojuego_repository.obtener_todos() #obtenemos la info

#service le solicita al repository el videojuego
def obtener_videojuego_por_id(id_videojuego: int):
    return videojuego_repository.obtener_por_id(id_videojuego)


def crear_videojuego(datos):
    # Se genera automáticamente el ID del videojuego
    nuevo_id = len(videojuego_repository.obtener_todos()) + 1

    videojuego = Videojuego(
        id_videojuego=nuevo_id,
        titulo=datos.titulo,
        plataforma=datos.plataforma,
        año_lanzamiento=datos.año_lanzamiento,
        id_categoria=datos.id_categoria
    )

    return videojuego_repository.crear(videojuego)


#aqui se actualiza los datos con la actualizacion del nuevo juego
def actualizar_videojuego(id_videojuego: int, datos):
    videojuego = videojuego_repository.obtener_por_id(id_videojuego)
    if videojuego is None:
        return None

    if datos.titulo is not None:
        videojuego.titulo = datos.titulo

    if datos.plataforma is not None:
        videojuego.plataforma = datos.plataforma

    if datos.año_lanzamiento is not None:
        videojuego.año_lanzamiento = datos.año_lanzamiento

    if datos.id_categoria is not None:
        videojuego.id_categoria = datos.id_categoria

    if datos.estado is not None:
        videojuego.estado = datos.estado

    return videojuego_repository.actualizar(videojuego) 
#"Si cambio Fortnite por Overcooked, debería cambiar también la categoría

def eliminar_videojuego(id_videojuego: int):
    return videojuego_repository.eliminar(id_videojuego)