class Estado:
    def __init__(self, ambito, nombreEstado):
        self.ambito = ambito
        self.nombreEstado = nombreEstado

    # Métodos GET
    def getAmbito(self):
        return self.ambito

    def getNombreEstado(self):
        return self.nombreEstado

    # Métodos SET
    def setAmbito(self, ambito):
        self.ambito = ambito

    def setNombreEstado(self, nombreEstado):
        self.nombreEstado = nombreEstado
