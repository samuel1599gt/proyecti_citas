from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import (
    create_user,
    login_user,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(data, db)
    return {"message": "Usuario creado correctamente", "user": user}

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(data, db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(user = Depends(get_current_user)):
    return user
