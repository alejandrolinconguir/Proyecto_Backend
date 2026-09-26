from typing import Optional

from app.domain.arriendo import Arriendo


class ArriendoRepository:
    """Repository de Arriendo usando almacenamiento en memoria."""

    def __init__(self):
        self._arriendos: list[Arriendo] = []
        self._siguiente_id: int = 1

    def crear(self, arriendo: Arriendo) -> Arriendo:
        arriendo.id_arriendo = self._siguiente_id
        self._siguiente_id += 1
        self._arriendos.append(arriendo)
        return arriendo

    def listar(self) -> list[Arriendo]:
        return self._arriendos

    def buscar_por_id(self, id_arriendo: int) -> Optional[Arriendo]:
        for arriendo in self._arriendos:
            if arriendo.id_arriendo == id_arriendo:
                return arriendo
        return None

    def buscar_activo_por_cliente(self, id_cliente: int) -> Optional[Arriendo]:
        for arriendo in self._arriendos:
            if arriendo.id_cliente == id_cliente and arriendo.esta_activo():
                return arriendo
        return None

    def actualizar(self, arriendo: Arriendo) -> Optional[Arriendo]:
        for i, actual in enumerate(self._arriendos):
            if actual.id_arriendo == arriendo.id_arriendo:
                self._arriendos[i] = arriendo
                return arriendo
        return None

    def eliminar(self, id_arriendo: int) -> Optional[Arriendo]:
        for i, arriendo in enumerate(self._arriendos):
            if arriendo.id_arriendo == id_arriendo:
                return self._arriendos.pop(i)
        return None

    def limpiar(self) -> None:
        """Utilidad para pruebas; no se usa desde la API."""
        self._arriendos.clear()
        self._siguiente_id = 1


arriendo_repository = ArriendoRepository()
