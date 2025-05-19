from entities.MuestraSismica import MuestraSismica
from data import sismografos_mock

class SerieTemporal:
    def __init__(self, condicionAlarma, fechaHoraInicioRegistroMuestras, fechaHoraRegistro, frecuenciaMuestreo, muestraSismica):
        self.__condicionAlarma = condicionAlarma
        self.__fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self.__fechaHoraRegistro = fechaHoraRegistro
        self.__frecuenciaMuestreo = frecuenciaMuestreo
        self.__muestraSismica = muestraSismica

    #Getters
    def getCondicionAlarma(self):
        return self.__condicionAlarma
    def getFechaHoraInicioRegistroMuestras(self):
        return self.__fechaHoraInicioRegistroMuestras
    def getFechaHoraRegistro(self):
        return self.__fechaHoraRegistro
    def getFrecuenciaMuestreo(self):
        return self.__frecuenciaMuestreo
    def getMuestraSismica(self):
        return self.__muestraSismica
    
    #Setters
    def setCondicionAlarma(self, condicionAlarma):
        self.__condicionAlarma = condicionAlarma
    def setFechaHoraInicioRegistroMuestras(self, fechaHoraInicioRegistroMuestras):
        self.__fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
    def setFechaHoraRegistro(self, fechaHoraRegistro):
        self.__fechaHoraRegistro = fechaHoraRegistro
    def setFrecuenciaMuestreo(self, frecuenciaMuestreo):
        self.__frecuenciaMuestreo = frecuenciaMuestreo
    def setMuestraSismica(self, muestraSismica):
        self.__muestraSismica = muestraSismica

    def obtenerNombreEstacion(self):
        for sismografo in sismografos_mock:
            if sismografo.esTuSerie(self):
                return sismografo.getEstacionSismologica().getNombre()
        