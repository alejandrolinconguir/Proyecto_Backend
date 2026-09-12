from dataclasses import dataclass


@dataclass
class Videojuego:
    """
    Entidad de dominio Videojuego.

    Representa un videojuego dentro del sistema RetroGames, independiente
    de cómo se reciba o entregue por la API (eso lo maneja schemas/).

    Relación: cada Videojuego pertenece a una Categoria (categoria_id).
    """
    id: int
    titulo: str
    categoria_id: int
    plataforma: str
    precio_arriendo_diario: float
    stock_total: int
    stock_disponible: int
    activo: bool = True

    def __post_init__(self):
        # Reglas de coherencia del propio dominio (no reglas de negocio del
        # caso de uso, sino invariantes que la entidad SIEMPRE debe cumplir).
        if self.stock_disponible > self.stock_total:
            raise ValueError(
                "stock_disponible no puede ser mayor que stock_total"
            )
        if self.stock_total < 0 or self.stock_disponible < 0:
            raise ValueError("El stock no puede ser negativo")
        if self.precio_arriendo_diario <= 0:
            raise ValueError("precio_arriendo_diario debe ser mayor a 0")

    def esta_disponible(self) -> bool:
        """Un videojuego está disponible para arriendo si está activo y tiene stock."""
        return self.activo and self.stock_disponible > 0

    def reservar_unidad(self) -> None:
        """Descuenta una unidad del stock disponible al concretar un arriendo."""
        if self.stock_disponible <= 0:
            raise ValueError("No hay stock disponible para reservar")
        self.stock_disponible -= 1

    def liberar_unidad(self) -> None:
        """Devuelve una unidad al stock disponible al finalizar un arriendo."""
        if self.stock_disponible >= self.stock_total:
            raise ValueError("El stock disponible no puede superar el stock total")
        self.stock_disponible += 1