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

    def bloquearEnRevision(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        """
        Mensaje 17 del diagrama de secuencia: bloquearEnRevision()
        """
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)
        self.setEstadoActual(estado)
        print(f"[LOG] Evento bloqueado en revisión. Estado actual: {estado.getNombreEstado()}")

    def rechazar(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        """
        Mensaje 19 del diagrama de secuencia: rechazar()
        """
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)
        self.setEstadoActual(estado)
        # Marcar fin del evento (estado terminal)
        self.setFechaHoraFin(fechaHora)
        print(f"[LOG][EventoSismico] Evento rechazado. Estado actual: {estado.getNombreEstado()}")
        print(f"[LOG][EventoSismico] Historial de cambios de estado:")
        for idx, cambio in enumerate(self.cambioEstado):
            print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))()}")

    def confirmar(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        """
        Mensaje 15 del diagrama de secuencia: confirmar()
        """
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)
        self.setEstadoActual(estado)
        # Marcar fin del evento (estado terminal)
        self.setFechaHoraFin(fechaHora)
        print(f"[LOG][EventoSismico] Evento confirmado. Estado actual: {estado.getNombreEstado()}")
        print(f"[LOG][EventoSismico] Historial de cambios de estado:")
        for idx, cambio in enumerate(self.cambioEstado):
            print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))()}")

    def solicitarRevisionExperto(self, estado: Estado, cambioEstado: CambioEstado, fechaHora, usuario):
        """
        Mensaje 16 del diagrama de secuencia: solicitarRevisionExperto()
        """
        cambioEstado.setFechaHoraFin(fechaHora)
        cambioEstado.setResponsableInspeccion(usuario)
        nuevoCambioEstado = CambioEstado(fechaHora, estado, usuario)
        self.cambioEstado.append(nuevoCambioEstado)
        self.setEstadoActual(estado)
        print(f"[LOG][EventoSismico] Evento solicitado a revisión de experto. Estado actual: {estado.getNombreEstado()}")
        print(f"[LOG][EventoSismico] Historial de cambios de estado:")
        for idx, cambio in enumerate(self.cambioEstado):
            print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))()}")

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

    def _transicionar_a(self, nuevo_estado):
        """
        Método interno que realiza la transición de estado.
        - Cierra el CambioEstado actual (setea fechaHoraFin)
        - Crea un nuevo CambioEstado con el nuevo estado
        - Actualiza estadoActual
        
        Args:
            nuevo_estado (Estado): Instancia del nuevo estado concreto
        """
        # Usar una única marca de tiempo para cerrar y abrir el cambio
        ahora = datetime.now()

        # Obtener el cambio de estado actual y cerrarlo
        cambio_actual = self.obtenerEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(ahora)

        # Crear nuevo cambio de estado
        nuevo_cambio = CambioEstado(
            fechaHoraInicio=ahora,
            estado=nuevo_estado,
            responsable=None  # Se puede setear después si es necesario
        )

        # Agregar a la lista de cambios y actualizar estado actual
        self.cambioEstado.append(nuevo_cambio)
        self.setEstadoActual(nuevo_estado)

        # Si el nuevo estado es terminal (Confirmado o Rechazado), cerrar el evento
        try:
            if nuevo_estado.esConfirmado() or nuevo_estado.esRechazado():
                self.setFechaHoraFin(ahora)
        except AttributeError:
            # En caso de que el estado no implemente helpers, usar nombre de clase
            if nuevo_estado.__class__.__name__ in ("Confirmado", "Rechazado"):
                self.setFechaHoraFin(ahora)

        print(f"[LOG][EventoSismico] Transición completada a estado: {nuevo_estado.getNombreEstado()}")

    def bloquearEventoEnRevision(self):
        """
        Método de dominio: delega al estado actual la transición a BloqueadoEnRevision.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.bloquear(self)

    def confirmarEvento(self):
        """
        Método de dominio: delega al estado actual la transición a Confirmado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.confirmar(self)

    def rechazarEvento(self):
        """
        Método de dominio: delega al estado actual la transición a Rechazado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.rechazar(self)

    def solicitarRevisionExpertoEvento(self):
        """
        Método de dominio: delega al estado actual la transición a SolicitadoRevisionExperto.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.solicitarRevisionExperto(self)

    def cancelarRevision(self):
        """
        Método de dominio: delega al estado actual la transición a PendienteDeRevision.
        Usado cuando un analista cancela la revisión de un evento bloqueado.
        Lanzará excepción si la transición no está permitida desde el estado actual.
        """
        self.estadoActual.volverAPendiente(self)
