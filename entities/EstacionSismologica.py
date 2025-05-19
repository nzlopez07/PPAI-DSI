class EstacionSismologica:
    def __init__(self, codigoEstacion, documentoCertificacionAdq, fechaSolicitudCertificacion, latitud, longitud, nombre, nroCertificacionAquision):
        self.__codigoEstacion = codigoEstacion
        self.__documentoCertificacionAdq = documentoCertificacionAdq
        self.__fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.__latitud = latitud
        self.__longitud = longitud
        self.__nombre = nombre
        self.__nroCertificacionAquision = nroCertificacionAquision
    
    #Getters
    def getCodigoEstacion(self):
        return self.__codigoEstacion
    def getDocumentoCertificacionAdq(self):
        return self.__documentoCertificacionAdq
    def getFechaSolicitudCertificacion(self):
        return self.__fechaSolicitudCertificacion
    def getLatitud(self):
        return self.__latitud
    def getLongitud(self):
        return self.__longitud
    def getNombre(self):
        return self.__nombre
    def getNroCertificacionAquision(self):
        return self.__nroCertificacionAquision
    
    #Setters
    def setCodigoEstacion(self, codigoEstacion):
        self.__codigoEstacion = codigoEstacion
    def setDocumentoCertificacionAdq(self, documentoCertificacionAdq):
        self.__documentoCertificacionAdq = documentoCertificacionAdq
    def setFechaSolicitudCertificacion(self, fechaSolicitudCertificacion):
        self.__fechaSolicitudCertificacion = fechaSolicitudCertificacion
    def setLatitud(self, latitud):
        self.__latitud = latitud
    def setLongitud(self, longitud):
        self.__longitud = longitud
    def setNombre(self, nombre):
        self.__nombre = nombre
    def setNroCertificacionAquision(self, nroCertificacionAquision):
        self.__nroCertificacionAquision = nroCertificacionAquision

