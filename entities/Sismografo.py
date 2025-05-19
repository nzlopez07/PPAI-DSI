from entities.EstacionSismologica import EstacionSismologica
#from data import series_mock


class Sismografo:
    def __init__(self, fechaAdquisicion, identificadorSismografo, nroSerie, estacionSismologica, seriesTemporales):
        self.__fechaAdquisicion = fechaAdquisicion
        self.__identificadorSismografo = identificadorSismografo
        self.__nroSerie = nroSerie
        
        #Atributos referenciales
        self.seriesSismologicas = seriesTemporales
        self.__estacionSismologica: EstacionSismologica = estacionSismologica
    
    #Getters
    def getFechaAdquisicion(self):
        return self.__fechaAdquisicion
    def getIdentificadorSismografo(self):
        return self.__identificadorSismografo
    def getNroSerie(self):
        return self.__nroSerie
    def getEstacionSismologica(self):
        return self.__estacionSismologica
    
    #Setters
    def setFechaAdquisicion(self, fechaAdquisicion):
        self.__fechaAdquisicion = fechaAdquisicion
    def setIdentificadorSismografo(self, identificadorSismografo):
        self.__identificadorSismografo = identificadorSismografo
    def setNroSerie(self, nroSerie):
        self.__nroSerie = nroSerie
    def setEstacionSismologica(self, estacionSismologica):
        self.__estacionSismologica = estacionSismologica

    #Métodos realizacion CU
    def esTuSerie(self, serieTemporal):
        for serie in self.seriesSismologicas:
            if serie == serieTemporal:
                return True
        return False