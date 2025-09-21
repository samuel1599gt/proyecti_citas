# Etapa 1: Build
FROM node:20-alpine AS build

# Crear directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Construir la app de producción
RUN npm run build

# Etapa 2: Servir con un servidor ligero
FROM nginx:1.27-alpine

# Copiar los archivos de build a Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Exponer puerto
EXPOSE 3000

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]
