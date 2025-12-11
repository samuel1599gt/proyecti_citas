# (Omitiendo la Etapa 1: BUILD)

# ==========================================================
# ETAPA 2: PRODUCCIÓN (Imagen final ligera para ejecución)
# ==========================================================
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# 💡 CORRECCIÓN 1: Asegurar que Python vea el directorio /app/app
ENV PYTHONPATH=/app

# 🚨 CORRECCIÓN 2: Asegurar que se instale el paquete necesario para SQLite en slim
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

# 🛑 CRÍTICO: Copiar el código fuente. Esto copia 'backend/app' a '/app/app'.
COPY . . 

# El puerto que escuchará Gunicorn
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]