from entities.EventoSismico import EventoSismico
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
from entities.AlcanceSismo import AlcanceSismo
from entities.SerieTemporal import SerieTemporal
from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from entities.Sismografo import Sismografo
from entities.EstacionSismologica import EstacionSismologica
from datetime import datetime

# Mocks simples para objetos referenciales
clasificacion_mock = [
    ClasificacionSismo(0, 70, "Superficial"),
    ClasificacionSismo(71, 300, "Intermedio"),
    ClasificacionSismo(301, 700, "Profundo")
]

magnitud = None       # Reemplazar por un mock si es necesario

origen_mock = [
    OrigenDeGeneracion("Tectónico", "Causado por el movimiento de las placas tectónicas.."), 
    OrigenDeGeneracion("Volcánico", "Originado por el ascenso de magma en zonas volcánicas."),
    OrigenDeGeneracion("Inducido", "Causado por actividades humanas como minería o fracking.")
]

alcances_mock = [
    AlcanceSismo("Local", "Percibido en un área geográfica limitada, cerca del epicentro."),
    AlcanceSismo("Regional", "Percibido en una región más amplia, incluyendo varias ciudades o provincias."),
    AlcanceSismo("Lejano", "Percibido a grandes distancias, incluso cientos de kilómetros del epicentro.")
]

# Lista de estados
estados_mock = [
    Estado(ambito="EventoSismico", nombreEstado="AutoDetectado"),
    Estado(ambito="EventoSismico", nombreEstado="PendienteDeRevision"),
    Estado(ambito="EventoSismico", nombreEstado="BloqueadoEnRevision")
]

cambios_estado_mock = [
    CambioEstado(datetime.now, estados_mock[0]),
    CambioEstado(datetime.now,estados_mock[1])
]

# Muestra mínima de una serie temporal
series_mock =[
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 5, 14, 10, 1),
        frecuenciaMuestreo=49,
        muestraSismica=[]  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=[]  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 4, 14, 10, 1),
        frecuenciaMuestreo=30,
        muestraSismica=[]  # Podés simular con mocks también
    ),
] 

#Lista de eventos sismicos
eventos_mock = [EventoSismico(
    clasificacion=clasificacion_mock[0],
    magnitud=magnitud,
    origenGeneracion=origen_mock[1],
    alcanceSismo=alcances_mock[1],
    estadoActual=estados_mock[1],
    cambioEstado=cambios_estado_mock[1],
    serieTemporal=series_mock,
    fechaHoraOcurrencia=datetime(2025, 5, 20, 13, 0),
    latitudEpicentro=-31.4167,
    latitudHipocentro=-31.4175,
    longitudEpicentro=-64.1833,
    longitudHipocentro=-64.1840,
    valorMagnitud=3.9
), EventoSismico(
    clasificacion=clasificacion_mock[1],
    magnitud=magnitud,
    origenGeneracion=origen_mock[0],
    alcanceSismo=alcances_mock[0],
    estadoActual=estados_mock[0],
    cambioEstado=cambios_estado_mock[0],
    serieTemporal=series_mock,
    fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
    latitudEpicentro=-31.4167,
    latitudHipocentro=-35.6175,
    longitudEpicentro=-64.1833,
    longitudHipocentro=-64.1840,
    valorMagnitud=3.7)]

sismografos_mock = [
    Sismografo(datetime(2025, 5, 14, 10, 0), "SISMO-001", "SN12345"),
    Sismografo(datetime(2024, 11, 2, 9, 30), "SISMO-002", "SN12346"),
    Sismografo(datetime(2023, 8, 20, 14, 15), "SISMO-003", "SN12347"),
    Sismografo(datetime(2022, 3, 5, 8, 45), "SISMO-004", "SN12348"),
    Sismografo(datetime(2021, 12, 1, 16, 0), "SISMO-005", "SN12349")
]

estaciones_mock = [
    EstacionSismologica("ST001", None, None, 0.0, 0.0, "Estación Central - Córdoba", None),
    EstacionSismologica("ST002", None, None, 0.0, 0.0, "Estación Norte - Salta", None),
    EstacionSismologica("ST003", None, None, 0.0, 0.0, "Estación Sur - Neuquén", None),
    EstacionSismologica("ST004", None, None, 0.0, 0.0, "Estación Andina - Mendoza", None),
    EstacionSismologica("ST005", None, None, 0.0, 0.0, "Estación Costera - Mar del Plata", None)
]
