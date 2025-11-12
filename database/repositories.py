"""
Repositorios para acceso a datos - Patrón Data Mapper

Los repositorios encapsulan la lógica de persistencia y proporcionan métodos
para materializar (cargar desde BD) y desmaterializar (guardar en BD) las entidades
del dominio.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from database.models import (
    EventoSismicoModel, CambioEstadoModel, AlcanceSismoModel,
    ClasificacionSismoModel, MagnitudRichterModel, OrigenDeGeneracionModel,
    EmpleadoModel, UsuarioModel, SesionModel,
    SerieTemporalModel, SismografoModel
)
from entities.EventoSismico import EventoSismico
from entities.CambioEstado import CambioEstado
from entities.AlcanceSismo import AlcanceSismo
from entities.ClasificacionSismo import ClasificacionSismo
from entities.MagnitudRichter import MagnitudRichter
from entities.OrigenDeGeneracion import OrigenDeGeneracion
from entities.Estado import (
    AutoDetectado, PendienteDeRevision, BloqueadoEnRevision,
    Confirmado, Rechazado, SolicitadoRevisionExperto
)
from entities.Empleado import Empleado
from entities.Usuario import Usuario
from entities.Sesion import Sesion


# ============================================================================
# MAPEO DE ESTADOS: Nombre de clase <-> Instancia de Estado
# ============================================================================

ESTADO_CLASS_MAP = {
    "AutoDetectado": AutoDetectado,
    "PendienteDeRevision": PendienteDeRevision,
    "BloqueadoEnRevision": BloqueadoEnRevision,
    "Confirmado": Confirmado,
    "Rechazado": Rechazado,
    "SolicitadoRevisionExperto": SolicitadoRevisionExperto
}


def nombre_estado_to_instance(nombre_clase: str):
    """Convierte el nombre de clase de Estado a una instancia concreta."""
    estado_class = ESTADO_CLASS_MAP.get(nombre_clase)
    if estado_class is None:
        raise ValueError(f"Estado desconocido: {nombre_clase}")
    return estado_class()


def instance_to_nombre_estado(estado_instance) -> str:
    """Extrae el nombre de la clase del estado actual."""
    return estado_instance.__class__.__name__


def _ensure_estado_instance(maybe_estado):
    """Normaliza un valor que representa un Estado y retorna una instancia de Estado.

    Acepta:
    - una instancia de Estado -> se retorna tal cual
    - una instancia de CambioEstado -> se retorna cambio.getEstado()
    - una cadena con el nombre de la clase -> se crea la instancia correspondiente
    """
    # Caso: ya es instancia de Estado (tiene getNombreEstado)
    if hasattr(maybe_estado, 'getNombreEstado'):
        return maybe_estado

    # Caso: es un CambioEstado accidentalmente pasado
    if isinstance(maybe_estado, CambioEstado):
        return maybe_estado.getEstado()

    # Caso: es un nombre de clase
    if isinstance(maybe_estado, str):
        return nombre_estado_to_instance(maybe_estado)

    # No sabemos cómo normalizarlo
    raise ValueError(f"No se pudo normalizar el estado: {type(maybe_estado)} -> {maybe_estado}")


# ============================================================================
# REPOSITORIO DE EVENTOS SÍSMICOS
# ============================================================================

class EventoSismicoRepository:
    """
    Repositorio para EventoSismico.
    Implementa el patrón Data Mapper para separar la lógica de persistencia.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, evento_id: int) -> Optional[EventoSismico]:
        """
        Obtiene un evento sísmico por su ID y lo materializa a objeto de dominio.
        """
        evento_model = self.db.query(EventoSismicoModel).filter(
            EventoSismicoModel.id == evento_id
        ).first()
        
        if not evento_model:
            return None
        
        return self._materialize(evento_model)
    
    def get_by_estado(self, nombre_estado: str) -> List[EventoSismico]:
        """
        Obtiene todos los eventos sísmicos en un estado específico.
        
        Args:
            nombre_estado: Nombre de la clase Estado (ej: "AutoDetectado", "PendienteDeRevision")
        """
        eventos_model = self.db.query(EventoSismicoModel).filter(
            EventoSismicoModel.estado_actual_nombre == nombre_estado
        ).all()
        
        return [self._materialize(em) for em in eventos_model]
    
    def get_auto_detectados_y_pendientes(self) -> List[EventoSismico]:
        """
        Obtiene eventos en estado AutoDetectado o PendienteDeRevision.
        """
        eventos_model = self.db.query(EventoSismicoModel).filter(
            EventoSismicoModel.estado_actual_nombre.in_([
                "AutoDetectado",
                "PendienteDeRevision"
            ])
        ).all()
        
        return [self._materialize(em) for em in eventos_model]
    
    def save(self, evento: EventoSismico) -> EventoSismico:
        """
        Guarda (crea o actualiza) un evento sísmico en la base de datos.
        """
        # Si el evento tiene un atributo _db_id, es una actualización
        if hasattr(evento, '_db_id') and evento._db_id:
            evento_model = self.db.query(EventoSismicoModel).filter(
                EventoSismicoModel.id == evento._db_id
            ).first()
            
            if evento_model:
                self._update_model(evento_model, evento)
            else:
                raise ValueError(f"Evento con ID {evento._db_id} no encontrado")
        else:
            # Crear nuevo evento
            evento_model = self._create_model(evento)
            self.db.add(evento_model)
        
        self.db.commit()
        self.db.refresh(evento_model)
        
        # Actualizar el ID en el objeto de dominio
        evento._db_id = evento_model.id
        
        return evento
    
    def delete(self, evento_id: int) -> bool:
        """Elimina un evento sísmico por su ID."""
        evento_model = self.db.query(EventoSismicoModel).filter(
            EventoSismicoModel.id == evento_id
        ).first()
        
        if not evento_model:
            return False
        
        self.db.delete(evento_model)
        self.db.commit()
        return True

    def get_datos_evento_por_estacion(self, evento_id: int) -> dict:
        """Devuelve datos agregados de series/muestras/detalles por estación para un evento.
        Estructura: { nombreEstacion: [ {fechaHoraMuestra, frecuenciaOnda, longitudOnda, velocidadOnda}, ... ] }
        """
        datos_por_estacion: dict[str, list[dict]] = {}
        # Buscar todas las series del evento
        series_models = self.db.query(SerieTemporalModel).filter(
            SerieTemporalModel.evento_sismico_id == evento_id
        ).all()
        
        for serie in series_models:
            # Resolver estación a través del sismógrafo
            sismografo = self.db.query(SismografoModel).filter(
                SismografoModel.id == serie.sismografo_id
            ).first()
            if sismografo and sismografo.estacion_sismologica:
                nombre_estacion = sismografo.estacion_sismologica.nombre
            else:
                nombre_estacion = "Estación Desconocida"
            
            lista = datos_por_estacion.setdefault(nombre_estacion, [])
            
            for muestra in serie.muestras_sismicas:
                if muestra.detalles_muestra:
                    detalle = muestra.detalles_muestra[0]
                    lista.append({
                        "fechaHoraMuestra": muestra.fecha_hora_muestra,
                        "frecuenciaOnda": detalle.frecuencia_onda,
                        "longitudOnda": detalle.longitud_onda,
                        "velocidadOnda": detalle.velocidad_onda,
                    })
        return datos_por_estacion
    
    # ========================================================================
    # MÉTODOS PRIVADOS DE MAPEO
    # ========================================================================
    
    def _materialize(self, evento_model: EventoSismicoModel) -> EventoSismico:
        """
        Materializa un EventoSismicoModel a un objeto EventoSismico de dominio.
        """
        # Materializar objetos relacionados (catálogos)
        alcance = AlcanceSismo(
            evento_model.alcance_sismo.nombre,
            evento_model.alcance_sismo.descripcion
        )
        
        clasificacion = ClasificacionSismo(
            evento_model.clasificacion.km_profundidad_desde,
            evento_model.clasificacion.km_profundidad_hasta,
            evento_model.clasificacion.nombre
        )
        
        magnitud = MagnitudRichter(
            evento_model.magnitud.descripcion_magnitud,
            evento_model.magnitud.numero
        )
        
        origen = OrigenDeGeneracion(
            evento_model.origen_generacion.nombre,
            evento_model.origen_generacion.descripcion
        )
        
        # Reconstruir el estado actual desde el nombre de clase
        estado_actual = nombre_estado_to_instance(evento_model.estado_actual_nombre)
        
        # Materializar el historial de cambios de estado
        cambios_estado = []
        for cambio_model in evento_model.cambios_estado:
            estado_cambio = nombre_estado_to_instance(cambio_model.estado_nombre)
            
            # Materializar responsable si existe
            responsable = None
            if cambio_model.responsable_inspeccion:
                responsable = Empleado(
                    cambio_model.responsable_inspeccion.apellido,
                    cambio_model.responsable_inspeccion.mail,
                    cambio_model.responsable_inspeccion.nombre,
                    cambio_model.responsable_inspeccion.telefono
                )
            
            cambio = CambioEstado(
                cambio_model.fecha_hora_inicio,
                estado_cambio,
                responsable,
                cambio_model.fecha_hora_fin
            )
            cambio._db_id = cambio_model.id
            cambios_estado.append(cambio)
        
        # Por ahora series temporales vacías (TODO: implementar si es necesario)
        series_temporales = []
        
        # Crear el objeto de dominio EventoSismico
        evento = EventoSismico(
            clasificacion=clasificacion,
            magnitud=magnitud,
            origenGeneracion=origen,
            alcanceSismo=alcance,
            estadoActual=estado_actual,
            cambiosEstado=cambios_estado,
            serieTemporal=series_temporales,
            fechaHoraOcurrencia=evento_model.fecha_hora_ocurrencia,
            latitudEpicentro=evento_model.latitud_epicentro,
            latitudHipocentro=evento_model.latitud_hipocentro,
            longitudEpicentro=evento_model.longitud_epicentro,
            longitudHipocentro=evento_model.longitud_hipocentro,
            valorMagnitud=evento_model.valor_magnitud,
            fechaHoraFin=evento_model.fecha_hora_fin
        )
        
        # Guardar el ID de BD en el objeto de dominio
        evento._db_id = evento_model.id
        
        return evento
    
    def _create_model(self, evento: EventoSismico) -> EventoSismicoModel:
        """
        Crea un EventoSismicoModel a partir de un objeto EventoSismico de dominio.
        """
        # Buscar o crear los catálogos relacionados
        alcance_id = self._get_or_create_alcance(evento.alcanceSismo)
        clasificacion_id = self._get_or_create_clasificacion(evento.clasificacion)
        magnitud_id = self._get_or_create_magnitud(evento.magnitud, evento.valorMagnitud)
        origen_id = self._get_or_create_origen(evento.origenGeneracion)
        
        # Crear el modelo de evento
        # Normalizar estadoActual a una instancia de Estado si vino mal formado
        estado_actual_inst = _ensure_estado_instance(evento.estadoActual)

        evento_model = EventoSismicoModel(
            fecha_hora_ocurrencia=evento.fechaHoraOcurrencia,
            fecha_hora_fin=evento.fechaHoraFin,
            latitud_epicentro=evento.latitudEpicentro,
            longitud_epicentro=evento.longitudEpicentro,
            latitud_hipocentro=evento.latitudHipocentro,
            longitud_hipocentro=evento.longitudHipocentro,
            valor_magnitud=evento.valorMagnitud,
            estado_actual_nombre=instance_to_nombre_estado(estado_actual_inst),
            alcance_sismo_id=alcance_id,
            clasificacion_id=clasificacion_id,
            magnitud_id=magnitud_id,
            origen_generacion_id=origen_id
        )
        
        # Crear los cambios de estado asociados
        for cambio in evento.cambioEstado:
            responsable_id = None
            if cambio.responsableInspeccion:
                # Buscar empleado por mail (debe existir previamente)
                empleado_model = self.db.query(EmpleadoModel).filter(
                    EmpleadoModel.mail == cambio.responsableInspeccion.getMail()
                ).first()
                if empleado_model:
                    responsable_id = empleado_model.id
            # Normalizar el estado almacenado en el CambioEstado por seguridad
            try:
                estado_for_model = _ensure_estado_instance(cambio.estado)
            except ValueError:
                # Si no se puede normalizar, fallar con claridad
                raise

            cambio_model = CambioEstadoModel(
                fecha_hora_inicio=cambio.fechaHoraInicio,
                fecha_hora_fin=cambio.fechaHoraFin,
                estado_nombre=instance_to_nombre_estado(estado_for_model),
                responsable_inspeccion_id=responsable_id
            )
            evento_model.cambios_estado.append(cambio_model)
        
        return evento_model
    
    def _update_model(self, evento_model: EventoSismicoModel, evento: EventoSismico):
        """
        Actualiza un EventoSismicoModel existente con los datos de un EventoSismico.
        """
        # Actualizar datos básicos
        evento_model.fecha_hora_ocurrencia = evento.fechaHoraOcurrencia
        evento_model.fecha_hora_fin = evento.fechaHoraFin
        evento_model.latitud_epicentro = evento.latitudEpicentro
        evento_model.longitud_epicentro = evento.longitudEpicentro
        evento_model.latitud_hipocentro = evento.latitudHipocentro
        evento_model.longitud_hipocentro = evento.longitudHipocentro
        evento_model.valor_magnitud = evento.valorMagnitud
        # Normalizar estadoActual antes de obtener su nombre de clase
        estado_actual_inst = _ensure_estado_instance(evento.estadoActual)
        evento_model.estado_actual_nombre = instance_to_nombre_estado(estado_actual_inst)
        
        # Actualizar referencias a catálogos
        evento_model.alcance_sismo_id = self._get_or_create_alcance(evento.alcanceSismo)
        evento_model.clasificacion_id = self._get_or_create_clasificacion(evento.clasificacion)
        evento_model.magnitud_id = self._get_or_create_magnitud(evento.magnitud, evento.valorMagnitud)
        evento_model.origen_generacion_id = self._get_or_create_origen(evento.origenGeneracion)
        
        # Sincronizar cambios de estado (borrar los antiguos y crear los nuevos)
        # Esto es simplificado; una solución más compleja compararía diferencias
        self.db.query(CambioEstadoModel).filter(
            CambioEstadoModel.evento_sismico_id == evento_model.id
        ).delete()
        
        for cambio in evento.cambioEstado:
            responsable_id = None
            if cambio.responsableInspeccion:
                empleado_model = self.db.query(EmpleadoModel).filter(
                    EmpleadoModel.mail == cambio.responsableInspeccion.getMail()
                ).first()
                if empleado_model:
                    responsable_id = empleado_model.id
            # Normalizar estado del cambio
            estado_for_model = _ensure_estado_instance(cambio.estado)

            cambio_model = CambioEstadoModel(
                fecha_hora_inicio=cambio.fechaHoraInicio,
                fecha_hora_fin=cambio.fechaHoraFin,
                estado_nombre=instance_to_nombre_estado(estado_for_model),
                evento_sismico_id=evento_model.id,
                responsable_inspeccion_id=responsable_id
            )
            self.db.add(cambio_model)
    
    # ========================================================================
    # HELPERS PARA CATÁLOGOS (GET OR CREATE)
    # ========================================================================
    
    def _get_or_create_alcance(self, alcance: AlcanceSismo) -> int:
        """Obtiene o crea un AlcanceSismo y retorna su ID."""
        alcance_model = self.db.query(AlcanceSismoModel).filter(
            AlcanceSismoModel.nombre == alcance.nombre
        ).first()
        
        if not alcance_model:
            alcance_model = AlcanceSismoModel(
                nombre=alcance.nombre,
                descripcion=alcance.descripcion
            )
            self.db.add(alcance_model)
            self.db.flush()
        
        return alcance_model.id
    
    def _get_or_create_clasificacion(self, clasificacion: ClasificacionSismo) -> int:
        """Obtiene o crea una ClasificacionSismo y retorna su ID."""
        clasificacion_model = self.db.query(ClasificacionSismoModel).filter(
            ClasificacionSismoModel.nombre == clasificacion.nombre
        ).first()
        
        if not clasificacion_model:
            clasificacion_model = ClasificacionSismoModel(
                nombre=clasificacion.nombre,
                km_profundidad_desde=clasificacion.kmProfundidadDesde,
                km_profundidad_hasta=clasificacion.kmProfunidadHasta
            )
            self.db.add(clasificacion_model)
            self.db.flush()
        
        return clasificacion_model.id
    
    def _get_or_create_magnitud(self, magnitud: MagnitudRichter, valor_magnitud: float = None) -> Optional[int]:
        """
        Obtiene o crea una MagnitudRichter y retorna su ID. 
        Si magnitud es None, usa valor_magnitud para buscar la magnitud más cercana.
        Retorna None si ambos son None.
        """
        if magnitud is None and valor_magnitud is None:
            return None
        
        # Si tenemos el objeto magnitud, úsalo
        if magnitud is not None:
            magnitud_model = self.db.query(MagnitudRichterModel).filter(
                MagnitudRichterModel.numero == magnitud.numero
            ).first()
            
            if not magnitud_model:
                magnitud_model = MagnitudRichterModel(
                    numero=magnitud.numero,
                    descripcion_magnitud=magnitud.descripcionMagnitud
                )
                self.db.add(magnitud_model)
                self.db.flush()
            
            return magnitud_model.id
        
        # Si solo tenemos valor_magnitud, buscar la magnitud más cercana (redondeando)
        import math
        magnitud_redondeada = math.floor(valor_magnitud) if valor_magnitud < 1.0 else round(valor_magnitud)
        
        magnitud_model = self.db.query(MagnitudRichterModel).filter(
            MagnitudRichterModel.numero == magnitud_redondeada
        ).first()
        
        if not magnitud_model:
            # Si no existe, crear una nueva magnitud
            magnitud_model = MagnitudRichterModel(
                numero=magnitud_redondeada,
                descripcion_magnitud=f"Magnitud {magnitud_redondeada}"
            )
            self.db.add(magnitud_model)
            self.db.flush()
        
        return magnitud_model.id
    
    def _get_or_create_origen(self, origen: OrigenDeGeneracion) -> int:
        """Obtiene o crea un OrigenDeGeneracion y retorna su ID."""
        origen_model = self.db.query(OrigenDeGeneracionModel).filter(
            OrigenDeGeneracionModel.nombre == origen.nombre
        ).first()
        
        if not origen_model:
            origen_model = OrigenDeGeneracionModel(
                nombre=origen.nombre,
                descripcion=origen.descripcion
            )
            self.db.add(origen_model)
            self.db.flush()
        
        return origen_model.id


