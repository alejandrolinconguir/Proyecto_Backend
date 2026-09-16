from typing import Optional
from app.domain.categoria import Categoria


class CategoriaRepository:
    """
    Repository de Categoria: maneja el almacenamiento en memoria.

    No contiene lógica de negocio, solo operaciones de guardar/buscar/
    listar/eliminar sobre una lista en memoria.
    """

    def __init__(self):
        self._categorias: list[Categoria] = []
        self._siguiente_id: int = 1

    def crear(self, categoria: Categoria) -> Categoria:
        categoria.id_categoria = self._siguiente_id
        self._siguiente_id += 1
        self._categorias.append(categoria)
        return categoria

    def listar(self) -> list[Categoria]:
        return self._categorias

    def buscar_por_id(self, id_categoria: int) -> Optional[Categoria]:
        for categoria in self._categorias:
            if categoria.id_categoria == id_categoria:
                return categoria
        return None

    def buscar_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """Usado por el service para verificar duplicados (case-insensitive)."""
        nombre_normalizado = nombre.strip().lower()
        for categoria in self._categorias:
            if categoria.nombre.strip().lower() == nombre_normalizado:
                return categoria
        return None

    def actualizar(self, categoria: Categoria) -> Categoria:
        for i, actual in enumerate(self._categorias):
            if actual.id_categoria == categoria.id_categoria:
                self._categorias[i] = categoria
                return categoria
        raise ValueError(f"Categoria con id {categoria.id_categoria} no encontrada")

    def eliminar(self, id_categoria: int) -> bool:
        categoria = self.buscar_por_id(id_categoria)
        if categoria is None:
            return False
        self._categorias.remove(categoria)
        return True


# Instancia única compartida por toda la app (patrón simple para
# almacenamiento en memoria sin base de datos real).
categoria_repository = CategoriaRepository()