# ==========================================================
# ETAPA 1: BUILDER (Instala dependencias y prepara el entorno)
# ==========================================================

FROM python:3.12 as builder

# Instalar herramientas de compilación necesarias para algunas librerías de Python (ej. NumPy)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar todas las dependencias. 
# Esto incluye Gunicorn, Uvicorn, FastAPI, y librerías de ML.
# Usamos --no-cache-dir para ahorrar espacio.
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================================
# ETAPA 2: PRODUCCIÓN (Imagen final ligera para ejecución)
# ==========================================================
# Usamos la imagen 'slim' (más ligera) para el entorno final de producción
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# 🚨 COPIAR SOLAMENTE LAS LIBRERÍAS INSTALADAS (no las herramientas de compilación)
# Copia las librerías instaladas desde la etapa 'builder' a la imagen final.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copiar el resto de tu código fuente (tu aplicación FastAPI, app.main, la carpeta 'ml', etc.)
COPY . .

# El puerto que escuchará Gunicorn
EXPOSE 8000

# Comando de inicio: Usar Gunicorn para producción.
# -w 4: Número de workers (se recomienda 2 * núcleos + 1, ajusta según tu servidor)
# -k uvicorn.workers.UvicornWorker: El worker que usará Gunicorn para FastAPI
# app.main:app: La ubicación de tu objeto FastAPI
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
