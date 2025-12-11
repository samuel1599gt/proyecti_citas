# backend/app/schemas/cita_schema.py

from pydantic import BaseModel, Field, field_validator # Importaciones necesarias
from pydantic.fields import FieldInfo 
from datetime import datetime
from typing import Optional, List, Any # Añadir Any para la validación de tipo mixto

# Datos fijos (No se usan para validación de contenido, solo para referencia)
ZONAS = ["Cabeza", "Pecho", "Abdomen", "Garganta", "Piernas", "Brazos",
         "Espalda", "Estómago", "Corazón", "Pulmones", "Ninguna"]

SINTOMAS = ["Fiebre", "Dolor", "Mareo", "Tos", "Náuseas", "Inflamación",
            "Dificultad respiratoria", "Cansancio", "Escalofríos", "Vómito", "Ninguno"]

CONDICIONES_PREVIAS = ["Hipertensión", "Cardiaco", "Diabetes", "Asma", "Obesidad",
                       "Artritis", "Migraña", "Alergias", "Epilepsia", "Colesterol alto", "Ninguna"]


class CitaBase(BaseModel):
    sintomas: List[str] = Field(..., description="Máximo 3 síntomas o Ninguno")
    zona_afectada: List[str] = Field(..., description="Máximo 3 zonas afectadas o Ninguna")
    condiciones_previas: Optional[List[str]] = Field(default=None, description="Máximo 3 condiciones previas o Ninguna")
    
    tiempo_sintomas: int = Field(..., ge=0, le=30, description="Días con síntomas (0-30)") 
    
    edad: int = Field(..., ge=1, le=100, description="Edad del paciente (1-100)")
    sexo: str = Field(..., description="Sexo del paciente (male/female)")

    # -------------------- VALIDACIONES V2 --------------------
    
    @field_validator("sintomas", "zona_afectada", "condiciones_previas", mode='before')
    @classmethod
    def validar_opciones(cls, v: Any, info: FieldInfo) -> List[str] | None:
        if v is None:
            return None
        
        field_name = info.field_name
        
        # 1. PASO CRÍTICO: Convertir el string separado por coma (del frontend) a lista
        if isinstance(v, str):
            # Split por coma y limpiar espacios en blanco
            # 💡 Mejora: Si el string está vacío (ej. condiciones_previas opcional), devuelve None/lista vacía
            v_list = [item.strip() for item in v.split(',') if item.strip()]
        elif isinstance(v, list):
            v_list = v # Si ya es lista, la usamos
        else:
            # Esto maneja entradas que no son str ni List[str]
            raise ValueError(f"Formato inesperado para {field_name}")
            
        if not v_list:
            return None # Devolvemos None si la lista está vacía después de la limpieza
            
        # 2. Máximo 3 seleccionadas (excluyendo 'Ninguna'/'Ninguno' si está presente solo)
        if len(v_list) > 3:
            raise ValueError(f"En '{field_name}' solo se pueden seleccionar máximo 3 opciones")

        # 3. Si elige 'Ninguna' o 'Ninguno', no puede elegir otra
        ninguna_opciones_lower = {"ninguna", "ninguno"}
        
        # Convertir a minúsculas para la comprobación
        v_list_lower = [op.lower() for op in v_list]
        
        # 🚨 CORRECCIÓN DE LÓGICA: Si hay alguna opción de exclusión...
        if any(op in ninguna_opciones_lower for op in v_list_lower):
            # ... y el número de opciones es mayor a 1, lanzar error.
            if len(v_list) > 1:
                raise ValueError(f"Si selecciona una opción de exclusión ('Ninguna/Ninguno'), no puede elegir más opciones en '{field_name}'")
        
        # Retornar la lista procesada
        return v_list

    @field_validator("sexo", mode='before') 
    @classmethod
    def validar_sexo(cls, v: Any) -> str:
        if isinstance(v, str) and v.lower() not in ["male", "female"]:
            raise ValueError("El sexo debe ser 'male' o 'female'")
        return v.lower()


class CitaCreate(CitaBase):
    # Hereda la validación y campos de CitaBase
    pass


class CitaOut(CitaBase):
    id: int
    user_id: int
    fecha_solicitud: datetime
    prioridad: Optional[str] = Field(default="Sin Clasificar", description="Prioridad asignada por el modelo ML")

    class Config:
        # 💡 Pydantic V2: Usamos from_attributes = True en lugar de orm_mode = True
        from_attributes = True 

class CitaCancelStatus(BaseModel):
    success: bool
    message: str