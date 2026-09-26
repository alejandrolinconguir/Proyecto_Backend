from typing import Optional
from app.domain.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate
from app.repositories.categoria_repository import categoria_repository


class CategoriaYaExisteError(Exception):
    """Se lanza cuando se intenta crear/renombrar una categoría con un
    nombre que ya existe (regla de negocio: evitar categorías duplicadas)."""
    pass


class CategoriaNoEncontradaError(Exception):
    """Se lanza cuando se busca/actualiza/elimina una categoría que no existe."""
    pass


class ParametroInvalidoError(Exception):
    """Se lanza cuando los parámetros de filtrado/orden/paginación son inválidos."""
    pass


CAMPOS_ORDENABLES = {"id_categoria", "nombre", "edad_minima", "estado"}


class CategoriaService:

    def crear_categoria(self, datos: CategoriaCreate) -> Categoria:
        existente = categoria_repository.buscar_por_nombre(datos.nombre)
        if existente is not None:
            raise CategoriaYaExisteError(
                f"Ya existe una categoría con el nombre '{datos.nombre}'"
            )

        nueva_categoria = Categoria(
            id_categoria=0,
            nombre=datos.nombre,
            descripcion=datos.descripcion,
            edad_minima=datos.edad_minima,
        )
        return categoria_repository.crear(nueva_categoria)

    def listar_categorias(self) -> list[Categoria]:
        return categoria_repository.listar()

    def listar_categorias_paginadas(
        self,
        estado: Optional[str] = None,
        ordenar_por: str = "id_categoria",
        direccion: str = "asc",
        pagina: int = 1,
        limite: int = 20,
    ) -> dict:
        if direccion not in ("asc", "desc"):
            raise ParametroInvalidoError("direccion debe ser 'asc' o 'desc'")
        if ordenar_por not in CAMPOS_ORDENABLES:
            raise ParametroInvalidoError(
                f"ordenar_por debe ser uno de: {', '.join(sorted(CAMPOS_ORDENABLES))}"
            )
        if pagina < 1:
            raise ParametroInvalidoError("pagina debe ser mayor o igual a 1")
        if not (1 <= limite <= 100):
            raise ParametroInvalidoError("limite debe estar entre 1 y 100")

        categorias = categoria_repository.listar()

        if estado is not None:
            categorias = [c for c in categorias if c.estado == estado]

        reverso = direccion == "desc"
        categorias = sorted(
            categorias, key=lambda c: getattr(c, ordenar_por), reverse=reverso
        )

        total = len(categorias)
        inicio = (pagina - 1) * limite
        fin = inicio + limite
        items = categorias[inicio:fin]
        total_paginas = (total + limite - 1) // limite if total > 0 else 0

        return {
            "items": items,
            "total": total,
            "pagina": pagina,
            "limite": limite,
            "total_paginas": total_paginas,
        }

    def obtener_categoria(self, id_categoria: int) -> Categoria:
        categoria = categoria_repository.buscar_por_id(id_categoria)
        if categoria is None:
            raise CategoriaNoEncontradaError(f"No existe una categoría con id {id_categoria}")
        return categoria

    def actualizar_categoria(self, id_categoria: int, datos: CategoriaUpdate) -> Categoria:
        categoria = self.obtener_categoria(id_categoria)

        if datos.nombre is not None and datos.nombre != categoria.nombre:
            existente = categoria_repository.buscar_por_nombre(datos.nombre)
            if existente is not None:
                raise CategoriaYaExisteError(
                    f"Ya existe una categoría con el nombre '{datos.nombre}'"
                )
            categoria.nombre = datos.nombre

        if datos.descripcion is not None:
            categoria.descripcion = datos.descripcion
        if datos.edad_minima is not None:
            categoria.edad_minima = datos.edad_minima
        if datos.estado is not None:
            categoria.estado = datos.estado

        return categoria_repository.actualizar(categoria)

    def eliminar_categoria(self, id_categoria: int) -> None:
        self.obtener_categoria(id_categoria)
        categoria_repository.eliminar(id_categoria)


categoria_service = CategoriaService()