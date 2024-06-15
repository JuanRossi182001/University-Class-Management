
# establesco la imagen de python que voy a utilizar
FROM python:3.12.1

# establesco directorio de trabajo  
WORKDIR /UniversityClassManagement

# copio archivos de requisitos e instalo dependencias 
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

# Copio el contenido de la app en el contenedor de Docker 
COPY . .

# Expongo el puerto que utilizara FastAPI
EXPOSE 8000


# Comando para ejecutar la app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]


