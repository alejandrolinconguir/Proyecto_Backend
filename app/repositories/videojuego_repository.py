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