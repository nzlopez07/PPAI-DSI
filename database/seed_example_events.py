"""
Seed script: generate synthetic seismic events with related series, samples and aggregated details.
Usage (PowerShell):
  python database/seed_example_events.py --events 20 --series-per-event 3 --samples-per-series 8
Idempotent: skips inserting an event if an existing event has same fecha_hora_ocurrencia and epicenter coords.
"""
import sys
from pathlib import Path
import argparse
import random
from datetime import datetime, timedelta

# Ensure root on path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from database.config import SessionLocal, init_db
from database.models import (
    EventoSismicoModel,
    SismografoModel,
    SerieTemporalModel,
    MuestraSismicaModel,
    DetalleMuestraSismicaModel,
    EstacionSismologicaModel
)
from database.models import TipoDeDatoModel
from database.repositories import EventoSismicoRepository

# Domain entities
from entities.EventoSismico import EventoSismico
from entities.CambioEstado import CambioEstado
from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from entities.AlcanceSismo import AlcanceSismo
from entities.MagnitudRichter import MagnitudRichter
from entities.Estado import AutoDetectado, PendienteDeRevision
from entities.SerieTemporal import SerieTemporal
from entities.MuestraSismica import MuestraSismica
from entities.DetalleMuestraSismica import DetalleMuestraSismica
from entities.TipoDeDato import TipoDeDato

TIPOS_DATOS = [
    TipoDeDato("Velocidad de onda", "km/seg", 10.0),
    TipoDeDato("Frecuencia de onda", "Hz", 15.0),
    TipoDeDato("Longitud de onda", "km/ciclo", 1.0),
]


def ensure_tipos_dato(db):
    """Inserta los tipos de dato del dominio en la tabla `tipos_de_dato` si no existen."""
    for tipo in TIPOS_DATOS:
        denominacion = tipo.getDenominacion()
        existente = db.query(TipoDeDatoModel).filter(
            TipoDeDatoModel.denominacion == denominacion
        ).first()
        if not existente:
            modelo = TipoDeDatoModel(
                denominacion=denominacion,
                nombre_unidad_medida=tipo.getNombreUnidadMedida(),
                valor_umbral=tipo.getValorUmbral()
            )
            db.add(modelo)
    db.commit()

# Catalog value pools (must match init_db inserted names to avoid duplicates)
ALCANCES = [
    ("Local", "Sismos que afectan áreas menores a 100 km del epicentro"),
    ("Regional", "Sismos que afectan regiones de cientos de kilómetros"),
    ("Lejano", "Sismos sentidos a gran distancia"),
]
CLASIFS = [
    (0, 70, "Superficial"),
    (70, 300, "Intermedio"),
    (300, 700, "Profundo"),
]
ORIGENES = [
    ("Tectónico", "Originado por movimiento de placas tectónicas"),
    ("Volcánico", "Originado por actividad volcánica"),
    ("Inducido", "Originado por actividad humana"),
]


def build_event(base_time: datetime) -> EventoSismico:
    """Create a domain EventoSismico with one CambioEstado (AutoDetectado or Pendiente)."""
    alcance_n = random.choice(ALCANCES)
    clasif_n = random.choice(CLASIFS)
    origen_n = random.choice(ORIGENES)

    alcance = AlcanceSismo(*alcance_n)
    clasif = ClasificacionSismo(clasif_n[0], clasif_n[1], clasif_n[2])
    origen = OrigenDeGeneracion(*origen_n)

    valor_magnitud = round(random.uniform(2.0, 6.5), 2)
    magnitud_num = round(valor_magnitud) if valor_magnitud >= 1 else 1.0
    magnitud = MagnitudRichter(f"Magnitud {magnitud_num}", magnitud_num)

    # State selection
    if random.random() < 0.5:
        estado_actual = AutoDetectado()
    else:
        estado_actual = PendienteDeRevision()

    cambio_inicial = CambioEstado(base_time, estado_actual, responsable=None)

    evento = EventoSismico(
        clasificacion=clasif,
        magnitud=magnitud,
        origenGeneracion=origen,
        alcanceSismo=alcance,
        estadoActual=estado_actual,
        cambiosEstado=[cambio_inicial],
        serieTemporal=[],  # filled later manually via ORM inserts
        fechaHoraOcurrencia=base_time,
        latitudEpicentro=round(random.uniform(-60.0, -20.0), 3),
        latitudHipocentro=round(random.uniform(-65.0, -25.0), 3),
        longitudEpicentro=round(random.uniform(-70.0, -50.0), 3),
        longitudHipocentro=round(random.uniform(-72.0, -52.0), 3),
        valorMagnitud=valor_magnitud,
        fechaHoraFin=None,
    )
    return evento


