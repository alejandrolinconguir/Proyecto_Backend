from typing import Any
from pydantic import BaseModel

#representa lo que está dentro de error
class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[Any] = []

#representa el objeto completo
class ErrorResponseWrapper(BaseModel):
    error: ErrorResponse