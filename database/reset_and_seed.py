"""
Script seguro para reinicializar la base de datos y poblarla con datos de ejemplo.

Usos:
  # Ejecuta interactivo (pregunta confirmación)
  python -m database.reset_and_seed

  # Forzar (sin confirmación) y generar 20 eventos con 3 series y 8 muestras
  python -m database.reset_and_seed --yes --events 20 --series 3 --samples 8

    # Solo reset (drop + create + catálogos/usuarios), sin seed de eventos
    python -m database.reset_and_seed --no-seed --yes

    # Solo seed (no destructivo): no borra tablas, solo ejecuta el seeder para eventos
    python -m database.reset_and_seed --no-reset --yes --events 10 --series 2 --samples 5

Notas:
- Este script usa las funciones existentes en `database.init_db` para crear tablas y
  cargar catálogos/usuarios; y `database.seed_example_events.seed` para generar eventos.
- Hacer backup antes de ejecutar en entornos con datos importantes.
"""

import argparse
import sys
from database.config import engine, Base, SessionLocal
import database.init_db as init_db_mod
try:
    import database.seed_example_events as seed_mod
except Exception:
    seed_mod = None
    import database.migrate_data as migrate_mod

from sqlalchemy.exc import SQLAlchemyError


def parse_args():
    p = argparse.ArgumentParser(description="Resetear y poblar la base de datos de eventos sísmicos")
    p.add_argument("--yes", action="store_true", help="No pedir confirmación")
    p.add_argument("--no-seed", action="store_true", help="No generar eventos de ejemplo (solo crear tablas y catálogos)")
    p.add_argument("--no-reset", action="store_true", help="No realizar el reset (drop/create). Solo ejecutar el seed si corresponde")
    p.add_argument("--events", type=int, default=10, help="Cantidad de eventos a generar para el seed (default: 10)")
    p.add_argument("--series", dest="series_per_event", type=int, default=2, help="Series por evento en el seed (default: 2)")
    p.add_argument("--samples", dest="samples_per_series", type=int, default=5, help="Muestras por serie en el seed (default: 5)")
    return p.parse_args()


def confirm_or_abort(force: bool):
    if force:
        return True
    print("¡¡¡ATENCIÓN!!! Esto eliminará todas las tablas y datos de la base de datos configurada.")
    ans = input("Desea continuar? [y/N]: ")
    return ans.strip().lower() == 'y'


def reset_db():
    print("[reset_and_seed] Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("[reset_and_seed] All tables dropped.")

    print("[reset_and_seed] Creating tables...")
    # Reuse the helper in init_db module
    init_db_mod.create_tables()
    print("[reset_and_seed] Tables created.")

    # Open a session to load catalogs/users
    db = SessionLocal()
    try:
        print("[reset_and_seed] Loading catalogs...")
        init_db_mod.load_catalogs(db)
        print("[reset_and_seed] Loading test users...")
        init_db_mod.load_test_users(db)
    finally:
        db.close()


def run_seed(events: int, series_per_event: int, samples_per_series: int):
    print(f"[reset_and_seed] Running seed: events={events}, series_per_event={series_per_event}, samples_per_series={samples_per_series} ...")
    # Si existe el script seed_example_events lo usamos (permite generar muchos datos).
    if seed_mod is not None:
        # seed() ya crea tablas si hace falta y abre su propia sesión
        seed_mod.seed(events, series_per_event, samples_per_series)
        print("[reset_and_seed] Seed finished using seed_example_events.")
    else:
        # Fallback: usar migrate_data que asegura un conjunto mínimo si la BD está vacía
        print("[reset_and_seed] seed_example_events no disponible. Usando migrate_data para llenar datos mínimos.")
        migrate_mod.main()
        print("[reset_and_seed] Seed finished using migrate_data (minimal data).")


def main():
    args = parse_args()
    # If the user requested a reset, confirm the destructive action (unless --yes)
    if not args.no_reset:
        if not confirm_or_abort(args.yes):
            print("Aborted by user.")
            sys.exit(0)

    try:
        # Perform reset (drop/create) only when not in no-reset mode
        if not args.no_reset:
            reset_db()

        # Run seed unless explicitly disabled
        if not args.no_seed:
            run_seed(args.events, args.series_per_event, args.samples_per_series)

        print("[reset_and_seed] Done.")
    except SQLAlchemyError as e:
        print(f"[ERROR] SQLAlchemy error during reset/seed: {e}")
        raise
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        raise


if __name__ == '__main__':
    main()
