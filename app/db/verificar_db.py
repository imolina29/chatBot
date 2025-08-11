# verificar_db.py
import sqlite3
import os

# Ruta al archivo tienda.db
DB_PATH = os.path.join(os.path.dirname(__file__), "tienda.db")

def verificar_db():
    if not os.path.exists(DB_PATH):
        print("❌ La base de datos no existe en:", DB_PATH)
        return

    print(f"✅ Conectando a la base de datos: {DB_PATH}\n")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    if not tablas:
        print("⚠️ No hay tablas en la base de datos.")
        return

    print("📦 Tablas encontradas:\n")
    for (tabla,) in tablas:
        print(f"🔹 {tabla}")
        cursor.execute(f"PRAGMA table_info({tabla})")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"   - {col[1]} ({col[2]})")
        print()

    conn.close()

if __name__ == "__main__":
    verificar_db()