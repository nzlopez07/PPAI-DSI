from entities.Empleado import Empleado
class Usuario:
    def __init__(self, contraseña, nombreUsuario, empleado):
        self.__contraseña = contraseña
        self.__nombreUsuario = nombreUsuario
        self.__empleado = empleado
    
    #Getters
    def getContraseña(self):
        return self.__contraseña
    def getNombreUsuario(self):
        return self.__nombreUsuario
    def getEmpleado(self):
        return self.__empleado

    #Setters
    def setContraseña(self, contraseña):
        self.__contraseña = contraseña
    def setNombreUsuario(self, nombreUsuario):
        self.__nombreUsuario = nombreUsuario
    def setEmpleado(self, empleado):
        self.__empleado = empleado


    #Métodos realizacion CU
    def obtenerEmpleado(self):
        return self.getEmpleado