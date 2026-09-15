#Aqui importamos la clase que esta creada dentro del domain
from app.domain.videojuego import Videojuego

videojuegos = [] #la base datos por asi decirlo

#no colocamos esto directamente para poder cumplir con la division de responsabilidades

def obtener_todos():
    return videojuegos


def crear(videojuego: Videojuego):
    videojuegos.append(videojuego)
    return videojuego


#esta funcion con la id busca con for quien tiene esa id para retornarlo y si no lo encuentra no devuelve nada 
def obtener_por_id(id_videojuego: int):
    for videojuego in videojuegos:
        if videojuego.id_videojuego == id_videojuego:
            return videojuego

    return None

#esta funcion busca por su ID y reemplaza el objeto antiguo por el nuevo.
def actualizar(videojuego_actualizado: Videojuego):
    for i, videojuego in enumerate(videojuegos):
        if videojuego.id_videojuego == videojuego_actualizado.id_videojuego:
            videojuegos[i] = videojuego_actualizado
            return videojuego_actualizado

    return None


def eliminar(id_videojuego: int):
    for i, videojuego in enumerate(videojuegos):
        if videojuego.id_videojuego == id_videojuego:
            return videojuegos.pop(i)
#si no encuentra la ID devuelve el None 
    return None