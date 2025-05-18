from entities.TipoDeDato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self,velOnda, frecOnda, longOnda):
        self.velocidadOnda = velOnda
        self.frecuenciaOnda = frecOnda
        self.longitudOnda = longOnda
    
    def getVelocidad(self):
        return self.velocidadOnda
    def getFrecuencia(self):
        return self.frecuenciaOnda
    def getLongitud(self):
        return self.longitudOnda
    
    def setVelocidad(self, velocidad):
        self.velocidadOnda = velocidad
    def setFrecuencia(self, frecuencia):
        self.frecuenciaOnda = frecuencia
    def setLongitud(self, longitud):
        self.longitudOnda = longitud

