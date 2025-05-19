from entities.DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fechaHoraMuestra,detalleMuestraSismica):
        self.fechaHoraMuestra = fechaHoraMuestra
        self.detalleMuestraSismica: list[DetalleMuestraSismica] = detalleMuestraSismica

    #Getters
    def getFechaHoraMuestra(self):
        return self.fechaHoraMuestra
    def getDetalleMuestraSismica(self):
        return self.detalleMuestraSismica
    
    #Setters
    def setFechaHoraMuestra(self, fechaHoraMuestra):
        self.fechaHoraMuestra = fechaHoraMuestra
    def setDetalleMuestraSismica(self, DetalleMuestraSismica):
        self.detalleMuestraSismica = DetalleMuestraSismica

    #Métodos realizacion CU
    