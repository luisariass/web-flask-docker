# Usa una imagen base oficial de Python (se recomienda 3.9 o 3.11 para estabilidad)
FROM python:3.9-slim

# Establece el directorio de trabajo DENTRO del contenedor
WORKDIR /app

# Copia el archivo de requerimientos (ahora está en la raíz del contexto)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO el contenido del directorio actual (el contexto de build)
# al WORKDIR (/app) dentro del contenedor.
# Esto incluye app.py, templates/, static/, etc.
COPY . .

# Expone el puerto
EXPOSE 5000

# Define las variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Ejecuta la aplicación con el servidor de desarrollo de Flask
CMD ["flask", "run"]