from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico

class PantallaRevisionEventoSismico:
    def __init__(self):
        self.gestorRevision:GestorRevisionEventoSismico = None
        self.eventosAutoDetectadosYPendientesDeRevision = None
        self.eventoSeleccionado = None
        self.nombreOrigen = None
        self.nombreAlcance = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.accionSeleccionada = None
        self.seleccionMapa = False
        self.seleccionModificar = False

    def opcRegistrarResultadoRevisionManual(self):
        self.habilitarPantalla()
        return self.eventosAutoDetectadosYPendientesDeRevision

    def habilitarPantalla(self):
        self.gestorRevision = GestorRevisionEventoSismico(self)
        self.gestorRevision.opcRegistrarResultadoRevisionManual()
    
    def mostrarYSolicitarSeleccionEvento(self, eventos):
        self.eventosAutoDetectadosYPendientesDeRevision = eventos

    def tomarSeleccionEvento(self, indice):
        # Asigna el evento sismico selecionado a la pantalla
        self.eventoSeleccionado = self.eventosAutoDetectadosYPendientesDeRevision[indice]
        
        self.gestorRevision.tomarSeleccionEvento(self.eventoSeleccionado)

        return self.mostrarDatosEventosSismicos(self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion)


    def mostrarDatosEventosSismicos(self, nombreAlcance, nombreOrigen, nombreClasificacion, datosEventoPorEstacion):
        self.nombreOrigen = nombreOrigen
        self.nombreAlcance = nombreAlcance
        self.nombreClasificacion = nombreClasificacion
        self.datosEventoPorEstacion = datosEventoPorEstacion

        return self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion

    def opRechazarEvento(self):
        self.accionSeleccionada = "Rechazar evento"
        self.gestorRevision.opRechazarEvento(self.accionSeleccionada)
    
    def cancelarRevisionEvento(self):
        self.gestorRevision.cancelarRevisionEventoSismico()

    def opConfirmarEvento(self):
        self.accionSeleccionada = "Confirmar evento"
        self.gestorRevision.opConfirmarEvento(self.accionSeleccionada)

    def opSolicitarRevisionExperto(self):
        self.accionSeleccionada = "Solicitar Revision a experto"
        self.gestorRevision.opSolicitarRevisionExperto(self.accionSeleccionada)

    def mostrarOpcionVisualizarMapa(self):
        print("GENERADOS BOTONES DE VISUALIZACION DE MAPA")
    
    def tomarSeleccionMapa(self, seleccionMapa):
        self.seleccionMapa = seleccionMapa

    def tomarSeleccionModificar(self, seleccionModificar):
        self.seleccionModificar = seleccionModificar


    def finCU(self):
        print("Fin de caso de uso PANTALLA")
        self.eventosAutoDetectadosYPendientesDeRevision = None
        self.eventoSeleccionado = None
        self.nombreOrigen = None
        self.nombreAlcance = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.accionSeleccionada = None
        self.seleccionMapa = False
        self.seleccionModificar = False
