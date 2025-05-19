from entities.Usuario import Usuario
class Sesion:
    def __init__(self, fechaInicio, usuarioActivo):
        self.__fechaInicio = fechaInicio
        self.__fechaFin = None
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

    #Métodos realizacion CU
    def obtenerEmpleado(self):
        return self.__usuarioActivo.obtenerEmpleado()
    
