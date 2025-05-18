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
   
    
    def esBloqueadoEnRevision(self):
        # Verificar que el estado sea "BloqueadoEnRevision"
        return self.nombreEstado == "BloqueadoEnRevision"
    
    def esPendienteDeRevision(self):
        return self.nombreEstado == "PendienteDeRevision"
            
    def esAmbitoEventoSismico(self):
        return self.ambito == "EventoSismico"
    
    def esAmbitoSerieTemporal(self):
        return self.ambito == "SerieTemporal"