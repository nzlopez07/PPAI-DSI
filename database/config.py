"""
Configuración de la base de datos SQLAlchemy para el sistema de eventos sísmicos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

_DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "eventos_sismicos.db"))
_DEFAULT_DB_PATH = _DEFAULT_DB_PATH.replace("\\", "/")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_DEFAULT_DB_PATH}")

_echo_env = os.getenv("SQLALCHEMY_ECHO", "0")
echo = str(_echo_env).lower() in ("1", "true", "yes")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=echo
)


if not echo:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
else:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency para obtener una sesión de base de datos.
    Se usa en Flask para inyectar la sesión en las rutas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    """
    from database import models
    
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")

def drop_all_tables():
    """
    Elimina todas las tablas (útil para testing o resetear la BD).
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas han sido eliminadas")
