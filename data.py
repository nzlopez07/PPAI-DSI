from datetime import datetime
#from collections import defaultdict

from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from entities.AlcanceSismo import AlcanceSismo
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
from entities.SerieTemporal import SerieTemporal
from entities.EventoSismico import EventoSismico
from entities.Sismografo import Sismografo
from entities.EstacionSismologica import EstacionSismologica
from entities.DetalleMuestraSismica import DetalleMuestraSismica
from entities.MuestraSismica import MuestraSismica
from entities.DetalleMuestraSismica import TipoDeDato
from entities.Empleado import Empleado
from entities.Usuario import Usuario

# Mocks simples para objetos referenciales
empleado_mock = Empleado("Gomez", "asd123@gmail.com", "Juan", "123456789")

usuario_mock = Usuario("pwdSegura123", "JuanGomezUSER", empleado_mock)
# Crear detalles individuales

mock_tipo_dato =[
    TipoDeDato(denominacion="Longitud de onda", nombreUnidadMedida="km/ciclo", valorUmbral=1 ),
    TipoDeDato(denominacion="Frecuencia de onda", nombreUnidadMedida="Hz", valorUmbral=15 ),
    TipoDeDato(denominacion="Velocidad de onda", nombreUnidadMedida="km/seg", valorUmbral=10 )
]

detalle_muestras_mock_0 = [
    DetalleMuestraSismica(valor=7, tipoDato=mock_tipo_dato[2]),
    DetalleMuestraSismica(valor=0.7, tipoDato=mock_tipo_dato[0]),
    DetalleMuestraSismica(valor=10, tipoDato=mock_tipo_dato[1])
]
detalle_muestras_mock_1 = [
    DetalleMuestraSismica(valor=7.02, tipoDato=mock_tipo_dato[2]),
    DetalleMuestraSismica(valor=0.69, tipoDato=mock_tipo_dato[0]),
    DetalleMuestraSismica(valor=10.01, tipoDato=mock_tipo_dato[1])
]

muestras_mock_0 = [
MuestraSismica(
    fechaHoraMuestra=datetime(2025, 5, 19, 10, 15),
    detalleMuestraSismica=detalle_muestras_mock_0
),
MuestraSismica(
    fechaHoraMuestra=datetime(2025, 5, 19, 10, 30),
    detalleMuestraSismica=detalle_muestras_mock_1
)
]

muestras_mock_1 = [
MuestraSismica(
    fechaHoraMuestra=datetime(2025, 6, 19, 11, 30),
    detalleMuestraSismica=detalle_muestras_mock_0
),
MuestraSismica(
    fechaHoraMuestra=datetime(2025, 6, 19, 11, 45),
    detalleMuestraSismica=detalle_muestras_mock_1
)
]


clasificacion_mock = [
    ClasificacionSismo(0, 70, "Superficial"),
    ClasificacionSismo(71, 300, "Intermedio"),
    ClasificacionSismo(301, 700, "Profundo")
]

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

estados_mock = [
    Estado(ambito="EventoSismico", nombreEstado="AutoDetectado"), #0
    Estado(ambito="EventoSismico", nombreEstado="PendienteDeRevision"), #1
    Estado(ambito="EventoSismico", nombreEstado="BloqueadoEnRevision"), #2
    Estado(ambito="EventoSismico", nombreEstado="Rechazado"),
    Estado(ambito="EventoSismico", nombreEstado="Confirmado"),
    Estado(ambito="EventoSismico", nombreEstado="SolicitadoRevisionExperto")
]


cambios_estado_mock_Rechazado = [
    CambioEstado(fechaHoraInicio=(datetime.now()), estado=estados_mock[0], fechaHoraFin=datetime.now(), responsable=usuario_mock.getEmpleado()),
    CambioEstado(fechaHoraInicio=datetime.now(),estado=estados_mock[1], fechaHoraFin=datetime.now(), responsable=usuario_mock.getEmpleado()),
    CambioEstado(fechaHoraInicio=datetime.now(),estado=estados_mock[3], responsable=usuario_mock.getEmpleado()),
]
cambios_estado_mock_PteRev = [
    CambioEstado(fechaHoraInicio=datetime.now(), estado=estados_mock[0], fechaHoraFin=datetime.now(), responsable=usuario_mock.getEmpleado()),
    CambioEstado(fechaHoraInicio=datetime.now(),estado=estados_mock[1], responsable=usuario_mock.getEmpleado()),
]
cambios_estado_mock_AutoDet = [
    CambioEstado(fechaHoraInicio=datetime.now(), estado=estados_mock[0], responsable=usuario_mock.getEmpleado()),
]

series_mock = [
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
]

series_mock_2 = [
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
]

series_mock_3 = [
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_0  # Podés simular con mocks también
    ),
    SerieTemporal(
        condicionAlarma=False,
        fechaHoraInicioRegistroMuestras=datetime(2025, 5, 14, 10, 0),
        fechaHoraRegistro=datetime(2025, 6, 14, 10, 1),
        frecuenciaMuestreo=50,
        muestraSismica=muestras_mock_1  # Podés simular con mocks también
    ),
]

