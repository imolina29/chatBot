# scripts/crear_tablas.py

import sys
import os

# Asegura que la app sea importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.init_db import engine, Base
from app.db.models import Conversacion, Producto
from app.db import models

if __name__ == "__main__":
    print("📦 Creando las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")