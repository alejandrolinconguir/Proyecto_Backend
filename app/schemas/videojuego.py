from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


PLATAFORMAS_VALIDAS = {"PS5", "PS4", "XBOX", "PC", "SWITCH", "SNES", "N64"}
ESTADOS_VALIDOS = {"Disponible", "Arrendado", "Dañado"}
AÑO_MINIMO = 1970


class VideojuegoBase(BaseModel):
    """Campos comunes a Create y Update, para no repetir validaciones."""

    titulo: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Título del videojuego",
    )
    plataforma: str = Field(
        ...,
        description="Plataforma del videojuego (ej. PS5, PC, SWITCH)",
    )
    año_lanzamiento: int = Field(
        ...,
        description="Año de lanzamiento del videojuego",
    )
    id_categoria: int = Field(
        ...,
        gt=0,
        description="ID de la categoría a la que pertenece (relación)",
    )


    @field_validator("plataforma")
    @classmethod
    def validar_plataforma(cls, valor: str) -> str:
        valor_normalizado = valor.strip().upper()
        if valor_normalizado not in PLATAFORMAS_VALIDAS:
            raise ValueError(
                f"Plataforma inválida. Debe ser una de: {', '.join(sorted(PLATAFORMAS_VALIDAS))}"
            )
        return valor_normalizado

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str) -> str:
        valor_limpio = valor.strip()
        if not valor_limpio:
            raise ValueError("El título no puede estar vacío o solo espacios")
        return valor_limpio

    @field_validator("año_lanzamiento")
    @classmethod
    def validar_año(cls, valor: int) -> int:
        año_actual = datetime.now().year
        if valor < AÑO_MINIMO or valor > año_actual:
            raise ValueError(
                f"año_lanzamiento debe estar entre {AÑO_MINIMO} y {año_actual}"
            )
        return valor


class VideojuegoCreate(VideojuegoBase):
    """DTO de entrada para crear un Videojuego (POST).

    No incluye 'id_videojuego' (lo genera el repository) ni 'estado'
    (todo videojuego nuevo empieza como 'Disponible').
    """
    pass


class VideojuegoUpdate(BaseModel):
    """DTO de entrada para actualizar un Videojuego (PUT/PATCH).

    Todos los campos son opcionales: el cliente solo envía lo que quiere
    cambiar. 'estado' se puede actualizar directamente aquí (ej. marcar
    como Dañado), aunque el flujo normal de arriendo/devolución debería
    pasar por el service.
    """
    titulo: Optional[str] = Field(None, min_length=2, max_length=100)
    plataforma: Optional[str] = None
    año_lanzamiento: Optional[int] = None
    id_categoria: Optional[int] = Field(None, gt=0)
    estado: Optional[str] = None

    @field_validator("plataforma")
    @classmethod
    def validar_plataforma(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return valor
        valor_normalizado = valor.strip().upper()
        if valor_normalizado not in PLATAFORMAS_VALIDAS:
            raise ValueError(
                f"Plataforma inválida. Debe ser una de: {', '.join(sorted(PLATAFORMAS_VALIDAS))}"
            )
        return valor_normalizado

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

    @field_validator("año_lanzamiento")
    @classmethod
    def validar_año(cls, valor: Optional[int]) -> Optional[int]:
        if valor is None:
            return valor
        año_actual = datetime.now().year
        if valor < AÑO_MINIMO or valor > año_actual:
            raise ValueError(
                f"año_lanzamiento debe estar entre {AÑO_MINIMO} y {año_actual}"
            )
        return valor


class VideojuegoResponse(VideojuegoBase):
    """DTO de salida: lo que la API devuelve al cliente."""
    id_videojuego: int
    estado: str

    model_config = {
        "from_attributes": True  # permite construirlo directo desde el objeto de domain/
    }
#esto solo definira como se nos devolveran los datos despues
class VideojuegoPaginadoResponse(BaseModel):
    items: list[VideojuegoResponse]
    total: int
    pagina: int
    limite: int
    total_paginas: int

