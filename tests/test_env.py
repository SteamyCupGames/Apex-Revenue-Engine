import os
from dotenv import load_dotenv

# Esto fuerza la carga si VSCode no lo hizo automáticamente
load_dotenv() 

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path:
    print(f"✅ Variable detectada: {credentials_path}")
    if os.path.exists(credentials_path):
        print("✅ El archivo JSON existe en esa ruta.")
    else:
        print("❌ La ruta existe en el .env, pero el archivo físico NO está ahí.")
else:
    print("❌ La variable NO ha sido detectada.")