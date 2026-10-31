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


# Descripciones que se muestran en Swagger (/docs) para cada código de error
DESCRIPCIONES_ERROR = {
    400: "Solicitud inválida",
    404: "Recurso no encontrado",
    409: "Conflicto con los datos existentes",
    422: "Error de validación de los datos enviados",
}


# Arma el parámetro 'responses' de un endpoint con el formato de error del proyecto.
# Ejemplo: responses=respuestas_error(404, 409)
def respuestas_error(*codigos: int) -> dict:
    return {
        codigo: {
            "model": ErrorResponseWrapper,
            "description": DESCRIPCIONES_ERROR[codigo],
        }
        for codigo in codigos
    }
