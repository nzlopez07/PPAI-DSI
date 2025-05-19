from entities.TipoDeDato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self,velOnda, frecOnda, longOnda):
        self.velocidadOnda = velOnda
        self.frecuenciaOnda = frecOnda
        self.longitudOnda = longOnda
    
    def getVelocidadOnda(self):
        return self.velocidadOnda
    def getFrecuenciaOnda(self):
        return self.frecuenciaOnda
    def getLongitudOnda(self):
        return self.longitudOnda
    
    def setVelocidadOnda(self, velocidad):
        self.velocidadOnda = velocidad
    def setFrecuenciaOnda(self, frecuencia):
        self.frecuenciaOnda = frecuencia
    def setLongitudOnda(self, longitud):
        self.longitudOnda = longitud

