class EventoSismico:
    def __init__(self, clasificacion, magnitud, origenGeneracion, alcanceSismo,  
                 estadoActual, cambioEstado, serieActual,
                 fechaHoraOcurrencia, latitudEpicentro, latitudHipocentro, 
                 longitudEpicentro, longitudHipocentro, valorMagnitud, fechaHoraFin=None):
        
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud

        # atributos referenciales
        self.clasificacion = clasificacion
        self.magnitud = magnitud
        self.origenGeneracion = origenGeneracion
        self.alcanceSismo = alcanceSismo
        self.estadoActual = estadoActual
        self.cambioEstado = cambioEstado
        self.serieActual = serieActual

    # Métodos GET
    def getFechaHoraFin(self):
        return self.fechaHoraFin
    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia
    def getLatitudEpicentro(self):
        return self.latitudEpicentro
    def getLatitudHipocentro(self):
        return self.latitudHipocentro
    def getLongitudEpicentro(self):
        return self.longitudEpicentro
    def getLongitudHipocentro(self):
        return self.longitudHipocentro
    def getValorMagnitud(self):
        return self.valorMagnitud
    
    # devuelven punteros
    def getClasificacion(self):
        return self.clasificacion
    def getMagnitud(self):
        return self.magnitud
    def getOrigenGeneracion(self):
        return self.origenGeneracion
    def getAlcanceSismo(self):
        return self.alcanceSismo
    def getEstadoActual(self):
        return self.estadoActual
    def getCambioEstado(self):
        return self.cambioEstado
    def getSerieActual(self):
        return self.serieActual

    # Métodos SET
    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin
    def setFechaHoraOcurrencia(self, fechaHoraOcurrencia):
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
    def setLatitudEpicentro(self, latitudEpicentro):
        self.latitudEpicentro = latitudEpicentro
    def setLatitudHipocentro(self, latitudHipocentro):
        self.latitudHipocentro = latitudHipocentro
    def setLongitudEpicentro(self, longitudEpicentro):
        self.longitudEpicentro = longitudEpicentro
    def setLongitudHipocentro(self, longitudHipocentro):
        self.longitudHipocentro = longitudHipocentro
    def setValorMagnitud(self, valorMagnitud):
        self.valorMagnitud = valorMagnitud

    # modifican el objeto al que apuntan
    def setClasificacion(self, clasificacion):
        self.clasificacion = clasificacion
    def setMagnitud(self, magnitud):
        self.magnitud = magnitud
    def setOrigenGeneracion(self, origenGeneracion):
        self.origenGeneracion = origenGeneracion
    def setAlcanceSismo(self, alcanceSismo):
        self.alcanceSismo = alcanceSismo
    def setEstadoActual(self, estadoActual):
        self.estadoActual = estadoActual
    def setCambioEstado(self, cambioEstado):
        self.cambioEstado = cambioEstado
    def setSerieActual(self, serieActual):
        self.serieActual = serieActual

    
