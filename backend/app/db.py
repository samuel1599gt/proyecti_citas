import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Cargar variables de entorno
load_dotenv()

# Configuración de la URL de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./citas.db")

# Creación del Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Configuración de la clase de Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Declarativa para los modelos ORM
Base = declarative_base()

# ----------------------------------------------------
# AÑADIDO CRÍTICO: Dependencia para la base de datos de FastAPI
# ----------------------------------------------------

def get_db():
    """
    Función generadora para crear una sesión de DB por solicitud (request)
    y asegurar que se cierre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión a la ruta/servicio
    finally:
        db.close() # Cierra la sesión después de que se completa la solicitud