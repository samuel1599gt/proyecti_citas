from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.cita_schema import CitaCreate, CitaBase, CitaOut, CitaCancelStatus
from app.services.auth_service import get_current_user # Usa este para obtener el usuario
from app.auth.auth_bearer import JWTBearer 
from app.models.user_model import User
from app.services.cita_service import crear_cita, obtener_citas, cancelar_cita # Importación consolidada
from typing import List


router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)

@router.post(
    "/", 
    response_model=CitaOut,
    summary="Crear una nueva cita",
    dependencies=[Depends(JWTBearer())] # Asegura la protección de la ruta
)
def crear(
    data: CitaBase,  # El esquema Pydantic para la entrada
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user) # Obtiene el objeto User
):
    """Crea una cita para el usuario autenticado."""
    return crear_cita(data, user.id, db)

@router.get(
    "/me/", 
    response_model=List[CitaOut],
    summary="Obtener todas las citas del usuario logueado",
    dependencies=[Depends(JWTBearer())]
)
# 🎯 CORRECCIÓN: Usamos /me/ para claridad y get_current_user para consistencia
def listar_citas(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user) 
):
    """
    Obtiene todas las citas agendadas por el usuario autenticado.
    """
    # Llama a la función de servicio que usa user.id
    return obtener_citas(user_id=user.id, db=db)
    
@router.delete(
    "/{cita_id}", 
    response_model=CitaCancelStatus, 
    status_code=status.HTTP_200_OK,
    summary="Eliminar una cita por ID",
    dependencies=[Depends(JWTBearer())] # Ruta protegida
)
def cancelar_cita_existente(
    cita_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user) # Obtiene el objeto User para verificar propiedad
):
    """
    Cancela una cita por su ID. Solo el propietario puede eliminarla.
    """
    # Llama al servicio de cancelación
    if cancelar_cita(cita_id=cita_id, user_id=user.id, db=db):
        return CitaCancelStatus(success=True, message=f"Cita con ID {cita_id} cancelada exitosamente.")
    
    # Si la cancelación devuelve False (no existe o no es del usuario)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Cita no encontrada o no tienes permiso para cancelarla."
    )