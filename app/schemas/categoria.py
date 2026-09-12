from typing import Optional
from pydantic import BaseModel, Field, field_validator

ESTADOS_VALIDOS = {"Activa", "Inactiva"}


class CategoriaBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre de la categoría (ej. Acción, RPG)",
    )
    descripcion: str = Field(
        ...,
        min_length=5,
        max_length=200,
        description="Descripción de la categoría",
    )
    edad_minima: int = Field(
        ...,
        ge=0,
        le=18,
        description="Edad mínima recomendada para esta categoría",
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        valor_limpio = valor.strip()
        if not valor_limpio:
            raise ValueError("El nombre no puede estar vacío o solo espacios")
        return valor_limpio


class CategoriaCreate(CategoriaBase):
    """DTO de entrada para crear una Categoria (POST).

    No incluye 'id_categoria' (lo genera el repository) ni 'estado'
    (toda categoría nueva empieza como 'Activa').
    """
    pass


class CategoriaUpdate(BaseModel):
    """DTO de entrada para actualizar una Categoria (PUT/PATCH)."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, min_length=5, max_length=200)
    edad_minima: Optional[int] = Field(None, ge=0, le=18)
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


class CategoriaResponse(CategoriaBase):
    """DTO de salida: lo que la API devuelve al cliente."""
    id_categoria: int
    estado: str

    model_config = {
        "from_attributes": True
    }