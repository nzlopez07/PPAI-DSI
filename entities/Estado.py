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
    def bloquear(self, evento):
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

    def bloquear(self, evento):
        """AutoDetectado -> BloqueadoEnRevision (cuando un analista selecciona el evento)"""
        from entities.Estado import BloqueadoEnRevision
        evento._transicionar_a(BloqueadoEnRevision())


class PendienteDeRevision(Estado):
    """Estado cuando un evento requiere revisión manual pero no está siendo procesado."""
    nombreEstado = "PendienteDeRevision"
    ambito = "EventoSismico"

    def esPendienteDeRevision(self):
        return True

    def bloquear(self, evento):
        """PendienteDeRevision -> BloqueadoEnRevision (cuando un analista selecciona el evento)"""
        from entities.Estado import BloqueadoEnRevision
        evento._transicionar_a(BloqueadoEnRevision())


class BloqueadoEnRevision(Estado):
    """Estado cuando un analista está revisando el evento (bloqueado para otros analistas)."""
    nombreEstado = "BloqueadoEnRevision"
    ambito = "EventoSismico"

    def esBloqueadoEnRevision(self):
        return True

    def confirmar(self, evento):
        """BloqueadoEnRevision -> Confirmado"""
        from entities.Estado import Confirmado
        evento._transicionar_a(Confirmado())

    def rechazar(self, evento):
        """BloqueadoEnRevision -> Rechazado"""
        from entities.Estado import Rechazado
        evento._transicionar_a(Rechazado())

    def solicitarRevisionExperto(self, evento):
        """BloqueadoEnRevision -> SolicitadoRevisionExperto"""
        from entities.Estado import SolicitadoRevisionExperto
        evento._transicionar_a(SolicitadoRevisionExperto())

    def volverAPendiente(self, evento):
        """BloqueadoEnRevision -> Estado anterior (usa la instancia del historial previo si existe)."""
        # Buscar el cambio de estado anterior al bloqueo (el penúltimo cambio)
        cambios = evento.getCambioEstado()
        if len(cambios) >= 2:
            # El último cambio es el bloqueo actual; el anterior contiene el estado previo
            cambio_anterior = cambios[-2]
            estado_previo = cambio_anterior.getEstado()
            evento._transicionar_a(estado_previo)
        else:
            # Si no hay historial suficiente, volver a AutoDetectado por defecto
            from entities.Estado import AutoDetectado
            evento._transicionar_a(AutoDetectado())


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