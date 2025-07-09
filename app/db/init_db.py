from .database import Base, engine
from .models import Conversacion, Producto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def init_db():
    Base.metadata.create_all(bind=engine)

DATABASE_URL = "sqlite:///app/db/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)