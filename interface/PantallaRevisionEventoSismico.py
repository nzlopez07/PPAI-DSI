from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico
from sqlalchemy.orm import Session

class PantallaRevisionEventoSismico:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.gestorRevision: GestorRevisionEventoSismico = None
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
        """
        Mensaje 1 del diagrama de secuencia: opcRegistrarResultadoRevisionManual()
        """
        self.habilitarPantalla()
        return self.eventosAutoDetectadosYPendientesDeRevision

    def habilitarPantalla(self):
        """
        Mensaje 2 del diagrama de secuencia: habilitarPantalla()
        """
        self.gestorRevision = GestorRevisionEventoSismico(self, self.db_session)
        self.gestorRevision.opcRegistrarResultadoRevisionManual()
    
    def mostrarYSolicitarSeleccionEvento(self, eventos):
        """
        Mensaje 3 del diagrama de secuencia: mostrarYSolicitarSeleccionEvento(eventos)
        """
        self.eventosAutoDetectadosYPendientesDeRevision = eventos

    def tomarSeleccionEvento(self, indice):
        """
        Mensaje 4 del diagrama de secuencia: tomarSeleccionEvento(indice)
        """
        self.eventoSeleccionado = self.eventosAutoDetectadosYPendientesDeRevision[indice]
        self.gestorRevision.tomarSeleccionEvento(self.eventoSeleccionado)
        return self.mostrarDatosEventosSismicos(self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion)


    def mostrarDatosEventosSismicos(self, nombreAlcance, nombreOrigen, nombreClasificacion, datosEventoPorEstacion):
        """
        Mensaje 5 del diagrama de secuencia: mostrarDatosEventosSismicos(...)
        """
        self.nombreOrigen = nombreOrigen
        self.nombreAlcance = nombreAlcance
        self.nombreClasificacion = nombreClasificacion
        self.datosEventoPorEstacion = datosEventoPorEstacion
        print(f"LOG: Mostrando datos del evento en pantalla: Origen={nombreOrigen}, Alcance={nombreAlcance}, Clasificación={nombreClasificacion}")
        return self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion

    def opRechazarEvento(self):
        """
        Mensaje 6 del diagrama de secuencia: opRechazarEvento()
        """
        self.accionSeleccionada = "Rechazar evento"
        self.gestorRevision.opRechazarEvento(self.accionSeleccionada)
    
    def cancelarRevisionEvento(self):
        """
        Mensaje 20 del diagrama de secuencia: cancelarRevisionEvento()
        """
        self.gestorRevision.cancelarRevisionEventoSismico()

    def opConfirmarEvento(self):
        """
        Mensaje 14 del diagrama de secuencia: opConfirmarEvento()
        """
        self.accionSeleccionada = "Confirmar evento"
        self.gestorRevision.opConfirmarEvento(self.accionSeleccionada)

    def opSolicitarRevisionExperto(self):
        """
        Mensaje 15 del diagrama de secuencia: opSolicitarRevisionExperto()
        """
        self.accionSeleccionada = "Solicitar Revision a experto"
        self.gestorRevision.opSolicitarRevisionExperto(self.accionSeleccionada)

    
    def tomarSeleccionMapa(self, seleccionMapa):
        self.seleccionMapa = seleccionMapa

    def tomarSeleccionModificar(self, seleccionModificar):
        self.seleccionModificar = seleccionModificar


    def finCU(self):
        """
        Mensaje 22 del diagrama de secuencia: finCU()
        """
        print("LOG: Fin de caso de uso PANTALLA")
        self.eventosAutoDetectadosYPendientesDeRevision = None
        self.eventoSeleccionado = None
        self.nombreOrigen = None
        self.nombreAlcance = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.accionSeleccionada = None
        self.seleccionMapa = False
        self.seleccionModificar = False
