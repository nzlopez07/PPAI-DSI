from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico

class PantallaRevisionEventoSismico:
    def __init__(self):
        self.gestorRevision:GestorRevisionEventoSismico = GestorRevisionEventoSismico(self)
        self.eventosAutoDetectadosYPendientesDeRevision = None
        self.eventoSeleccionado = None
        self.nombreOrigen = None
        self.nombreAlcance = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        
    def opcRegistrarResultadoRevisionManual(self):
        self.habilitarPantalla()
        return self.eventosAutoDetectadosYPendientesDeRevision

    def habilitarPantalla(self):
        self.gestorRevision.opcRegistrarResultadoRevisionManual()
    
    def mostrarYSolicitarSeleccionEvento(self, eventos):
        #self.tomarSeleccionEvento()
        self.eventosAutoDetectadosYPendientesDeRevision = eventos

    def tomarSeleccionEvento(self, indice):
        # Asigna el evento sismico selecionado a la pantalla
        self.eventoSeleccionado = self.eventosAutoDetectadosYPendientesDeRevision[indice]
        
        self.gestorRevision.tomarSeleccionEvento(self.eventoSeleccionado)
        return self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion

    def mostrarDatosEventosSismicos(self, nombreAlcance, nombreOrigen, nombreClasificacion, datosEventoPorEstacion):
        print("ENTRÉ AL MÉTODO MOSTRAR DATOS EVENTOS SISMICOS DE PANTALLA")
        self.nombreOrigen = nombreOrigen
        self.nombreAlcance = nombreAlcance
        self.nombreClasificacion = nombreClasificacion
        self.datosEventoPorEstacion = datosEventoPorEstacion
        ##Este método tengo entendido que no instancia la carga en la pantalla,
        ##Se hace una asignación de valores que desconozco el por qué.

    def opRechazarEvento(self):
        self.gestorRevision.opRechazarEvento()
    
