from entities.DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fechaHoraMuestra,DetalleMuestraSismica):
        self.__fechaHoraMuestra = fechaHoraMuestra
        self.__DetalleMuestraSismica = DetalleMuestraSismica

    #Getters
    def getFechaHoraMuestra(self):
        return self.__fechaHoraMuestra
    def getDetalleMuestraSismica(self):
        return self.__DetalleMuestraSismica
    
    #Setters
    def setFechaHoraMuestra(self, fechaHoraMuestra):
        self.__fechaHoraMuestra = fechaHoraMuestra
    def setDetalleMuestraSismica(self, DetalleMuestraSismica):
        self.__DetalleMuestraSismica = DetalleMuestraSismica

    #Métodos realizacion CU
    def getDatos(self):
        return self.__DetalleMuestraSismica.getDatos()