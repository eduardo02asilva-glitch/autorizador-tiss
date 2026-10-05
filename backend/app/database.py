import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL padrão para rodar localmente na sua máquina
DEFAULT_DB_URL = "postgresql+psycopg2://tiss_user:tiss_password@localhost:5432/autorizador_tiss_db"

# Lê a URL do ambiente (Docker) ou usa a local como padrão
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Garante que o driver +psycopg2 seja usado mesmo que o Docker injete apenas "postgresql://"
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()