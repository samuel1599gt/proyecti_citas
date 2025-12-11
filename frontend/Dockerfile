# ==========================================================
# Etapa 1: Build (Compilación de la aplicación React)
# ==========================================================
FROM node:20-alpine AS build

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente del frontend
COPY . .

# Construir la app de producción (Genera la carpeta 'build' si usas CRA)
RUN npm run build

# ==========================================================
# Etapa 2: Servir con un servidor ligero (NGINX)
# ==========================================================
FROM nginx:1.27-alpine

# Eliminar el archivo de configuración por defecto de Nginx 
# (Opcional, pero bueno si usas tu propia configuración)
# RUN rm /etc/nginx/conf.d/default.conf

# 🚨 CORRECCIÓN/VERIFICACIÓN: 
# Copiar los archivos de la carpeta de salida (cambiar 'dist' por 'build' si usaste CRA)
COPY --from=build /app/build /usr/share/nginx/html

# Exponer el puerto estándar de Nginx
EXPOSE 80

# 🚨 NOTA: Nginx escucha por defecto en el puerto 80.
# Cambié la línea de EXPOSE de 3000 a 80, que es el puerto HTTP estándar para Nginx.
# Asegúrate de mapear el puerto 80 del contenedor a 80/3000 de tu host en el docker-compose.yml. 
# Si el puerto 3000 es crítico para ti, déjalo en 3000, pero 80 es la convención para Nginx.

# Comando por defecto para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]
