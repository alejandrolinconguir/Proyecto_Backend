import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator

ESTADOS_VALIDOS = {"Activo", "Inactivo"}

# Patrón simple de correo: algo@algo.algo
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Patrón simple de teléfono: solo dígitos, espacios, + y guiones, 7-15 caracteres
PATRON_TELEFONO = re.compile(r"^[\d\s\+\-]{7,15}$")


class ClienteBase(BaseModel):
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre del cliente",
    )
    apellido: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Apellido del cliente",
    )
    correo: str = Field(
        ...,
        description="Correo electrónico del cliente",
    )
    telefono: str = Field(
        ...,
        description="Teléfono de contacto del cliente",
    )

    @field_validator("nombre", "apellido")
    @classmethod
    def validar_no_vacio(cls, valor: str) -> str:
        valor_limpio = valor.strip()
        if not valor_limpio:
            raise ValueError("Este campo no puede estar vacío o solo espacios")
        return valor_limpio

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: str) -> str:
        valor_limpio = valor.strip().lower()
        if not PATRON_CORREO.match(valor_limpio):
            raise ValueError("El correo no tiene un formato válido (ej. usuario@dominio.com)")
        return valor_limpio

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor: str) -> str:
        valor_limpio = valor.strip()
        if not PATRON_TELEFONO.match(valor_limpio):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos (puede incluir +, espacios o guiones)")
        return valor_limpio


class ClienteCreate(ClienteBase):
    """DTO de entrada para crear un Cliente (POST).

    No incluye 'id_cliente' (lo genera el repository) ni 'estado'
    (todo cliente nuevo empieza como 'Activo').
    """
    pass


class ClienteUpdate(BaseModel):
    """DTO de entrada para actualizar un Cliente (PUT/PATCH)."""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    apellido: Optional[str] = Field(None, min_length=2, max_length=50)
    correo: Optional[str] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return valor
        valor_limpio = valor.strip().lower()
        if not PATRON_CORREO.match(valor_limpio):
            raise ValueError("El correo no tiene un formato válido (ej. usuario@dominio.com)")
        return valor_limpio

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, valor: Optional[str]) -> Optional[str]:
        if valor is None:
            return valor
        valor_limpio = valor.strip()
        if not PATRON_TELEFONO.match(valor_limpio):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos (puede incluir +, espacios o guiones)")
        return valor_limpio

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


class ClienteResponse(ClienteBase):
    """DTO de salida: lo que la API devuelve al cliente."""
    id_cliente: int
    estado: str

    model_config = {
        "from_attributes": True
    }