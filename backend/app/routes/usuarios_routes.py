from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.utils import hash_password, verify_password

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/registrarse", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def registrarse(usuario: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario (registrarse)"""
    # Verificar que el correo no esté registrado
    usuario_existente = db.query(User).filter(User.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear nuevo usuario
    nuevo_usuario = User(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        password_hash=hash_password(usuario.password)
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


@router.post("/login")
def login(credenciales: UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    # Buscar el usuario por correo
    usuario = db.query(User).filter(User.correo == credenciales.correo).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(credenciales.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos"
        )
    
    return {
        "id": usuario.id,
        "correo": usuario.correo,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "mensaje": "Login exitoso"
    }


@router.get("/", response_model=List[UserOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    """Obtener todos los usuarios"""
    usuarios = db.query(User).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UserOut)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por su ID"""
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.get("/correo/{correo}", response_model=UserOut)
def obtener_usuario_por_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un usuario por su correo"""
    usuario = db.query(User).filter(User.correo == correo).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario
