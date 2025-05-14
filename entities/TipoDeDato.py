class TipoDeDato:
    def __init__(self, denominacion, nombreUnidadMedida, valorUmbral):
        self.__denominacion = denominacion
        self.__nombreUnidadMedida = nombreUnidadMedida
        self.__valorUmbral = valorUmbral

    #Getters
    def getDenominacion(self):
        return self.__denominacion
    def getNombreUnidadMedida(self):
        return self.__nombreUnidadMedida
    def getValorUmbral(self):
        return self.__valorUmbral
    
    #Setters
    def setDenominacion(self, denominacion):
        self.__denominacion = denominacion
    def setNombreUnidadMedida(self, nombreUnidadMedida):
        self.__nombreUnidadMedida = nombreUnidadMedida
    def setValorUmbral(self, valorUmbral):
        self.__valorUmbral = valorUmbral

    #Métodos realizacion CU
    def esTuDenominacion(self, denominacionInput):
        return self.__denominacion == denominacionInput