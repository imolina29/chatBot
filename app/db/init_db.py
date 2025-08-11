from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.tienda import Base, engine, SessionLocal  # Asegúrate de que Base está definido correctamente aquí

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")