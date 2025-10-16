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
        """
        Mensaje auxiliar: esAutoDetectado()
        """
        return self.nombreEstado == "AutoDetectado"

    def esBloqueadoEnRevision(self):
        """
        Mensaje auxiliar: esBloqueadoEnRevision()
        """
        return self.nombreEstado == "BloqueadoEnRevision"

    def esPendienteDeRevision(self):
        """
        Mensaje auxiliar: esPendienteDeRevision()
        """
        return self.nombreEstado == "PendienteDeRevision"

    def esAmbitoEventoSismico(self):
        """
        Mensaje auxiliar: esAmbitoEventoSismico()
        """
        return self.ambito == "EventoSismico"

    def esAmbitoSerieTemporal(self):
        """
        Mensaje auxiliar: esAmbitoSerieTemporal()
        """
        return self.ambito == "SerieTemporal"

    def esRechazado(self):
        """
        Mensaje auxiliar: esRechazado()
        """
        return self.nombreEstado == "Rechazado"

    def esConfirmado(self):
        """
        Mensaje auxiliar: esConfirmado()
        """
        return self.nombreEstado == "Confirmado"

    def esSolicitadoRevisionExperto(self):
        """
        Mensaje auxiliar: esSolicitadoRevisionExperto()
        """
        return self.nombreEstado == "SolicitadoRevisionExperto"