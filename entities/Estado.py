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
        print("Entramos al método esAutoDetectado de Estado correctamente")
        return self.nombreEstado == "AutoDetectado"
   
    
    def esBloqueadoParaRevision(self):
        # Verificar que el estado sea "BloqueadoParaRevision"
        return self.nombreEstado == "BloqueadoParaRevision"
    
    def esPendienteDeRevision(self):
        return self.nombreEstado == "PendienteDeRevision"
            
