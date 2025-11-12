"""
Patrón State para el dominio de EventoSismico.
Estado base abstracto con subclases concretas para cada estado posible.
Mantiene compatibilidad con código existente mediante métodos esX() y getNombreEstado().
"""


class Estado:
    """
    Clase base abstracta para el patrón State.
    Define la interfaz común y transiciones por defecto (no permitidas).
    """
    nombreEstado = "Estado"
    ambito = "EventoSismico"
    
    def __init__(self):
        """Constructor sin parámetros. Subclases definen nombreEstado y ambito como atributos de clase."""
        pass

    # Métodos GET (compatibilidad con código existente)
    def getAmbito(self):
        return self.ambito

    def getNombreEstado(self):
        return self.nombreEstado

    # Métodos SET (mantenidos por compatibilidad, pero no deberían usarse en el patrón State puro)
    def setAmbito(self, ambito):
        self.ambito = ambito

    def setNombreEstado(self, nombreEstado):
        self.nombreEstado = nombreEstado

    # Métodos de consulta de tipo (por defecto todos False, override en subclases)
    def esAutoDetectado(self):
        """Mensaje auxiliar: esAutoDetectado()"""
        return False

    def esBloqueadoEnRevision(self):
        """Mensaje auxiliar: esBloqueadoEnRevision()"""
        return False

    def esPendienteDeRevision(self):
        """Mensaje auxiliar: esPendienteDeRevision()"""
        return False

    def esRechazado(self):
        """Mensaje auxiliar: esRechazado()"""
        return False

    def esConfirmado(self):
        """Mensaje auxiliar: esConfirmado()"""
        return False

    def esSolicitadoRevisionExperto(self):
        """Mensaje auxiliar: esSolicitadoRevisionExperto()"""
        return False

    def esAmbitoEventoSismico(self):
        """Mensaje auxiliar: esAmbitoEventoSismico()"""
        return self.ambito == "EventoSismico"

    def esAmbitoSerieTemporal(self):
        """Mensaje auxiliar: esAmbitoSerieTemporal()"""
        return self.ambito == "SerieTemporal"


    # Métodos de transición (por defecto no permitidas, override en subclases según reglas de negocio)
    def bloquear(self, evento, fecha_hora_cambio_estado, cambio_estados, responsable):
        """Transición a BloqueadoEnRevision"""
        raise ValueError(f"Transición 'bloquear' no permitida desde estado {self.nombreEstado}")

    def confirmar(self, evento):
        """Transición a Confirmado"""
        raise ValueError(f"Transición 'confirmar' no permitida desde estado {self.nombreEstado}")

    def rechazar(self, evento):
        """Transición a Rechazado"""
        raise ValueError(f"Transición 'rechazar' no permitida desde estado {self.nombreEstado}")

    def solicitarRevisionExperto(self, evento):
        """Transición a SolicitadoRevisionExperto"""
        raise ValueError(f"Transición 'solicitarRevisionExperto' no permitida desde estado {self.nombreEstado}")

    def volverAPendiente(self, evento):
        """Transición a PendienteDeRevision (usado al cancelar)"""
        raise ValueError(f"Transición 'volverAPendiente' no permitida desde estado {self.nombreEstado}")



# ===========================
# Subclases concretas de Estado
# ===========================

class AutoDetectado(Estado):
    """Estado inicial cuando un evento es detectado automáticamente por el sistema."""
    nombreEstado = "AutoDetectado"
    ambito = "EventoSismico"

    def esAutoDetectado(self):
        return True

    def bloquear(self, evento, fecha_hora_cambio_estado, cambios_estado, responsable):
        """AutoDetectado -> BloqueadoEnRevision (cuando un analista selecciona el evento)"""
        from entities.Estado import BloqueadoEnRevision
        from entities.CambioEstado import CambioEstado
        for cambio_estado in cambios_estado:
            if cambio_estado.esEstadoActual():
                cambio_estado.setFechaHoraFin(fecha_hora_cambio_estado)
        nuevo_estado = BloqueadoEnRevision()
        nuevo_cambio = CambioEstado(fecha_hora_cambio_estado, nuevo_estado, responsable)  
        evento.agregarCambioEstado(nuevo_cambio)
        evento.setEstadoActual(nuevo_estado)


