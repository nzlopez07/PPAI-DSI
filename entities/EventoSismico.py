from entities.AlcanceSismo import AlcanceSismo
from entities.CambioEstado import CambioEstado
from entities.Estado import Estado
from entities.SerieTemporal import SerieTemporal
from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion


class EventoSismico:
    def __init__(self, clasificacion, magnitud, origenGeneracion, alcanceSismo,  
                 estadoActual, cambiosEstado, serieTemporal,
                 fechaHoraOcurrencia, latitudEpicentro, latitudHipocentro, 
                 longitudEpicentro, longitudHipocentro, valorMagnitud, fechaHoraFin=None):
        
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud

        # atributos referenciales (son objetos)
        self.clasificacion: ClasificacionSismo = clasificacion
        self.magnitud = magnitud
        self.origenGeneracion: OrigenDeGeneracion = origenGeneracion
        self.alcanceSismo: AlcanceSismo = alcanceSismo
        self.estadoActual: Estado = estadoActual
        self.cambioEstado: list[CambioEstado] = cambiosEstado
        self.serieTemporal: list[SerieTemporal] = serieTemporal # Es una lista

    # Métodos GET
    def getFechaHoraFin(self):
        return self.fechaHoraFin
    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia
    def getLatitudEpicentro(self):
        return self.latitudEpicentro
    def getLatitudHipocentro(self):
        return self.latitudHipocentro
    def getLongitudEpicentro(self):
        return self.longitudEpicentro
    def getLongitudHipocentro(self):
        return self.longitudHipocentro
    def getValorMagnitud(self):
        return self.valorMagnitud
    
    # devuelven punteros
    def getClasificacion(self):
        return self.clasificacion
    def getMagnitud(self):
        return self.magnitud
    def getOrigenGeneracion(self):
        return self.origenGeneracion
    def getAlcanceSismo(self):
        return self.alcanceSismo
    def getEstadoActual(self):
        return self.estadoActual
    def getCambioEstado(self):
        return self.cambioEstado
    def getSerieTemporal(self):
        return self.serieTemporal

    # Métodos SET
    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin
    def setFechaHoraOcurrencia(self, fechaHoraOcurrencia):
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
    def setLatitudEpicentro(self, latitudEpicentro):
        self.latitudEpicentro = latitudEpicentro
    def setLatitudHipocentro(self, latitudHipocentro):
        self.latitudHipocentro = latitudHipocentro
    def setLongitudEpicentro(self, longitudEpicentro):
        self.longitudEpicentro = longitudEpicentro
    def setLongitudHipocentro(self, longitudHipocentro):
        self.longitudHipocentro = longitudHipocentro
    def setValorMagnitud(self, valorMagnitud):
        self.valorMagnitud = valorMagnitud

    # modifican el objeto al que apuntan
    def setClasificacion(self, clasificacion):
        self.clasificacion = clasificacion
    def setMagnitud(self, magnitud):
        self.magnitud = magnitud
    def setOrigenGeneracion(self, origenGeneracion):
        self.origenGeneracion = origenGeneracion
    def setAlcanceSismo(self, alcanceSismo):
        self.alcanceSismo = alcanceSismo
    def setEstadoActual(self, estadoActual):
        self.estadoActual = estadoActual
    def setCambioEstado(self, cambioEstado):
        self.cambioEstado = cambioEstado
    def setSerieTemporal(self, serieTemporal):
        self.serieTemporal = serieTemporal

    # Otros métodos
    def estaAutoDetectado(self):
        return self.estadoActual.esAutoDetectado()
    
    def estaPendienteDeRevision(self):
        return self.estadoActual.esPendienteDeRevision()

    def obtenerEstadoActual(self):
        # Si el cambio de estado es el estado actual devuelve el cambio de estado
        # Sino devuelve None (En caso de no encontrar nada)
        for cambioEstado in self.cambioEstado:
            if cambioEstado.esEstadoActual():
                return cambioEstado

    # Método que corresponedría a la maquina de estados
    def bloquearEnRevision(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)

    def rechazar(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)

    def confirmar(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)

    def solicitarRevisionExperto(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)

    # Nombres a chequear
    def obtenerDatosEvento(self):
        print("\n\nObtenemos datos del evento")
        alcance = self.getAlcanceSismo().getNombre()
        origen = self.getOrigenGeneracion().getNombre()
        clasificacion = self.getClasificacion().getNombre()
        print("Nombre origen: ", origen)
        print("Nombre alcance: ", alcance)
        print("Nombre clasificacion: ", clasificacion)
        print("\n")
        return alcance, origen, clasificacion
    
    def validarDatos(self):
        if(self.valorMagnitud == None) or (self.alcanceSismo == None) or (self.origenGeneracion == None):
            return False
        else:
            return True
