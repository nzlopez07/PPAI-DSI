from datetime import datetime
from entities.EventoSismico import EventoSismico
from data import eventos_mock

class GestorRevisionEventoSismico:
    def __init__(self):
        self.horaFechaFinCambioEstado = None
        self.eventosSismicos: list[EventoSismico] = eventos_mock # Colección de todos los eventos sísmicos
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"

    #Métodos get y set si corresponden
    def getEventosSismicos(self):
        return self.eventosSismicos
    def getEventosSismicosAutoDetectados(self):
        return self.eventosSismicosAutoDetectados

    # Lógica del CU
    def opcRegistrarResultadoRevisionManual(self):
        return self.buscarEventosAutoDetectados()

    def calcularFechaHoraFinCambioEstado(self):
    # Método para calcular fecha y hora en el momento    
        self.horaFechaFinCambioEstado = datetime.now()
    
    def buscarEventosAutoDetectados(self):
        print("Entramos al método buscarEventosAutoDetectados de Gestor correctamente")
        # Recorre la colección de todos los eventos sísmicos y valida que tengan el estado "AutoDetectado"
        self.eventosSismicosAutoDetectados = []
        for evento in self.eventosSismicos:
            if (evento.estaAutoDetectado()) or (evento.estaPendienteDeRevision()):
                self.eventosSismicosAutoDetectados.append(evento)
        self.ordenarPorFechaYHora(self.eventosSismicosAutoDetectados)
        #return self.eventosSismicosAutoDetectados

    
    def ordenarPorFechaYHora(self, eventosSismicos:list[EventoSismico]):
        n = len(eventosSismicos)
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if eventosSismicos[i].getFechaHoraOcurrencia() > eventosSismicos[j].getFechaHoraOcurrencia():
                    eventosSismicos[i], eventosSismicos[j] = eventosSismicos[j], eventosSismicos[i]
        
        return eventosSismicos
            

    def obtenerEstacionesSismográficas():
        pass

    def clasificarMuestrasPorEstaciones():
        pass

    def llamarCU18():
        pass
