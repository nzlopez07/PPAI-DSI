"""
Script histórico de migración refactorizado.

Este script ya NO depende de data.py (eliminado). Se conserva el nombre
por compatibilidad pero ahora genera un pequeño set inicial si la BD está vacía
o sugiere usar el nuevo script seed_example_events.py para grandes volúmenes.

Para generar muchos datos usar:
  python database/seed_example_events.py --events 50 --series-per-event 3 --samples-per-series 10
"""
import sys
from pathlib import Path
from datetime import datetime

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from database.config import SessionLocal, init_db
from database.repositories import EventoSismicoRepository
from database.models import EventoSismicoModel

from entities.EventoSismico import EventoSismico
from entities.CambioEstado import CambioEstado
from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from entities.AlcanceSismo import AlcanceSismo
from entities.MagnitudRichter import MagnitudRichter
from entities.Estado import AutoDetectado


def migrate_minimum_if_empty(db):
    """Inserta un mínimo de eventos sintéticos si la tabla está vacía."""
    count = db.query(EventoSismicoModel).count()
    if count > 0:
        print(f"   ℹ️  Ya existen {count} eventos. No se insertan mínimos. Use seed_example_events.py para más datos.")
        return
    repo = EventoSismicoRepository(db)
    print("   ➕ Insertando 3 eventos sintéticos mínimos...")
    for i in range(3):
        base_time = datetime.utcnow()
        alcance = AlcanceSismo("Local", "Sismo local inicial")
        clasif = ClasificacionSismo(0,70,"Superficial")
        origen = OrigenDeGeneracion("Tectónico","Origen tectónico")
        magnitud_val = 3.2 + i * 0.5
        magnitud = MagnitudRichter(f"Magnitud {round(magnitud_val)}", round(magnitud_val))
        estado = AutoDetectado()
        cambio = CambioEstado(base_time, estado, responsable=None)
        evento = EventoSismico(
            clasificacion=clasif,
            magnitud=magnitud,
            origenGeneracion=origen,
            alcanceSismo=alcance,
            estadoActual=estado,
            cambiosEstado=[cambio],
            serieTemporal=[],
            fechaHoraOcurrencia=base_time,
            latitudEpicentro=-30.0 - i,
            latitudHipocentro=-31.0 - i,
            longitudEpicentro=-60.0 + i,
            longitudHipocentro=-61.0 + i,
            valorMagnitud=magnitud_val,
            fechaHoraFin=None
        )
        repo.save(evento)
    print("   ✅ Inserción mínima completada")


# Las funciones de migración de catálogos/estaciones/sismógrafos/usuarios basadas en data.py
# fueron eliminadas. Los catálogos se crean en init_db y los datos masivos ahora se generan
# con database/seed_example_events.py


def migrate_eventos(db):
    """Conservado por compatibilidad: ahora solo asegura mínimos si vacío."""
    migrate_minimum_if_empty(db)


def main():
    """Ejecuta la migración completa"""
    print("=" * 60)
    print("  MIGRACION BÁSICA (refactor) - usar seed_example_events.py para datos masivos")
    print("=" * 60)
    
    # Inicializar BD (si no existe)
    init_db()
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Solo asegura que haya algunos eventos iniciales si no hay datos
        migrate_eventos(db)
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN BÁSICA COMPLETADA")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
