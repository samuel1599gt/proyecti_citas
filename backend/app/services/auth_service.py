from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.db import get_db

SECRET_KEY = "MI_SUPER_SECRETO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------
# Funciones internas
# ------------------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


# ------------------------
# CRUD de Usuario
# ------------------------

def create_user(data: UserCreate, db: Session):
    user = db.query(User).filter(User.correo == data.correo).first()
    if user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    new_user = User(
        nombre=data.nombre,
        apellido=data.apellido,
        correo=data.correo,
        password_hash=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(data: UserLogin, db: Session):
    user = db.query(User).filter(User.correo == data.correo).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode(
        {"sub": user.correo, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ------------------------
# Tokens y Validación
# ------------------------

def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.correo == correo).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return get_user_from_token(token, db)