class PendienteDeRevision(Estado):
    """Estado cuando un evento requiere revisión manual pero no está siendo procesado."""
    nombreEstado = "PendienteDeRevision"
    ambito = "EventoSismico"

    def esPendienteDeRevision(self):
        return True

    def bloquear(self, evento, fecha_hora_cambio_estado, cambios_estado, responsable):
        """PendienteDeRevision -> BloqueadoEnRevision (cuando un analista selecciona el evento)"""
        from entities.Estado import BloqueadoEnRevision
        from entities.CambioEstado import CambioEstado
        for cambio_estado in cambios_estado:
            if cambio_estado.esEstadoActual():
                cambio_estado.setFechaHoraFin(fecha_hora_cambio_estado)
        nuevo_estado = BloqueadoEnRevision()
        nuevo_cambio = CambioEstado(fecha_hora_cambio_estado, nuevo_estado, responsable)  
        evento.agregarCambioEstado(nuevo_cambio)
        evento.setEstadoActual(nuevo_estado)



class BloqueadoEnRevision(Estado):
    """Estado cuando un analista está revisando el evento (bloqueado para otros analistas)."""
    nombreEstado = "BloqueadoEnRevision"
    ambito = "EventoSismico"

    def esBloqueadoEnRevision(self):
        return True

    def confirmar(self, evento, fecha_hora_cambio_estado, cambios_estado, responsable):
        """BloqueadoEnRevision -> Confirmado"""
        from entities.Estado import Confirmado
        from entities.CambioEstado import CambioEstado
        for cambio_estado in cambios_estado:
            if cambio_estado.esEstadoActual():
                cambio_estado.setFechaHoraFin(fecha_hora_cambio_estado)
        nuevo_estado = Confirmado()
        nuevo_cambio = CambioEstado(fecha_hora_cambio_estado, nuevo_estado, responsable)  
        evento.agregarCambioEstado(nuevo_cambio)
        evento.setEstadoActual(nuevo_estado)


    def rechazar(self, evento, fecha_hora_cambio_estado, cambios_estado, responsable):
        """BloqueadoEnRevision -> Rechazado"""
        from entities.Estado import Rechazado
        from entities.CambioEstado import CambioEstado
        for cambio_estado in cambios_estado:
            if cambio_estado.esEstadoActual():
                cambio_estado.setFechaHoraFin(fecha_hora_cambio_estado)
        nuevo_estado = Rechazado()
        nuevo_cambio = CambioEstado(fecha_hora_cambio_estado, nuevo_estado, responsable)  
        evento.agregarCambioEstado(nuevo_cambio)
        evento.setEstadoActual(nuevo_estado)


    def solicitarRevisionExperto(self, evento, fecha_hora_cambio_estado, cambios_estado, responsable):
        """BloqueadoEnRevision -> SolicitadoRevisionExperto"""
        from entities.Estado import SolicitadoRevisionExperto
        from entities.CambioEstado import CambioEstado
        for cambio_estado in cambios_estado:
            if cambio_estado.esEstadoActual():
                cambio_estado.setFechaHoraFin(fecha_hora_cambio_estado)
        nuevo_estado = SolicitadoRevisionExperto()
        nuevo_cambio = CambioEstado(fecha_hora_cambio_estado, nuevo_estado, responsable)  
        evento.agregarCambioEstado(nuevo_cambio)
        evento.setEstadoActual(nuevo_estado)


    def volverAPendiente(self, evento, cambios_estado):
        """BloqueadoEnRevision -> Estado anterior (usa la instancia del historial previo si existe)."""
        # Buscar el cambio de estado anterior al bloqueo (el penúltimo cambio)
        cambios = evento.getCambioEstado()
        # Buscar el cambio actualmente activo y eliminarlo del historial
        for cambio_estado in list(cambios_estado):
            if cambio_estado.esEstadoActual() and cambio_estado.getFechaHoraFin() is None:
                cambios_estado.remove(cambio_estado)
                break

        # Ahora el último elemento del historial (si existe) representa el cambio
        # anterior del que queremos recuperar la instancia de Estado.
        if len(cambios_estado) == 0:
            raise ValueError("No existe un cambio de estado previo al que volver")

        ultimo_cambio = cambios_estado[-1]
        ultimo_cambio.setFechaHoraFin(None)
        ultimo_cambio.setResponsableInspeccion(None)
        # Asegurarse de pasar la instancia Estado, no el objeto CambioEstado entero
        evento.setEstadoActual(ultimo_cambio.getEstado())


class Confirmado(Estado):
    """Estado final cuando el evento es confirmado por el analista."""
    nombreEstado = "Confirmado"
    ambito = "EventoSismico"

    def esConfirmado(self):
        return True


class Rechazado(Estado):
    """Estado final cuando el evento es rechazado por el analista."""
    nombreEstado = "Rechazado"
    ambito = "EventoSismico"

    def esRechazado(self):
        return True


class SolicitadoRevisionExperto(Estado):
    """Estado cuando se solicita revisión de un experto externo."""
    nombreEstado = "SolicitadoRevisionExperto"
    ambito = "EventoSismico"

    def esSolicitadoRevisionExperto(self):
        return True