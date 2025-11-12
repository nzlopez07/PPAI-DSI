from entities.AlcanceSismo import AlcanceSismo
from entities.CambioEstado import CambioEstado
from entities.Estado import Estado
from entities.SerieTemporal import SerieTemporal
from entities.ClasificacionSismo import ClasificacionSismo
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from datetime import datetime


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


    # --- Métodos de tracking y lógica de estados ---
    def estaAutoDetectado(self):
        """
        Mensaje 12 del diagrama de secuencia: estaAutoDetectado()
        """
        return self.estadoActual.esAutoDetectado()

    def estaPendienteDeRevision(self):
        """
        Mensaje 12 del diagrama de secuencia: estaPendienteDeRevision()
        """
        return self.estadoActual.esPendienteDeRevision()

    def obtenerEstadoActual(self):
        """
        Mensaje 14 del diagrama de secuencia: obtenerEstadoActual()
        """
        for cambioEstado in self.cambioEstado:
            if cambioEstado.esEstadoActual():
                return cambioEstado


    def obtenerDatosEvento(self):
        """
        Mensaje 13 del diagrama de secuencia: obtenerDatosEvento()
        """
        alcance = self.getAlcanceSismo().getNombre()
        origen = self.getOrigenGeneracion().getNombre()
        clasificacion = self.getClasificacion().getNombre()
        print(f"[LOG] Datos del evento: Origen={origen}, Alcance={alcance}, Clasificación={clasificacion}")
        return alcance, origen, clasificacion

    def validarDatos(self):
        """
        Mensaje 20 del diagrama de secuencia: validarDatos()
        """
        if(self.valorMagnitud == None) or (self.alcanceSismo == None) or (self.origenGeneracion == None):
            return False
        else:
            return True

    # ======================================================
    # Métodos del patrón State - Transiciones delegadas
    # ======================================================

    def agregarCambioEstado(self, cambioNuevo):
        self.cambioEstado.append(cambioNuevo)


    def bloquearEventoEnRevision(self, fecha_hora_cambio_estado, responsable):
        """
        Método de dominio: delega al estado actual la transición a BloqueadoEnRevision.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.bloquear(self, fecha_hora_cambio_estado, self.cambioEstado, responsable)

    def confirmarEvento(self, fecha_hora_cambio_estado, responsable):
        """
        Método de dominio: delega al estado actual la transición a Confirmado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.confirmar(self, fecha_hora_cambio_estado, self.cambioEstado,responsable)

    def rechazarEvento(self, fecha_hora_cambio_estado, responsable):
        """
        Método de dominio: delega al estado actual la transición a Rechazado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.rechazar(self, fecha_hora_cambio_estado, self.cambioEstado, responsable)

    def solicitarRevisionExpertoEvento(self, fecha_hora_cambio_estado, responsable):
        """
        Método de dominio: delega al estado actual la transición a SolicitadoRevisionExperto.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.solicitarRevisionExperto(self, fecha_hora_cambio_estado, self.cambioEstado, responsable)

    def cancelarRevision(self):
        """
        Método de dominio: delega al estado actual la transición a PendienteDeRevision.
        Usado cuando un analista cancela la revisión de un evento bloqueado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.volverAPendiente(self, self.cambioEstado)
