from pydantic import BaseModel


#aqui el id_videojuego no se coloca por el backend es quien la va a hacer
#cuando alguein mande info el backend le da la id
class VideojuegoCreate(BaseModel):
    titulo: str
    plataforma: str
    genero: str
    anio_lanzamiento: int
    estado: str