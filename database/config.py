"""
Configuración de la base de datos SQLAlchemy para el sistema de eventos sísmicos.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# URL de la base de datos (SQLite por defecto para desarrollo)
# Puedes cambiar esto a PostgreSQL, MySQL, etc.
# Usamos una ruta ABSOLUTA por defecto para evitar problemas de CWD (especialmente en Windows con rutas con acentos)
_DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "eventos_sismicos.db"))
# Normalizar separadores para SQLAlchemy
_DEFAULT_DB_PATH = _DEFAULT_DB_PATH.replace("\\", "/")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_DEFAULT_DB_PATH}")

# Crear el engine de SQLAlchemy
# Control de verbosity: `echo` controla que SQLAlchemy imprima cada sentencia SQL.
# Lo leemos desde la variable de entorno SQLALCHEMY_ECHO para poder activarlo
# temporalmente sin editar código (valores aceptados: 1/true/yes).
_echo_env = os.getenv("SQLALCHEMY_ECHO", "0")
echo = str(_echo_env).lower() in ("1", "true", "yes")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=echo
)

# Ajustar el logger para evitar mensajes verbosos adicionales de SQLAlchemy
# cuando echo está desactivado.
if not echo:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
else:
    # Si se desea debug más detallado se puede bajar el nivel a INFO/DEBUG.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos declarativos
Base = declarative_base()

def get_db():
    """
    Dependency para obtener una sesión de base de datos.
    Se usa en Flask/FastAPI para inyectar la sesión en las rutas.
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
    # Importar todos los modelos aquí para que SQLAlchemy los registre
    from database import models
    
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")

def drop_all_tables():
    """
    Elimina todas las tablas (útil para testing o resetear la BD).
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas han sido eliminadas")
