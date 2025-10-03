from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime


class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del usuario")
    apellido: str = Field(..., min_length=2, max_length=50, description="Apellido del usuario")
    correo: EmailStr
    password: str = Field(..., min_length=6, max_length=32, description="Contraseña del usuario")
    password_repeat: str = Field(..., min_length=6, max_length=32, description="Repetición de la contraseña")

    @validator("password_repeat")
    def validar_passwords(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Las contraseñas no coinciden")
        return v


class UserLogin(BaseModel):
    correo: EmailStr
    password: str = Field(..., min_length=6, max_length=32)


class UserOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: EmailStr
    fecha_creacion: datetime

    class Config:
        orm_mode = True