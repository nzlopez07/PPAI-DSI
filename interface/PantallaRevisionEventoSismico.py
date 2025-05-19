from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico

class PantallaRevisionEventoSismico:
    def __init__(self):
        self.gestorRevision:GestorRevisionEventoSismico = GestorRevisionEventoSismico(self)
        self.eventosAutoDetectadosYPendientesDeRevision = None
        self.eventoSeleccionado = None
        self.nombreOrigen = None
        self.nombreAlcance = None
        self.nombreClasificacion = None
        
    def opcRegistrarResultadoRevisionManual(self):
        self.habilitarPantalla()
        return self.eventosAutoDetectadosYPendientesDeRevision

    def habilitarPantalla(self):
        self.gestorRevision.opcRegistrarResultadoRevisionManual()
    
    def mostrarYSolicitarSeleccionEvento(self, eventos):
        #self.tomarSeleccionEvento()
        self.eventosAutoDetectadosYPendientesDeRevision = eventos

    def tomarSeleccionEvento(self):
        self.gestorRevision.tomarSeleccionEvento()
        return self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion

    def mostrarDatosEventosSismicos(self, nombreAlcance, nombreOrigen, nombreClasificacion):
        self.nombreOrigen = nombreOrigen
        self.nombreAlcance = nombreAlcance
        self.nombreClasificacion = nombreClasificacion
        
    
