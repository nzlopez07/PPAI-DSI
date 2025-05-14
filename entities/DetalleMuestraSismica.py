from entities.TipoDeDato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self,valor):
        self.__valor = valor
    #Getters
    def getValor(self):
        return self.__valor
    
    #Setters
    def setValor(self, valor):
        self.__valor = valor

    #Métodos realizacion CU
    def getDatos(self):
        return self.__denominacion    
