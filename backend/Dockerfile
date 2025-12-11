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
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

ENV PYTHONPATH=/app

# 🚨 COPIAR las LIBRERÍAS (Archivos .py, etc.)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# 🚨 CRÍTICO: COPIAR los BINARIOS (Ejecutables como 'gunicorn')
# Los ejecutables se encuentran en /usr/local/bin
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/

# Copiar el resto de tu código fuente 
COPY . .

# El puerto que escuchará Gunicorn
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]