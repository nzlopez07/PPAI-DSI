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

    # Definición de otros métodos
    def esAutoDetectado(self):
        # Verificar que el estado sea "AutoDetectado"
        autoDetectado = False
        if self.nombreEstado == "AutoDetectado":
            autoDetectado = True
        return autoDetectado
    
    def esBloqueadoParaRevision(self):
        # Verificar que el estado sea "BloqueadoParaRevision"
        bloqueadoParaRevision = False
        if self.nombreEstado == "BloqueadoParaRevision":
            bloqueadoParaRevision = True
        return bloqueadoParaRevision