def ensure_min_sismografos(db, target: int = 10):
    """Create minimal stations + sismografos if none exist."""
    estaciones = db.query(EstacionSismologicaModel).count()
    if estaciones == 0:
        # Create stations
        for i in range(5):
            st = EstacionSismologicaModel(
                codigo_estacion=f"EST{i+1:02}",
                nombre=f"Estacion {i+1}",
                latitud=-30.0 - i,
                longitud=-60.0 + i,
                documento_certificacion_adq=None,
                nro_certificacion_adquisicion=None,
                fecha_solicitud_certificacion=None
            )
            db.add(st)
        db.commit()
    # Ensure sismografos
    estacion_objs = db.query(EstacionSismologicaModel).all()
    existing = db.query(SismografoModel).count()
    if existing >= target:
        return
    for i in range(existing, target):
        est = estacion_objs[i % len(estacion_objs)]
        s = SismografoModel(
            identificador_sismografo=f"SIS-{i+1:03}",
            nro_serie=f"SN-{random.randint(10000,99999)}",
            fecha_adquisicion=datetime.utcnow(),
            estacion_id=est.id
        )
        db.add(s)
    db.commit()


def seed(events: int, series_per_event: int, samples_per_series: int):
    init_db()
    db = SessionLocal()
    repo = EventoSismicoRepository(db)
    try:
        # Asegurar que existan tipos de dato en la BD
        ensure_tipos_dato(db)

        ensure_min_sismografos(db, target=max(5, events//3))
        sismografos = db.query(SismografoModel).all()
        sismografo_cycle = list(sismografos)

        inserted_events = 0
        inserted_series = 0
        inserted_samples = 0
        inserted_details = 0

        for idx in range(events):
            base_time = datetime.utcnow() - timedelta(hours=idx)
            # Idempotency check
            existing = db.query(EventoSismicoModel).filter(
                EventoSismicoModel.fecha_hora_ocurrencia == base_time
            ).first()
            if existing:
                continue
            evento = build_event(base_time)
            repo.save(evento)  # commits event & cambios estado
            db.flush()
            inserted_events += 1

            # Create series
            for sidx in range(series_per_event):
                sismografo = sismografo_cycle[(idx + sidx) % len(sismografo_cycle)]
                serie_model = SerieTemporalModel(
                    condicion_alarma=False,
                    fecha_hora_inicio_registro_muestras=base_time,
                    fecha_hora_registro=base_time + timedelta(minutes=1),
                    frecuencia_muestreo=50.0,
                    sismografo_id=sismografo.id,
                    evento_sismico_id=evento._db_id
                )
                db.add(serie_model)
                db.flush()
                inserted_series += 1

                # Samples
                for midx in range(samples_per_series):
                    muestra_time = base_time + timedelta(minutes=midx)
                    muestra_model = MuestraSismicaModel(
                        fecha_hora_muestra=muestra_time,
                        serie_temporal_id=serie_model.id
                    )
                    db.add(muestra_model)
                    db.flush()
                    inserted_samples += 1

                    # Aggregate detail (three values mapped)
                    velocidad = round(random.uniform(5.0, 15.0), 2)
                    frecuencia = round(random.uniform(8.0, 20.0), 2)
                    longitud = round(random.uniform(0.5, 2.0), 2)
                    detalle_model = DetalleMuestraSismicaModel(
                        velocidad_onda=velocidad,
                        frecuencia_onda=frecuencia,
                        longitud_onda=longitud,
                        muestra_sismica_id=muestra_model.id
                    )
                    db.add(detalle_model)
                    inserted_details += 1

            db.commit()
        print(f"✅ Seed completado: eventos={inserted_events}, series={inserted_series}, muestras={inserted_samples}, detalles={inserted_details}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error durante seed: {e}")
        raise
    finally:
        db.close()


def parse_args():
    p = argparse.ArgumentParser(description="Seed synthetic seismic data")
    p.add_argument("--events", type=int, default=10, help="Cantidad de eventos a generar")
    p.add_argument("--series-per-event", type=int, default=2, help="Series por evento")
    p.add_argument("--samples-per-series", type=int, default=5, help="Muestras por serie")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    seed(args.events, args.series_per_event, args.samples_per_series)
