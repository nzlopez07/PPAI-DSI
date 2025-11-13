# Metadatos del paquete
__version__ = "1.0.0"
__author__ = "Sistema de Monitoreo Sísmico - DSI 2025"

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
