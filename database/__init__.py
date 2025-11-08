"""
Paquete de persistencia con SQLAlchemy para el sistema de eventos sísmicos.

Este paquete proporciona:
- Modelos ORM (database.models)
- Repositorios con patrón Data Mapper (database.repositories)
- Configuración de base de datos (database.config)
- Scripts de inicialización (database.init_db)

Uso básico:
    from database.config import SessionLocal, init_db
    from database.repositories import EventoSismicoRepository
    
    # Inicializar BD (solo primera vez)
    init_db()
    
    # Crear sesión y repositorio
    db = SessionLocal()
    repo = EventoSismicoRepository(db)
    
    # Usar repositorio
    eventos = repo.get_auto_detectados_y_pendientes()
    
    # Cerrar sesión
    db.close()
"""

__version__ = "1.0.0"
__author__ = "Sistema de Monitoreo Sísmico - DSI 2025"

# Imports principales para facilitar el uso
from database.config import SessionLocal, init_db, get_db, engine, Base
from database.repositories import (
    EventoSismicoRepository,
    EmpleadoRepository,
    UsuarioRepository,
    nombre_estado_to_instance,
    instance_to_nombre_estado
)

__all__ = [
    # Config
    "SessionLocal",
    "init_db",
    "get_db",
    "engine",
    "Base",
    # Repositorios
    "EventoSismicoRepository",
    "EmpleadoRepository",
    "UsuarioRepository",
    # Utilidades Estado
    "nombre_estado_to_instance",
    "instance_to_nombre_estado",
]
