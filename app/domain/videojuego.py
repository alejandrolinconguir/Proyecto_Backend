from dataclasses import dataclass

# Estados válidos para un videojuego, según el MER del equipo.
ESTADOS_VIDEOJUEGO = {"Disponible", "Arrendado", "Dañado"}


@dataclass
class Videojuego:
    """
    Entidad de dominio Videojuego (alineada al MER de RetroGames).

    Representa un videojuego dentro del sistema, independiente de cómo se
    reciba o entregue por la API (eso lo maneja schemas/).

    Relación: cada Videojuego pertenece a una Categoria (id_categoria).
    """
    id_videojuego: int
    titulo: str
    plataforma: str
    año_lanzamiento: int
    id_categoria: int
    estado: str = "Disponible"

    def __post_init__(self):
        # Reglas de coherencia del propio dominio: invariantes que la
        # entidad SIEMPRE debe cumplir, sin importar quién la cree.
        if self.estado not in ESTADOS_VIDEOJUEGO:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_VIDEOJUEGO))}"
            )
        if not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")

    def esta_disponible(self) -> bool:
        """Un videojuego solo puede arrendarse si su estado es 'Disponible'."""
        return self.estado == "Disponible"

    def marcar_arrendado(self) -> None:
        """Cambia el estado al concretar un arriendo (regla de negocio 1 del MER)."""
        if not self.esta_disponible():
            raise ValueError(
                f"No se puede arrendar: el videojuego está '{self.estado}'"
            )
        self.estado = "Arrendado"

    def marcar_disponible(self) -> None:
        """Cambia el estado al devolver un videojuego arrendado."""
        self.estado = "Disponible"

    def marcar_dañado(self) -> None:
        """Cambia el estado si el videojuego se reporta dañado al devolverlo."""
        self.estado = "Dañado"