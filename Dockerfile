# 1. Imagen base ligera de Python
FROM python:3.14-slim

# 2. Directorio de trabajo
WORKDIR /app

# 3. Instalación de dependencias (Capa de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar estructura modular del proyecto
# Copiamos solo lo necesario para la inferencia y la consola SDR
COPY app/ ./app/
COPY Model/ ./Model/
COPY src/ ./src/

# 5. Exponer el puerto por defecto de Streamlit
EXPOSE 8501

# 6. Variables de entorno para evitar buffers de logs
ENV PYTHONUNBUFFERED=1

# 7. Comando para ejecutar la SDR Priority Console
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]