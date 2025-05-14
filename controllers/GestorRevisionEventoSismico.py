from datetime import datetime
from entities.EventoSismico import EventoSismico

class GestorRevisionEventoSismico:
    def __init__(self):
        self.horaFechaFinCambioEstado = None
        self.eventosSismicos: list[EventoSismico] = [] # Colección de todos los eventos sísmicos
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"

    #Métodos get y set si corresponden

    # Lógica del CU
    def calcularFechaHoraFinCambioEstado(self):
    # Método para calcular fecha y hora en el momento    
        self.horaFechaFinCambioEstado = datetime.now()
    
    def buscarEventosAutoDetectados(self):
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
