from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator, model_validator

ESTADOS_VALIDOS = {"Activo", "Devuelto"}


class ArriendoBase(BaseModel):
    id_cliente: int = Field(
        ...,
        gt=0,
        description="ID del cliente que realiza el arriendo (relación)",
    )
    id_videojuego: int = Field(
        ...,
        gt=0,
        description="ID del videojuego arrendado (relación)",
    )
    fecha_arriendo: date = Field(
        ...,
        description="Fecha en que se realiza el arriendo",
    )
    fecha_devolucion: date = Field(
        ...,
        description="Fecha estimada/real de devolución",
    )

    @model_validator(mode="after")
    def validar_fechas(self):
        # Regla de negocio 3 del MER, aplicada también a nivel de schema
        # para que el error 422 salga apenas llega el request, antes de
        # tocar el dominio.
        if self.fecha_devolucion < self.fecha_arriendo:
            raise ValueError(
                "La fecha de devolución no puede ser anterior a la fecha de arriendo"
            )
        return self


class ArriendoCreate(ArriendoBase):
    """DTO de entrada para crear un Arriendo (POST).

    No incluye 'id_arriendo' (lo genera el repository) ni 'estado'
    (todo arriendo nuevo empieza como 'Activo').

    Nota: no validamos aquí si el videojuego ya está arrendado ni si el
    cliente ya tiene un arriendo activo del mismo juego, porque eso
    requiere revisar los datos guardados (lo hace el service).
    """
    pass


class ArriendoUpdate(BaseModel):
    """DTO de entrada para actualizar un Arriendo (PUT/PATCH).

    Pensado principalmente para el flujo de devolución (cambiar estado
    y/o fecha_devolucion real).
    """
    fecha_devolucion: Optional[date] = None
    estado: Optional[str] = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return valor
        if valor not in ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}"
            )
        return valor


class ArriendoResponse(ArriendoBase):
    """DTO de salida: lo que la API devuelve al cliente."""
    id_arriendo: int
    estado: str

    model_config = {
        "from_attributes": True
    }