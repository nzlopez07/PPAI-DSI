"""
Ensure the database has at least N events by running the seeder for the missing amount.
Usage:
  python -m database.ensure_total_events --total 100 [--series 2 --samples 5]
This is non-destructive: it will not drop/create tables.
"""
import argparse
import sys
from database.config import SessionLocal
from database.models import EventoSismicoModel

try:
    import database.seed_example_events as seed_mod
except Exception as e:
    print("seed_example_events not available:", e)
    seed_mod = None


def parse_args():
    p = argparse.ArgumentParser(description="Ensure total number of events in DB by seeding missing ones")
    p.add_argument("--total", type=int, required=True, help="Total desired events in DB")
    p.add_argument("--series", dest="series_per_event", type=int, default=2, help="Series per event for new seeded events")
    p.add_argument("--samples", dest="samples_per_series", type=int, default=5, help="Samples per series for new seeded events")
    return p.parse_args()


def main():
    args = parse_args()
    db = SessionLocal()
    try:
        existing = db.query(EventoSismicoModel).count()
    finally:
        db.close()

    print(f"Existing events in DB: {existing}")
    if existing >= args.total:
        print("No work needed - DB already has desired number of events.")
        return

    needed = args.total - existing
    print(f"Need to seed {needed} events (to reach total {args.total}).")

    if seed_mod is None:
        print("No seeder module available. Aborting.")
        sys.exit(1)

    # Call the seeder to create exactly `needed` events
    seed_mod.seed(needed, args.series_per_event, args.samples_per_series)
    print("Seeding finished. Verify counts if needed.")


if __name__ == '__main__':
    main()
