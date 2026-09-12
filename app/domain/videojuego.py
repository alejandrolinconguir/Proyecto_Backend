#aqui se representan la entidad videojuego
from dataclasses import dataclass
#Nos permite definir una clase que representa nuestros datos sin tener que escribir manualmente un montón de código.

@dataclass            #aqui estoy creando la clase del videojuego
class Videojuego:
    id_videojuego: int
    titulo: str
    plataforma: str
    genero: str
    anio_lanzamiento: int
    estado: str
