from datetime import datetime
from entities.EventoSismico import EventoSismico

class GestorRevisionEventoSismico:
    def __init__(self, eventos):
        self.horaFechaFinCambioEstado = None
        self.eventosSismicos: list[EventoSismico] = eventos # Colección de todos los eventos sísmicos
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"

    #Métodos get y set si corresponden
    def getEventosSismicos(self):
        return self.eventosSismicos
    def getEventosSismicosAutoDetectados(self):
        return self.eventosSismicosAutoDetectados

    # Lógica del CU
    def calcularFechaHoraFinCambioEstado(self):
    # Método para calcular fecha y hora en el momento    
        self.horaFechaFinCambioEstado = datetime.now()
    
    def buscarEventosAutoDetectados(self):
        print("Entramos al método buscarEventosAutoDetectados de Gestor correctamente")
        # Recorre la colección de todos los eventos sísmicos y valida que tengan el estado "AutoDetectado"
        for evento in self.eventosSismicos:
            if evento.estaAutoDetectado():
                self.eventosSismicosAutoDetectados.append(evento)

    def ordenarPorFechaYHora():
        pass

    def obtenerEstacionesSismográficas():
        pass

    def clasificarMuestrasPorEstaciones():
        pass

    def llamarCU18():
        pass
