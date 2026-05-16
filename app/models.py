"""Modelos Pydantic para validación de datos de sensores industriales."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator, ValidationInfo

# Rangos válidos por tipo de sensor (mínimo, máximo).
RANGOS: dict[str, tuple[float, float]] = {
    "temperatura": (-10.0, 100.0),
    "presion": (0.0, 500.0),
    "vibracion": (0.0, 5.0),
}

TipoSensor = Literal["temperatura", "presion", "vibracion"]


class SensorBase(BaseModel):
    """Modelo base con los campos comunes de un sensor industrial."""

    tipo: TipoSensor = Field(..., description="Tipo de sensor")
    valor: float = Field(..., description="Lectura del sensor")
    ubicacion: str = Field(..., min_length=1, max_length=100, description="Ubicación física del sensor")
    fecha: datetime = Field(..., description="Fecha de la lectura en formato ISO 8601")

    @field_validator("valor")
    @classmethod
    def validar_rango(cls, v: float, info: ValidationInfo) -> float:
        """Verifica que el valor esté dentro del rango permitido según el tipo."""
        tipo = info.data.get("tipo")
        if tipo and tipo in RANGOS:
            minimo, maximo = RANGOS[tipo]
            if not minimo <= v <= maximo:
                raise ValueError(f"{tipo} debe estar entre {minimo} y {maximo}")
        return v


class SensorCreate(SensorBase):
    """Modelo utilizado para crear un nuevo sensor. Hereda de SensorBase sin cambios."""
    pass


class SensorUpdate(BaseModel):
    """Modelo para actualizar un sensor. Todos los campos son opcionales y no incluye tipo."""
    
    valor: Optional[float] = Field(None, description="Nueva lectura del sensor")
    ubicacion: Optional[str] = Field(None, min_length=1, max_length=100, description="Nueva ubicación")
    fecha: Optional[datetime] = Field(None, description="Nueva fecha de lectura")

    # Nota: No implementamos la validación de rango cruzada aquí mediante @field_validator
    # porque en la actualización Pydantic no tiene el campo "tipo" (está en la URL, no en el body).
    # Esa validación se hará a mano en el endpoint PUT (main.py).


class SensorOut(SensorBase):
    """Modelo de salida que incluye el identificador generado por la base de datos."""
    
    id: str = Field(..., description="ID único del documento en MongoDB")
