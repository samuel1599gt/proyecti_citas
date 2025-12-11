import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# -----------------------
# CONFIGURACIÓN JWT
# -----------------------

SECRET_KEY = os.getenv("JWT_SECRET", "MI_SUPER_SECRETO")  # <-- corregido
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# -----------------------
# CONFIGURACIÓN BASE DE DATOS
# -----------------------

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./citas.db")

# -----------------------
# VARIABLES DE LA APP
# -----------------------

APP_NAME = os.getenv("PROJECT_NAME", "API Citas Médicas")
APP_VERSION = "1.0.0"
