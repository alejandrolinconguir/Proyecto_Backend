from typing import Optional
from pydantic import BaseModel, Field, field_validator


PLATAFORMAS_VALIDAS = {"PS5", "PS4", "XBOX", "PC", "SWITCH", "SNES", "N64"}


class VideojuegoBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100)
    categoria_id: int = Field(..., gt=0)
    plataforma: str = Field(...)
    precio_arriendo_diario: float = Field(..., gt=0)
    stock_total: int = Field(..., ge=0)

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


class VideojuegoCreate(VideojuegoBase):
    pass


class VideojuegoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=100)
    categoria_id: Optional[int] = Field(None, gt=0)
    plataforma: Optional[str] = None
    precio_arriendo_diario: Optional[float] = Field(None, gt=0)
    stock_total: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None

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


class VideojuegoResponse(VideojuegoBase):
    id: int
    stock_disponible: int
    activo: bool

    model_config = {
        "from_attributes": True
    }