eventos_mock = [
    EventoSismico(
        clasificacion=clasificacion_mock[1],
        magnitud=None,
        origenGeneracion=origen_mock[1],
        alcanceSismo=alcances_mock[1],
        estadoActual=estados_mock[1],
        cambiosEstado=cambios_estado_mock_PteRev,
        serieTemporal=series_mock + series_mock_2,
        fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
        latitudEpicentro=-31.4167,
        latitudHipocentro=-35.6175,
        longitudEpicentro=-64.1833,
        longitudHipocentro=-64.1840,
        valorMagnitud=2
    ), 
    EventoSismico(
        clasificacion=clasificacion_mock[2],
        magnitud=None,
        origenGeneracion=origen_mock[2],
        alcanceSismo=alcances_mock[2],
        estadoActual=estados_mock[0],
        cambiosEstado=cambios_estado_mock_AutoDet,
        serieTemporal=series_mock,
        fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
        latitudEpicentro=-31.4167,
        latitudHipocentro=-35.6175,
        longitudEpicentro=-64.1833,
        longitudHipocentro=-64.1840,
        valorMagnitud=3
    ),
    EventoSismico(
        clasificacion=clasificacion_mock[1],
        magnitud=None,
        origenGeneracion=origen_mock[1],
        alcanceSismo=alcances_mock[1],
        estadoActual=estados_mock[1],
        cambiosEstado=cambios_estado_mock_PteRev,
        serieTemporal=series_mock + series_mock_2,
        fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
        latitudEpicentro=-31.4167,
        latitudHipocentro=-35.6175,
        longitudEpicentro=-64.1833,
        longitudHipocentro=-64.1840,
        valorMagnitud=5
    ), 
    EventoSismico(
        clasificacion=clasificacion_mock[2],
        magnitud=None,
        origenGeneracion=origen_mock[2],
        alcanceSismo=alcances_mock[2],
        estadoActual=estados_mock[0],
        cambiosEstado=cambios_estado_mock_AutoDet,
        serieTemporal=series_mock,
        fechaHoraOcurrencia=datetime(2025, 5, 14, 10, 0),
        latitudEpicentro=-31.4167,
        latitudHipocentro=-35.6175,
        longitudEpicentro=-64.1833,
        longitudHipocentro=-64.1840,
        valorMagnitud=6
    )
]

#estaciones_mock = [
    #EstacionSismologica("ST001", None, None, 0.0, 0.0, "Estación Central - Córdoba", None),
    #EstacionSismologica("ST002", None, None, 0.0, 0.0, "Estación Norte - Salta", None),
    #EstacionSismologica("ST003", None, None, 0.0, 0.0, "Estación Sur - Neuquén", None),
    #EstacionSismologica("ST004", None, None, 0.0, 0.0, "Estación Andina - Mendoza", None),
    #EstacionSismologica("ST005", None, None, 0.0, 0.0, "Estación Costera - Mar del Plata", None)
#]

#sismografos_mock = [
    #Sismografo(datetime(2025, 5, 14, 10, 0), "SISMO-001", "SN12345", estacionSismologica=estaciones_mock[0], seriesTemporales=series_mock),
    #Sismografo(datetime(2024, 11, 2, 9, 30), "SISMO-002", "SN12346", estacionSismologica=estaciones_mock[1], seriesTemporales=series_mock),
    #Sismografo(datetime(2023, 8, 20, 14, 15), "SISMO-003", "SN12347"),
    #Sismografo(datetime(2022, 3, 5, 8, 45), "SISMO-004", "SN12348"),
    #Sismografo(datetime(2021, 12, 1, 16, 0), "SISMO-005", "SN12349")
#]

# ...existing code...

# Mock de varias estaciones y sismógrafos para pruebas en detalle_evento.html
estaciones_mock = [
    EstacionSismologica("ST001", None, None, -31.4167, -64.1833, "Estación Central - Córdoba", None),
    EstacionSismologica("ST002", None, None, -24.7821, -65.4232, "Estación Norte - Salta", None),
    EstacionSismologica("ST003", None, None, -38.9516, -68.0591, "Estación Sur - Neuquén", None),
    EstacionSismologica("ST004", None, None, -32.8908, -68.8272, "Estación Andina - Mendoza", None),
    EstacionSismologica("ST005", None, None, -38.0055, -57.5426, "Estación Costera - Mar del Plata", None)
]

sismografos_mock = [
    Sismografo(datetime(2025, 5, 14, 10, 0), "SISMO-001", "SN12345", estacionSismologica=estaciones_mock[0], seriesTemporales=series_mock_3),
    Sismografo(datetime(2025, 5, 15, 11, 30), "SISMO-002", "SN12346", estacionSismologica=estaciones_mock[1], seriesTemporales=series_mock),
    Sismografo(datetime(2025, 5, 16, 9, 45), "SISMO-003", "SN12347", estacionSismologica=estaciones_mock[2], seriesTemporales=series_mock_2),
    Sismografo(datetime(2025, 5, 17, 14, 20), "SISMO-004", "SN12348", estacionSismologica=estaciones_mock[3], seriesTemporales=series_mock),
    Sismografo(datetime(2025, 5, 18, 16, 10), "SISMO-005", "SN12349", estacionSismologica=estaciones_mock[4], seriesTemporales=series_mock_2)
]