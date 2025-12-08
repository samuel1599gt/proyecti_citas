from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.models.cita_model import Cita
from app.models.user_model import User
from app.schemas.cita_schema import CitaCreate, CitaResponse

router = APIRouter(prefix="/citas", tags=["Citas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita"""
    usuario = db.query(User).filter(User.id == cita.user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    nueva_cita = Cita(
        user_id=cita.user_id,
        sintomas=cita.sintomas,
        zona_afectada=cita.zona_afectada,
        condiciones_previas=cita.condiciones_previas,
        tiempo_con_sintomas=cita.tiempo_con_sintomas,
        edad=cita.edad,
        sexo=cita.sexo
    )
    
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    
    return nueva_cita


@router.get("/", response_model=List[CitaResponse])
def obtener_todas_citas(db: Session = Depends(get_db)):
    """Obtener todas las citas"""
    citas = db.query(Cita).all()
    return citas


@router.get("/usuario/{user_id}", response_model=List[CitaResponse])
def obtener_citas_por_usuario(user_id: int, db: Session = Depends(get_db)):
    """Obtener todas las citas de un usuario específico"""
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    citas = db.query(Cita).filter(Cita.user_id == user_id).all()
    return citas


@router.get("/{cita_id}", response_model=CitaResponse)
def obtener_cita_por_id(cita_id: int, db: Session = Depends(get_db)):
    """Obtener una cita específica por su ID"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    return cita


@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(cita_id: int, cita_actualizada: CitaCreate, db: Session = Depends(get_db)):
    """Actualizar una cita existente"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    cita.sintomas = cita_actualizada.sintomas
    cita.zona_afectada = cita_actualizada.zona_afectada
    cita.condiciones_previas = cita_actualizada.condiciones_previas
    cita.tiempo_con_sintomas = cita_actualizada.tiempo_con_sintomas
    cita.edad = cita_actualizada.edad
    cita.sexo = cita_actualizada.sexo
    
    db.commit()
    db.refresh(cita)
    
    return cita


@router.delete("/{cita_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    """Eliminar una cita"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    db.delete(cita)
    db.commit()
    
    return None
