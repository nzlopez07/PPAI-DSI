"""
Modelos ORM de SQLAlchemy para el sistema de eventos sísmicos.

Este módulo define el mapeo objeto-relacional respetando el diagrama de clases
y las relaciones ya implementadas en las entidades del dominio.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
)
from sqlalchemy.orm import relationship
from database.config import Base


# ============================================================================
# TABLAS DE CATÁLOGO / MAESTROS
# ============================================================================

class AlcanceSismoModel(Base):
    """Tabla: alcances_sismo - Catálogo de alcances sísmicos (local, regional, etc.)"""
    __tablename__ = "alcances_sismo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    
    # Relación con EventoSismico
    eventos_sismicos = relationship("EventoSismicoModel", back_populates="alcance_sismo")


class ClasificacionSismoModel(Base):
    """Tabla: clasificaciones_sismo - Catálogo de clasificaciones según profundidad"""
    __tablename__ = "clasificaciones_sismo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    km_profundidad_desde = Column(Float, nullable=False)
    km_profundidad_hasta = Column(Float, nullable=False)
    
    # Relación con EventoSismico
    eventos_sismicos = relationship("EventoSismicoModel", back_populates="clasificacion")


class MagnitudRichterModel(Base):
    """Tabla: magnitudes_richter - Catálogo de escalas de magnitud"""
    __tablename__ = "magnitudes_richter"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Float, nullable=False, unique=True)
    descripcion_magnitud = Column(Text, nullable=True)
    
    # Relación con EventoSismico
    eventos_sismicos = relationship("EventoSismicoModel", back_populates="magnitud")


class OrigenDeGeneracionModel(Base):
    """Tabla: origenes_generacion - Catálogo de orígenes (tectónico, volcánico, etc.)"""
    __tablename__ = "origenes_generacion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    
    # Relación con EventoSismico
    eventos_sismicos = relationship("EventoSismicoModel", back_populates="origen_generacion")


class TipoDeDatoModel(Base):
    """Tabla: tipos_de_dato - Catálogo de tipos de datos medidos"""
    __tablename__ = "tipos_de_dato"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    denominacion = Column(String(100), nullable=False, unique=True)
    nombre_unidad_medida = Column(String(50), nullable=False)
    valor_umbral = Column(Float, nullable=True)


# ============================================================================
# TABLA DE ESTADOS (Nuevo)
# ============================================================================
class EstadoModel(Base):
    """Tabla: estados - Catálogo de estados del dominio (AutoDetectado, PendienteDeRevision, ...)

    Esta tabla permite normalizar los estados en BD y añadir metadatos por estado.
    """
    __tablename__ = "estados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    # Relaciones inversas (opcional)
    eventos_actuales = relationship("EventoSismicoModel", back_populates="estado_actual", foreign_keys='EventoSismicoModel.estado_actual_id')
    cambios = relationship("CambioEstadoModel", back_populates="estado", foreign_keys='CambioEstadoModel.estado_id')


# ============================================================================
# TABLAS DE USUARIOS Y SESIONES
# ============================================================================

class EmpleadoModel(Base):
    """Tabla: empleados - Empleados del sistema"""
    __tablename__ = "empleados"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    apellido = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    mail = Column(String(150), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    
    # Relación con Usuario
    usuario = relationship("UsuarioModel", back_populates="empleado", uselist=False)


class UsuarioModel(Base):
    """Tabla: usuarios - Usuarios del sistema"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    contraseña = Column(String(255), nullable=False)  # Debe hashearse en producción
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    
    # Relaciones
    empleado = relationship("EmpleadoModel", back_populates="usuario")
    sesiones = relationship("SesionModel", back_populates="usuario_activo")


class SesionModel(Base):
    """Tabla: sesiones - Sesiones activas/históricas de usuarios"""
    __tablename__ = "sesiones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relación con Usuario
    usuario_activo = relationship("UsuarioModel", back_populates="sesiones")


# ============================================================================
# TABLAS DE ESTACIONES Y SISMÓGRAFOS
# ============================================================================

class EstacionSismologicaModel(Base):
    """Tabla: estaciones_sismologicas - Estaciones de monitoreo"""
    __tablename__ = "estaciones_sismologicas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_estacion = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(150), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    documento_certificacion_adq = Column(String(255), nullable=True)
    nro_certificacion_adquisicion = Column(String(100), nullable=True)
    fecha_solicitud_certificacion = Column(DateTime, nullable=True)
    
    # Relación con Sismografo
    sismografos = relationship("SismografoModel", back_populates="estacion_sismologica")


class SismografoModel(Base):
    """Tabla: sismografos - Instrumentos de medición"""
    __tablename__ = "sismografos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    identificador_sismografo = Column(String(50), nullable=False, unique=True)
    nro_serie = Column(String(100), nullable=False)
    fecha_adquisicion = Column(DateTime, nullable=False)
    estacion_id = Column(Integer, ForeignKey("estaciones_sismologicas.id"), nullable=False)
    
    # Relaciones
    estacion_sismologica = relationship("EstacionSismologicaModel", back_populates="sismografos")
    series_temporales = relationship("SerieTemporalModel", back_populates="sismografo")


# ============================================================================
# TABLAS DE EVENTOS SÍSMICOS Y ESTADOS
# ============================================================================

