from dataclasses import dataclass

ESTADOS_CLIENTE = {"Activo", "Inactivo"}


@dataclass
class Cliente:
    """
    Entidad de dominio Cliente (alineada al MER de RetroGames).

    Relación: un Cliente puede realizar muchos Arriendos (1..N).
    """
    id_cliente: int
    nombre: str
    apellido: str
    correo: str
    telefono: str
    estado: str = "Activo"

    def __post_init__(self):
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not self.apellido.strip():
            raise ValueError("El apellido no puede estar vacío")
        if "@" not in self.correo:
            raise ValueError("El correo no tiene un formato válido")
        if self.estado not in ESTADOS_CLIENTE:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_CLIENTE))}"
            )

    def esta_activo(self) -> bool:
        return self.estado == "Activo"

    def desactivar(self) -> None:
        self.estado = "Inactivo"

    def activar(self) -> None:
        self.estado = "Activo"

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"