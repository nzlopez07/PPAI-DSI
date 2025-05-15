class MagnitudRichter:
    def __init__(self,descripcionMagnitud,numero):
        self.descripcionMagnitud = descripcionMagnitud
        self.numero = numero

    # Metodos GET
    def getDescripcionMagnitud(self):
        return self.descripcionMagnitud

    def getNumero(self):
        return self.numero
    
    # Metodos SET

    def setDescripcionMagnitud(self, descripcionMagnitud):
        self.descripcionMagnitud = descripcionMagnitud
        
    def setNumero(self, numero):
        self.numero = numero