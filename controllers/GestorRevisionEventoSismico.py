from datetime import datetime
from entities.EventoSismico import EventoSismico
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
from entities.Sesion import Sesion
#from interface.PantallaRevisionEventoSismico import PantallaRevisionEventoSismico
from data import eventos_mock, estados_mock, sismografos_mock, usuario_mock
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
        self.estadoRechazado: Estado = None 
        self.cambioEstadoActual: CambioEstado = None
        self.nombreAlcance = None
        self.nombreOrigen = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.accionSeleccionada = None 
        self.sesionActiva = Sesion(datetime.now(), usuario_mock)
        self.usuarioActivo = None


    #Métodos get y set si corresponden
    def getEventosSismicosAutoDetectados(self):
        return self.eventosSismicosAutoDetectados

    # Lógica del CU
    def opcRegistrarResultadoRevisionManual(self):
        self.obtenerUsuarioLogueado()
        return self.buscarEventosAutoDetectados()

    def calcularFechaHoraActual(self):
    # Método para calcular fecha y hora en el momento    
        return datetime.now()
    
    # Buscar eventos autodetectados o pendientes de revision para mostrar al inicio
    def buscarEventosAutoDetectados(self):
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

        # Arma diccionario para clasificar por estacion todos los datos de los detalles muestra de cada muestra de cada serie
        self.buscarDatosSeriesPorEstacion()

        # Envia esos datos a la pantalla para mostrar
        self.pantallaRevision.mostrarDatosEventosSismicos(self.nombreAlcance, self.nombreOrigen,self.nombreClasificacion, self.datosEventoPorEstacion)
        print("Datos enviados a la pantalla")
            
    def bloquearEventoSismico(self):
        # Buscar por estado y ambito el estado BloqueadoEnRevision
        for estado in estados_mock:
            if (estado.esAmbitoEventoSismico()) and (estado.esBloqueadoEnRevision()):
                self.estadoBloqueadoEnRevision = estado
                break
        # Buscar el cambio de estado actual
        self.cambioEstadoActual = self.eventoSismicoSeleccionado.obtenerEstadoActual()

        #Calcular fecha y hora actual
        self.horaFechaFinCambioEstado = self.calcularFechaHoraActual()

        #Realizar el cambio de estado
        print("Estado antes del cambio: ", self.eventoSismicoSeleccionado.estadoActual.getNombreEstado())
        self.eventoSismicoSeleccionado.setEstadoActual(self.estadoBloqueadoEnRevision)
        print("Lista de cambios de estados previos: ")
        for cambioEstado in self.eventoSismicoSeleccionado.cambioEstado:
            print("Cambio de estado:", cambioEstado.getEstado().getNombreEstado())
        print("-----")  
        print("Estado luego del cambio: ", self.eventoSismicoSeleccionado.estadoActual.getNombreEstado())
        self.eventoSismicoSeleccionado.bloquearEnRevision(self.estadoBloqueadoEnRevision, 
                                                          self.cambioEstadoActual, 
                                                          self.horaFechaFinCambioEstado, self.usuarioActivo)
        for cambioEstado in self.eventoSismicoSeleccionado.cambioEstado:
            print("Cambio de estado:", cambioEstado.getEstado().getNombreEstado())
            print("Empleado responsable: ", cambioEstado.getResponsableInspeccion().getNombre())
            print("Fecha y hora de cambio de estado: ", cambioEstado.getFechaHoraFin())
        print("-----")   
    
    def buscarDatosEventoSismico(self):
        self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion = self.eventoSismicoSeleccionado.obtenerDatosEvento()


    def buscarDatosSeriesPorEstacion(self):
        # Se crea un diccionario que arma una lista por clave
        self.datosEventoPorEstacion = defaultdict(list)
        for serie in self.eventoSismicoSeleccionado.getSerieTemporal():
            nombreEstacion = serie.obtenerNombreEstacion(sismografos_mock) # Los pasamos por parametros a todos los sismografos porque saltaba error importacion circular
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
        # Mostramos por consola los datos de cada serie temporal
        """print("\nDatos por Estación Sismográfica:\n" + "="*40)
        for nombre_estacion, muestras in self.datosEventoPorEstacion.items():
            print(f"\nEstación: {nombre_estacion}\n" + "-"*40)
            for i, muestra in enumerate(muestras, start=1):
                print(f"Muestra #{i}:")
                print(f"\tFecha y Hora: {muestra['fechaHoraMuestra']}")
                print(f"\tFrecuencia de Onda: {muestra['frecuenciaOnda']} Hz")
                print(f"\tLongitud de Onda:   {muestra['longitudOnda']} m")
                print(f"\tVelocidad de Onda:  {muestra['velocidadOnda']} m/s")
            print("-"*40) """

    def llamarCU18():
        print("ESTO ES UN SISMOGRAMA")

    def opRechazarEvento(self):
        print(self.eventoSismicoSeleccionado.getMagnitud())
        self.accionSeleccionada = "Rechazar evento"
        if(self.validarAccionSeleccionada(self.accionSeleccionada)):
            if(self.eventoSismicoSeleccionado.validarDatos()):
                print("Datos válidos")
                self.rechazarEventoSismico()
            else:
                print("Datos inválidos")

    def validarAccionSeleccionada(self, opcion):
        if (opcion in ["Rechazar evento", "Confirmar evento", "Solicitar Revision a experto"]):
            return True

    def obtenerUsuarioLogueado(self):
        self.usuarioActivo = self.sesionActiva.getUsuarioActivo().getEmpleado()

    def rechazarEventoSismico(self):
        # Buscar por estado y ambito el estado BloqueadoEnRevision
        for estado in estados_mock:
            if (estado.esAmbitoEventoSismico()) and (estado.esRechazado()):
                self.estadoRechazado = estado
                break
        # Buscar el cambio de estado actual
        self.cambioEstadoActual = self.eventoSismicoSeleccionado.obtenerEstadoActual()

        #Calcular fecha y hora actual
        self.horaFechaFinCambioEstado = self.calcularFechaHoraActual()

        #Realizar el cambio de estado
        print("ESTE ES DEL RECHAZADO")
        print("Estado antes del cambio: ", self.eventoSismicoSeleccionado.estadoActual.getNombreEstado())
        self.eventoSismicoSeleccionado.setEstadoActual(self.estadoRechazado)
        for cambioEstado in self.eventoSismicoSeleccionado.cambioEstado:
            print("Cambio de estado:", cambioEstado.getEstado().getNombreEstado())
            print("Empleado responsable: ", cambioEstado.getResponsableInspeccion().getNombre())
        print("-----")  
        print("Estado luego del cambio: ", self.eventoSismicoSeleccionado.estadoActual.getNombreEstado())
        self.eventoSismicoSeleccionado.rechazar(self.estadoRechazado, 
                                                          self.cambioEstadoActual, 
                                                          self.horaFechaFinCambioEstado, self.usuarioActivo)
