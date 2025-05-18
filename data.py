from entities.EventoSismico import EventoSismico
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
from entities.AlcanceSismo import AlcanceSismo
from entities.SerieTemporal import SerieTemporal
from datetime import datetime

# Mocks simples para objetos referenciales
clasificacion = None  # Reemplazar por un mock si es necesario
magnitud = None       # Reemplazar por un mock si es necesario
origen = None         # Reemplazar por un mock si es necesario
alcance = AlcanceSismo("ASD", "Alcance")  # Completar según implementación

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
serie = SerieTemporal(
    condicionAlarma=False,
    fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
    fechaHoraRegistro=datetime(2025, 5, 14, 10, 1),
    frecuenciaMuestreo=50,
    muestraSismica=[]  # Podés simular con mocks también
)

#Lista de eventos sismicos
eventos_mock = [EventoSismico(
    clasificacion=clasificacion,
    magnitud=magnitud,
    origenGeneracion=origen,
    alcanceSismo=alcance,
    estadoActual=estados_mock[1],
    cambioEstado=cambios_estado_mock[1],
    serieTemporal=[serie],
    fechaHoraOcurrencia=datetime(2025, 5, 20, 13, 0),
    latitudEpicentro=-31.4167,
    latitudHipocentro=-31.4175,
    longitudEpicentro=-64.1833,
    longitudHipocentro=-64.1840,
    valorMagnitud=3.9
), EventoSismico(
    clasificacion=clasificacion,
    magnitud=magnitud,
    origenGeneracion=origen,
    alcanceSismo=alcance,
    estadoActual=estados_mock[0],
    cambioEstado=cambios_estado_mock[0],
    serieTemporal=[serie],
    fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
    latitudEpicentro=-31.4167,
    latitudHipocentro=-35.6175,
    longitudEpicentro=-64.1833,
    longitudHipocentro=-64.1840,
    valorMagnitud=3.7)]
