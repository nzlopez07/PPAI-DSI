from datetime import datetime
from entities.EventoSismico import EventoSismico
from entities.Estado import Estado
from entities.CambioEstado import CambioEstado
from data import eventos_mock, estados_mock

class GestorRevisionEventoSismico:
    def __init__(self):
        self.horaFechaFinCambioEstado = None
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"
        self.eventoSismicoSeleccionado: EventoSismico = None
        self.estadoBloqueadoEnRevision: Estado = None
        self.cambioEstadoActual: CambioEstado = None
        self.fechaHoraActualBloqueadoEnRevision = None

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
        print("Entramos al método buscarEventosAutoDetectados de Gestor correctamente")
        # Recorre la colección de todos los eventos sísmicos y valida que tengan el estado "AutoDetectado"
        self.eventosSismicosAutoDetectados = []
        for evento in eventos_mock:
            if (evento.estaAutoDetectado()) or (evento.estaPendienteDeRevision()):
                self.eventosSismicosAutoDetectados.append(evento)
        self.ordenarPorFechaYHora(self.eventosSismicosAutoDetectados)
        return self.eventosSismicosAutoDetectados

    def ordenarPorFechaYHora(self, eventosSismicos:list[EventoSismico]):
        n = len(eventosSismicos)
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if (eventosSismicos[i].getFechaHoraOcurrencia()) > (eventosSismicos[j].getFechaHoraOcurrencia()):
                    eventosSismicos[i], eventosSismicos[j] = eventosSismicos[j], eventosSismicos[i]
    
    # Seleccionar un evento
    def tomarSeleccionEvento(self):
        pass
            
    def bloquearEventoSismico(self):
        # Buscar por estado y ambito el estado BloqueadoEnRevision
        for estado in estados_mock:
            if (estado.esAmbitoEventoSismico) and (estado.esBloqueadoEnRevision):
                self.estadoBloqueadoEnRevision = estado
                break
        # Buscar el cambio de estado actual
        self.cambioEstadoActual = self.eventoSismicoSeleccionado.esEstadoActual()

        #Calcular fecha y hora actual
        self.horaFechaFinCambioEstado = self.calcularFechaHoraActual()

        #Realizar el cambio de estado
        self.eventoSismicoSeleccionado.setEstadoActual(self.estadoBloqueadoEnRevision)
        self.eventoSismicoSeleccionado.bloquearEnRevision(self.estadoBloqueadoEnRevision, self.cambioEstadoActual, self.fechaHoraActualBloqueadoEnRevision)
        

    def obtenerEstacionesSismográficas():
        pass

    def clasificarMuestrasPorEstaciones():
        pass

    def llamarCU18():
        pass
