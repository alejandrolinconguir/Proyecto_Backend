from dataclasses import dataclass
from datetime import date

ESTADOS_ARRIENDO = {"Activo", "Devuelto"}


@dataclass
class Arriendo:
    """
    Entidad de dominio Arriendo (alineada al MER de RetroGames).

    Relación: cada Arriendo pertenece a un Cliente (id_cliente) y a un
    Videojuego (id_videojuego). Es la entidad que conecta ambas.
    """
    id_arriendo: int
    id_cliente: int
    id_videojuego: int
    fecha_arriendo: date
    fecha_devolucion: date
    estado: str = "Activo"

    def __post_init__(self):
        # Regla de negocio 3 del MER: la fecha de devolución no puede ser
        # anterior a la de arriendo. Esta SÍ es un invariante de dominio,
        # porque solo depende de los propios datos de esta entidad.
        if self.fecha_devolucion < self.fecha_arriendo:
            raise ValueError(
                "La fecha de devolución no puede ser anterior a la fecha de arriendo"
            )
        if self.estado not in ESTADOS_ARRIENDO:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_ARRIENDO))}"
            )

    def esta_activo(self) -> bool:
        return self.estado == "Activo"

    def marcar_devuelto(self) -> None:
        if not self.esta_activo():
            raise ValueError("Este arriendo ya fue devuelto")
        self.estado = "Devuelto"