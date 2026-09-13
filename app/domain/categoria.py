from dataclasses import dataclass

ESTADOS_CATEGORIA = {"Activa", "Inactiva"}


@dataclass
class Categoria:
    """
    Entidad de dominio Categoria (alineada al MER de RetroGames).

    Relación: una Categoria puede tener muchos Videojuegos (1..N).
    """
    id_categoria: int
    nombre: str
    descripcion: str
    edad_minima: int
    estado: str = "Activa"

    def __post_init__(self):
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if self.edad_minima < 0:
            raise ValueError("edad_minima no puede ser negativa")
        if self.estado not in ESTADOS_CATEGORIA:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_CATEGORIA))}"
            )

    def esta_activa(self) -> bool:
        return self.estado == "Activa"

    def desactivar(self) -> None:
        self.estado = "Inactiva"

    def activar(self) -> None:
        self.estado = "Activa"