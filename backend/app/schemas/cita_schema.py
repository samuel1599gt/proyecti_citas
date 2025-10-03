from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CitaBase(BaseModel):
    sintomas: str
    zona_afectada: str
    condiciones_previas: Optional[str] = None
    tiempo_con_sintomas: str
    edad: int
    sexo: str


class CitaCreate(CitaBase):
    user_id: int   # el ID del usuario al que se asigna la cita


class CitaResponse(CitaBase):
    id: int
    user_id: int
    fecha_solicitud: datetime
    prioridad: Optional[str] = None

    class Config:
        orm_mode = True