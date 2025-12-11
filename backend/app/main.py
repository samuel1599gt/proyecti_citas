from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app.routes import auth_routes, citas_routes
import os
from dotenv import load_dotenv

# Cargar variables de entorno (necesario para el puerto, host, etc.)
load_dotenv()

# ----------------------------------------------------
# 1. INICIALIZACIÓN DE FASTAPI
# ----------------------------------------------------
app = FastAPI(
    title="API de Citas Médicas MVP",
    description="Backend para la gestión de usuarios y clasificación de citas médicas por ML.",
    version="1.0.0"
)

# ----------------------------------------------------
# 2. CREACIÓN DE TABLAS DE LA BASE DE DATOS
# ----------------------------------------------------
# Al iniciar la aplicación, crea todas las tablas (User y Cita) 
# definidas en tus modelos si no existen en la base de datos configurada en db.py.
Base.metadata.create_all(bind=engine)

# ----------------------------------------------------
# 3. CONFIGURACIÓN CORS (Para desarrollo de Frontend)
# ----------------------------------------------------
# Ajusta la lista 'origins' al dominio donde corre tu frontend
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),  # FRONTEND_URL de tu .env o valor por defecto
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Por seguridad, es mejor usar 'origins'
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Nota: Durante el desarrollo, 'allow_origins=["*"]' es común, 
# pero reemplázalo por 'allow_origins=origins' en producción para mayor seguridad.

# ----------------------------------------------------
# 4. REGISTRO DE RUTAS (Routers)
# ----------------------------------------------------
# Conecta los módulos de rutas revisados (auth y citas) a la aplicación principal.
app.include_router(auth_routes.router)
app.include_router(citas_routes.router)

# ----------------------------------------------------
# 5. RUTA RAIZ (Sanity Check)
# ----------------------------------------------------
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "API de Citas Médicas funcionando.", 
        "docs_url": "/docs"
    }
