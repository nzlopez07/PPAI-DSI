from entities.Estado import Estado

class CambioEstado:
    def __init__(self, fechaHoraInicio, estado, fechaHoraFin=None):
        self.fechaHoraInicio = fechaHoraInicio
        self.estado: Estado = estado #Objeto del tipo Estado
        self.fechaHoraFin = fechaHoraFin # Cuando se crea el cambio de estado no tiene fecha de fin
        self.responsableInspeccion = None # Cuando se crea el cambio de estado a "AutoDetectado", todavía nadie hizo la revisión

    # Métodos GET
    def getFechaHoraInicio(self):
        return self.fechaHoraInicio

    def getEstado(self):
        return self.estado

    def getFechaHoraFin(self):
        return self.fechaHoraFin
    
    def getResponsableInspeccion(self):
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
        # Verificar que el objeto CambioEstado es del estado actual
        aux = False
        if self.fechaHoraFin == None:
            aux = True
        return aux
        #return self.fechaHoraFin == None
    
    def esEstadoAutoDetectado(self):
        # Verificar que el estado al que apunta el cambio de estado sea "AutoDetectado"
        autoDetectado = False
        if self.estado.getNombre() == "AutoDetectado":
            autoDetectado = True
        return autoDetectado