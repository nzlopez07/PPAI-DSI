class Sesion:
    def __init__(self, fechaInicio, fechaFin, usuarioActivo):
        self.__fechaInicio = fechaInicio
        self.__fechaFin = fechaFin
        self.__usuarioActivo = usuarioActivo
    
    #Getters
    def getFechaInicio(self):
        return self.__fechaInicio
    def getFechaFin(self):
        return self.__fechaFin
    def getUsuarioActivo(self):
        return self.__usuarioActivo
    
    #Setters
    def setFechaInicio(self, fechaInicio):
        self.__fechaInicio = fechaInicio
    def setFechaFin(self, fechaFin):
        self.__fechaFin = fechaFin
    def setUsuarioActivo(self, usuarioActivo):
        self.__usuarioActivo = usuarioActivo