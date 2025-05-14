from datetime import datetime
from entities.EventoSismico import EventoSismico
class GestorRevisionEventoSismico:
    def __init__(self, eventosSismicos):
        self.__eventosSismicos = eventosSismicos

    #Métodos get y set si corresponden

    def calcularHoraFechaActual(self):
    # Método para calcular fecha y hora en el momento    
        return datetime.now()
    
    def buscarEventosAutoDetectados(self):
        eventosAutoDetectados = []
        for evento in self.__eventosSismicos:
            if evento.EstaAutoDetectado():
                eventosAutoDetectados.append(evento)
        return eventosAutoDetectados