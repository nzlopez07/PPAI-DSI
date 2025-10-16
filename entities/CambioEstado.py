from entities.Estado import Estado

class CambioEstado:
    def __init__(self, fechaHoraInicio, estado, responsable, fechaHoraFin=None):
        self.fechaHoraInicio = fechaHoraInicio
        self.estado: Estado = estado #Objeto del tipo Estado
        self.fechaHoraFin = fechaHoraFin # Cuando se crea el cambio de estado no tiene fecha de fin
        self.responsableInspeccion = responsable # Cuando se crea el cambio de estado a "AutoDetectado", todavía nadie hizo la revisión

    # Métodos GET
    def getFechaHoraInicio(self):
        """
        Mensaje auxiliar: getFechaHoraInicio()
        """
        return self.fechaHoraInicio

    def getEstado(self):
        """
        Mensaje auxiliar: getEstado()
        """
        return self.estado

    def getFechaHoraFin(self):
        """
        Mensaje auxiliar: getFechaHoraFin()
        """
        return self.fechaHoraFin
    
    def getResponsableInspeccion(self):
        """
        Mensaje auxiliar: getResponsableInspeccion()
        """
        return self.responsableInspeccion

    # Métodos SET
    def setFechaHoraInicio(self, fechaHoraInicio):
        self.fechaHoraInicio = fechaHoraInicio

    def setEstado(self, estado):
        self.estado = estado

    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin

    def setResponsableInspeccion(self, responsable):
        self.responsableInspeccion = responsable

    # Definición de otros métodos

    def esEstadoActual(self):
        """
        Mensaje auxiliar: esEstadoActual()
        """
        return self.fechaHoraFin is None
    
    def esEstadoAutoDetectado(self):
        """
        Mensaje auxiliar: esEstadoAutoDetectado()
        """
        return self.estado.getNombreEstado() == "AutoDetectado"