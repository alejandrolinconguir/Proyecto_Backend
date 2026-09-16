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


class CategoriaService:

    def crear_categoria(self, datos: CategoriaCreate) -> Categoria:
        # Regla de negocio: no permitir categorías con nombre duplicado.
        existente = categoria_repository.buscar_por_nombre(datos.nombre)
        if existente is not None:
            raise CategoriaYaExisteError(
                f"Ya existe una categoría con el nombre '{datos.nombre}'"
            )

        nueva_categoria = Categoria(
            id_categoria=0,  # el repository asigna el id real
            nombre=datos.nombre,
            descripcion=datos.descripcion,
            edad_minima=datos.edad_minima,
        )
        return categoria_repository.crear(nueva_categoria)

    def listar_categorias(self) -> list[Categoria]:
        return categoria_repository.listar()

    def obtener_categoria(self, id_categoria: int) -> Categoria:
        categoria = categoria_repository.buscar_por_id(id_categoria)
        if categoria is None:
            raise CategoriaNoEncontradaError(
                f"No existe una categoría con id {id_categoria}"
            )
        return categoria

    def actualizar_categoria(self, id_categoria: int, datos: CategoriaUpdate) -> Categoria:
        categoria = self.obtener_categoria(id_categoria)  # lanza error si no existe

        # Si se está cambiando el nombre, verificar que no choque con otra categoría
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
        self.obtener_categoria(id_categoria)  # lanza error si no existe
        categoria_repository.eliminar(id_categoria)


categoria_service = CategoriaService()