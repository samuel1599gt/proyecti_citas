# ==========================================================
# ETAPA 1: BUILD (Compilación y obtención de dependencias)
# CRÍTICO: Definir el alias "builder"
# ==========================================================
FROM python:3.12 AS builder

# Establecer directorio de trabajo para la Etapa 1
WORKDIR /tmp/build

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ==========================================================
# ETAPA 2: PRODUCCIÓN (Imagen final ligera para ejecución)
# ==========================================================
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# 💡 CORRECCIÓN 1: Asegurar que Python vea el directorio /app/app
ENV PYTHONPATH=/app

# 🚨 CORRECCIÓN 2: Instalar dependencias del sistema requeridas para librerías Python (como la base de datos)
# Esto incluye las librerías necesarias para que SQLite y psycopg2 (si se usara PostgreSQL) funcionen
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    # SQLite
    libsqlite3-dev \
    # Limpieza
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar las LIBRERÍAS (Desde la etapa "builder")
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copiar los BINARIOS (gunicorn)
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/

# 🛑 CRÍTICO 3: Copiar el código fuente. Esto copia 'backend/app', 'citas.db', etc., a '/app/'
COPY . . 

# El puerto que escuchará Gunicorn
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]