from app.domain.videojuego import Videojuego
from app.repositories import videojuego_repository
from app.repositories.categoria_repository import categoria_repository
from app.core.errors import (
    VideojuegoNoEncontradoError,
    CategoriaNoEncontradaError,
    SolicitudInvalidaError,
)

def obtener_videojuegos(          #las 3 funciones del GET
    id_categoria=None,
    plataforma=None,
    estado=None,
    orden=None,
    pagina=1,
    limite=10
):
    videojuegos = videojuego_repository.obtener_todos()

    # 1. FILTRAR
    if id_categoria is not None:
        videojuegos = [
            videojuego
            for videojuego in videojuegos
            if videojuego.id_categoria == id_categoria
        ]

    if plataforma is not None:
        plataforma = plataforma.strip().upper()
        videojuegos = [
            videojuego
            for videojuego in videojuegos
            if videojuego.plataforma == plataforma
        ]

    if estado is not None:
        videojuegos = [
            videojuego
            for videojuego in videojuegos
            if videojuego.estado == estado
        ]

    # 2. ORDENAR
    if orden is not None:
        campos_orden = {
            "titulo": lambda videojuego: videojuego.titulo.lower(),
            "plataforma": lambda videojuego: videojuego.plataforma,
            "año_lanzamiento": lambda videojuego: videojuego.año_lanzamiento,
            "id_categoria": lambda videojuego: videojuego.id_categoria,
            "estado": lambda videojuego: videojuego.estado
        }

        orden_descendente = orden.startswith("-")
        campo = orden[1:] if orden_descendente else orden

        if campo not in campos_orden:
            raise SolicitudInvalidaError(
        "Orden inválido. Opciones: titulo, plataforma, "
        "año_lanzamiento, id_categoria, estado")

        videojuegos = sorted(
            videojuegos,
            key=campos_orden[campo],
            reverse=orden_descendente
        )

    # 3. PAGINAR
    total = len(videojuegos)

    inicio = (pagina - 1) * limite
    fin = inicio + limite

    videojuegos_pagina = videojuegos[inicio:fin]

    total_paginas = (total + limite - 1) // limite

    return {
        "items": videojuegos_pagina,
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "total_paginas": total_paginas
    }

#service le solicita al repository el videojuego
def obtener_videojuego_por_id(id_videojuego: int):
    videojuego = videojuego_repository.obtener_por_id(id_videojuego)

    if videojuego is None:
        raise VideojuegoNoEncontradoError("No existe un videojuego con el ID solicitado")
    return videojuego


def crear_videojuego(datos):
    #para valdiar que la categoria exista dentro del sistema, si existe detiene la creacion 
    categoria = categoria_repository.buscar_por_id(datos.id_categoria)

    if categoria is None:
        raise CategoriaNoEncontradaError("La categoría indicada no existe")

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
        raise VideojuegoNoEncontradoError("No existe un videojuego con el ID solicitado")

    if datos.titulo is not None:
        videojuego.titulo = datos.titulo

    if datos.plataforma is not None:
        videojuego.plataforma = datos.plataforma

    if datos.año_lanzamiento is not None:
        videojuego.año_lanzamiento = datos.año_lanzamiento

    if datos.id_categoria is not None:
    # Verificamos que la nueva categoría exista
        categoria = categoria_repository.obtener_por_id(datos.id_categoria)
        if categoria is None:
            raise CategoriaNoEncontradaError("La categoría indicada no existe")
        videojuego.id_categoria = datos.id_categoria

    if datos.estado is not None:
        videojuego.estado = datos.estado

    return videojuego_repository.actualizar(videojuego) 
#"Si cambio Fortnite por Overcooked, debería cambiar también la categoría

def eliminar_videojuego(id_videojuego: int):
    videojuego = videojuego_repository.eliminar(id_videojuego)
#para cuando no exista el juego a eliminar
    if videojuego is None:
        raise VideojuegoNoEncontradoError("No existe un videojuego con el ID solicitado")

    return videojuego