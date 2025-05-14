class CambioEstado:
    def __init__(self, fechaHoraInicio, estado, fechaHoraFin=None):
        self.fechaHoraInicio = fechaHoraInicio
        self.estado = estado
        self.fechaHoraFin = fechaHoraFin

    # Métodos GET
    def getFechaHoraInicio(self):
        return self.fechaHoraInicio

    def getEstado(self):
        return self.estado

    def getFechaHoraFin(self):
        return self.fechaHoraFin

    # Métodos SET
    def setFechaHoraInicio(self, fechaHoraInicio):
        self.fechaHoraInicio = fechaHoraInicio

    def setEstado(self, estado):
        self.estado = estado

    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin
