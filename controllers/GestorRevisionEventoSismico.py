from datetime import datetime
from entities.EventoSismico import EventoSismico
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
#from interface.PantallaRevisionEventoSismico import PantallaRevisionEventoSismico
from data import eventos_mock, estados_mock, sismografos_mock
from collections import defaultdict

#lista_estados_mock = [Estado(**data) for data in estados_mock]
#lista_eventos_mock = [EventoSismico(**data) for data in eventos_mock]

class GestorRevisionEventoSismico:
    def __init__(self, pantalla):
        self.pantallaRevision = pantalla
        self.horaFechaFinCambioEstado = None
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"
        self.eventoSismicoSeleccionado: EventoSismico = None
        self.estadoBloqueadoEnRevision: Estado = None
        self.cambioEstadoActual: CambioEstado = None
        self.fechaHoraActualBloqueadoEnRevision = None
        self.nombreAlcance = None
        self.nombreOrigen = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None

    #Métodos get y set si corresponden
    def getEventosSismicosAutoDetectados(self):
        return self.eventosSismicosAutoDetectados

    # Lógica del CU
    def opcRegistrarResultadoRevisionManual(self):
        return self.buscarEventosAutoDetectados()

    def calcularFechaHoraActual(self):
    # Método para calcular fecha y hora en el momento    
        return datetime.now()
    
    # Buscar eventos autodetectados o pendientes de revision para mostrar al inicio
    def buscarEventosAutoDetectados(self):
        print("------Entramos al método buscarEventosAutoDetectados de Gestor correctamente\n")
        # Recorre la colección de todos los eventos sísmicos y valida que tengan el estado "AutoDetectado"
        self.eventosSismicosAutoDetectados = []
        # Busca por estado actual, no por el cambio de estado
        for evento in eventos_mock:
            if (evento.estaAutoDetectado()) or (evento.estaPendienteDeRevision()):
                self.eventosSismicosAutoDetectados.append(evento)
        
        #Ordena los eventos sismicos a mostrar
        self.ordenarPorFechaYHora(self.eventosSismicosAutoDetectados)
        # Los manda
        self.pantallaRevision.mostrarYSolicitarSeleccionEvento(self.eventosSismicosAutoDetectados)
        #return self.eventosSismicosAutoDetectados

    def ordenarPorFechaYHora(self, eventosSismicos:list[EventoSismico]):
        n = len(eventosSismicos)
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if (eventosSismicos[i].getFechaHoraOcurrencia()) > (eventosSismicos[j].getFechaHoraOcurrencia()):
                    eventosSismicos[i], eventosSismicos[j] = eventosSismicos[j], eventosSismicos[i]
    
    # Seleccionar un evento
    def tomarSeleccionEvento(self, evento):
        # Asigna el evento sismico seleccionado al gestor
        self.eventoSismicoSeleccionado = evento

        # Cambio de estado del evento sismico
        self.bloquearEventoSismico()

        # Busca nombre de origen, alcance y clasifiacion
        self.buscarDatosEventoSismico()

        # Envia esos datos a la pantalla para mostrar
        self.pantallaRevision.mostrarDatosEventosSismicos(self.nombreAlcance, self.nombreOrigen,self.nombreClasificacion)

        # Arma diccionario para clasificar por estacion todos los datos de los detalles muestra de cada muestra de cada serie
        self.buscarDatosSeriesPorEstacion()
            
    def bloquearEventoSismico(self):
        # Buscar por estado y ambito el estado BloqueadoEnRevision
        for estado in estados_mock:
            if (estado.esAmbitoEventoSismico) and (estado.esBloqueadoEnRevision):
                self.estadoBloqueadoEnRevision = estado
                break
        # Buscar el cambio de estado actual
        self.cambioEstadoActual = self.eventoSismicoSeleccionado.obtenerEstadoActual()

        #Calcular fecha y hora actual
        self.horaFechaFinCambioEstado = self.calcularFechaHoraActual()

        #Realizar el cambio de estado
        self.eventoSismicoSeleccionado.setEstadoActual(self.estadoBloqueadoEnRevision)
        self.eventoSismicoSeleccionado.bloquearEnRevision(self.estadoBloqueadoEnRevision, self.cambioEstadoActual, self.fechaHoraActualBloqueadoEnRevision)
        print("Estado actual es: ", self.eventoSismicoSeleccionado.estadoActual.getNombreEstado())
    
    
    def buscarDatosEventoSismico(self):
        self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion = self.eventoSismicoSeleccionado.obtenerDatosEvento()


    def buscarDatosSeriesPorEstacion(self):
        # Se crea un diccionario que arma una lista por clave
        self.datosEventoPorEstacion = defaultdict(list)
        for serie in self.eventoSismicoSeleccionado.getSerieTemporal():
            nombreEstacion = serie.obtenerNombreEstacion(sismografos_mock)
            for muestra in serie.getMuestraSismica():
                fechaHoraMuestra = muestra.getFechaHoraMuestra()
                for detalle in muestra.getDetalleMuestraSismica():
                    frecuencia = detalle.getFrecuenciaOnda()
                    longitud = detalle.getLongitudOnda()
                    velocidad = detalle.getVelocidadOnda()

                    # Guardar valores
                    self.datosEventoPorEstacion[nombreEstacion].append({
                        "fechaHoraMuestra": fechaHoraMuestra,
                        "frecuenciaOnda": frecuencia,
                        "longitudOnda":longitud,
                        "velocidadOnda":velocidad
                    })

        print("\nDatos por Estación Sismográfica:\n" + "="*40)
        for nombre_estacion, muestras in self.datosEventoPorEstacion.items():
            print(f"\nEstación: {nombre_estacion}\n" + "-"*40)
            for i, muestra in enumerate(muestras, start=1):
                print(f"Muestra #{i}:")
                print(f"\tFecha y Hora: {muestra['fechaHoraMuestra']}")
                print(f"\tFrecuencia de Onda: {muestra['frecuenciaOnda']} Hz")
                print(f"\tLongitud de Onda:   {muestra['longitudOnda']} m")
                print(f"\tVelocidad de Onda:  {muestra['velocidadOnda']} m/s")
            print("-"*40)

    def llamarCU18():
        pass