class EventoSismicoModel(Base):
    """
    Tabla: eventos_sismicos - Eventos sísmicos registrados.
    
    Nota: El estadoActual se almacena como string del nombre de la clase concreta
    para poder reconstruir el objeto Estado correcto al hidratar desde BD.
    """
    __tablename__ = "eventos_sismicos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_ocurrencia = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=True)
    latitud_epicentro = Column(Float, nullable=False)
    longitud_epicentro = Column(Float, nullable=False)
    latitud_hipocentro = Column(Float, nullable=False)
    longitud_hipocentro = Column(Float, nullable=False)
    valor_magnitud = Column(Float, nullable=False)
    
    # FK a tabla estados (fuente de verdad tras migración)
    estado_actual_id = Column(Integer, ForeignKey("estados.id"), nullable=False)
    # Relación hacia EstadoModel (usada tras migración)
    estado_actual = relationship("EstadoModel", back_populates="eventos_actuales", foreign_keys=[estado_actual_id])
    
    # Foreign Keys
    clasificacion_id = Column(Integer, ForeignKey("clasificaciones_sismo.id"), nullable=False)
    magnitud_id = Column(Integer, ForeignKey("magnitudes_richter.id"), nullable=True)
    origen_generacion_id = Column(Integer, ForeignKey("origenes_generacion.id"), nullable=False)
    alcance_sismo_id = Column(Integer, ForeignKey("alcances_sismo.id"), nullable=False)
    
    # Relaciones
    clasificacion = relationship("ClasificacionSismoModel", back_populates="eventos_sismicos")
    magnitud = relationship("MagnitudRichterModel", back_populates="eventos_sismicos")
    origen_generacion = relationship("OrigenDeGeneracionModel", back_populates="eventos_sismicos")
    alcance_sismo = relationship("AlcanceSismoModel", back_populates="eventos_sismicos")
    
    # Relaciones con historial y series temporales
    cambios_estado = relationship(
        "CambioEstadoModel", 
        back_populates="evento_sismico",
        cascade="all, delete-orphan",
        order_by="CambioEstadoModel.fecha_hora_inicio.desc()"
    )
    series_temporales = relationship(
        "SerieTemporalModel",
        back_populates="evento_sismico",
        cascade="all, delete-orphan"
    )


class CambioEstadoModel(Base):
    """
    Tabla: cambios_estado - Historial de cambios de estado de eventos.
    
    Almacena el nombre de la clase Estado concreta y el responsable que realizó el cambio.
    """
    __tablename__ = "cambios_estado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_inicio = Column(DateTime, nullable=False)
    fecha_hora_fin = Column(DateTime, nullable=True)
    estado_id = Column(Integer, ForeignKey("estados.id"), nullable=False)
    evento_sismico_id = Column(Integer, ForeignKey("eventos_sismicos.id"), nullable=False)
    responsable_inspeccion_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    
    # Relaciones
    evento_sismico = relationship("EventoSismicoModel", back_populates="cambios_estado")
    responsable_inspeccion = relationship("EmpleadoModel")
    estado = relationship("EstadoModel", back_populates="cambios", foreign_keys=[estado_id])


# ============================================================================
# TABLAS DE SERIES TEMPORALES Y MUESTRAS
# ============================================================================

class SerieTemporalModel(Base):
    """Tabla: series_temporales - Series de tiempo de mediciones sísmicas"""
    __tablename__ = "series_temporales"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    condicion_alarma = Column(Boolean, nullable=False)
    fecha_hora_inicio_registro_muestras = Column(DateTime, nullable=False)
    fecha_hora_registro = Column(DateTime, nullable=False)
    frecuencia_muestreo = Column(Float, nullable=False)
    
    # Foreign Keys
    sismografo_id = Column(Integer, ForeignKey("sismografos.id"), nullable=False)
    evento_sismico_id = Column(Integer, ForeignKey("eventos_sismicos.id"), nullable=True)
    
    # Relaciones
    sismografo = relationship("SismografoModel", back_populates="series_temporales")
    evento_sismico = relationship("EventoSismicoModel", back_populates="series_temporales")
    muestras_sismicas = relationship(
        "MuestraSismicaModel",
        back_populates="serie_temporal",
        cascade="all, delete-orphan"
    )


class MuestraSismicaModel(Base):
    """Tabla: muestras_sismicas - Muestras individuales de datos sísmicos"""
    __tablename__ = "muestras_sismicas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora_muestra = Column(DateTime, nullable=False)
    serie_temporal_id = Column(Integer, ForeignKey("series_temporales.id"), nullable=False)
    
    # Relaciones
    serie_temporal = relationship("SerieTemporalModel", back_populates="muestras_sismicas")
    detalles_muestra = relationship(
        "DetalleMuestraSismicaModel",
        back_populates="muestra_sismica",
        cascade="all, delete-orphan"
    )


class DetalleMuestraSismicaModel(Base):
    """Tabla: detalles_muestra_sismica - Detalles de ondas sísmicas medidas"""
    __tablename__ = "detalles_muestra_sismica"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    velocidad_onda = Column(Float, nullable=False)
    frecuencia_onda = Column(Float, nullable=False)
    longitud_onda = Column(Float, nullable=False)
    muestra_sismica_id = Column(Integer, ForeignKey("muestras_sismicas.id"), nullable=False)
    
    # Relación con MuestraSismica
    muestra_sismica = relationship("MuestraSismicaModel", back_populates="detalles_muestra")