# ============================================================================
# REPOSITORIO DE EMPLEADOS Y USUARIOS
# ============================================================================

class EmpleadoRepository:
    """Repositorio para Empleados."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_mail(self, mail: str) -> Optional[Empleado]:
        """Obtiene un empleado por su correo electrónico."""
        empleado_model = self.db.query(EmpleadoModel).filter(
            EmpleadoModel.mail == mail
        ).first()
        
        if not empleado_model:
            return None
        
        return Empleado(
            empleado_model.apellido,
            empleado_model.mail,
            empleado_model.nombre,
            empleado_model.telefono
        )
    
    def save(self, empleado: Empleado) -> Empleado:
        """Guarda un empleado en la base de datos."""
        empleado_model = EmpleadoModel(
            apellido=empleado._Empleado__apellido,
            nombre=empleado._Empleado__nombre,
            mail=empleado._Empleado__mail,
            telefono=empleado._Empleado__telefono
        )
        self.db.add(empleado_model)
        self.db.commit()
        self.db.refresh(empleado_model)
        
        return empleado


class UsuarioRepository:
    """Repositorio para Usuarios."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, nombre_usuario: str) -> Optional[Usuario]:
        """Alias de get_by_nombre_usuario para compatibilidad con código existente."""
        return self.get_by_nombre_usuario(nombre_usuario)
    
    def get_by_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario."""
        usuario_model = self.db.query(UsuarioModel).filter(
            UsuarioModel.nombre_usuario == nombre_usuario
        ).first()
        
        if not usuario_model:
            return None
        
        # Materializar el empleado asociado
        empleado = Empleado(
            usuario_model.empleado.apellido,
            usuario_model.empleado.mail,
            usuario_model.empleado.nombre,
            usuario_model.empleado.telefono
        )
        
        return Usuario(
            usuario_model.contraseña,
            usuario_model.nombre_usuario,
            empleado
        )
    
    def save(self, usuario: Usuario, empleado_mail: str) -> Usuario:
        """Guarda un usuario en la base de datos."""
        # Buscar el empleado asociado
        empleado_model = self.db.query(EmpleadoModel).filter(
            EmpleadoModel.mail == empleado_mail
        ).first()
        
        if not empleado_model:
            raise ValueError(f"Empleado con mail {empleado_mail} no encontrado")
        
        usuario_model = UsuarioModel(
            nombre_usuario=usuario._Usuario__nombreUsuario,
            contraseña=usuario._Usuario__contraseña,
            empleado_id=empleado_model.id
        )
        self.db.add(usuario_model)
        self.db.commit()
        self.db.refresh(usuario_model)
        
        return usuario
