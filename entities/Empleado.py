class Empleado:
    def __init__(self, apellido, mail, nombre, telefono):
        self.__apellido = apellido
        self.__mail = mail
        self.__nombre = nombre
        self.__telefono = telefono

    #Getters
    def getEmpleado(self):
        return self.__apellido, self.__mail, self.__nombre, self.__telefono
    def getApellido(self):
        return self.__apellido
    def getMail(self):
        return self.__mail
    def getNombre(self):
        return self.__nombre
    def getTelefono(self):
        return self.__telefono
    
    #Setters
    def setApellido(self, apellido):
        self.__apellido = apellido
    def setMail(self, mail):
        self.__mail = mail
    def setNombre(self, nombre):
        self.__nombre = nombre
    def setTelefono(self, telefono):
        self.__telefono = telefono