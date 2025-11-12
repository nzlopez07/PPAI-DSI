"""
Script de inicialización de la base de datos.

Este script:
1. Crea todas las tablas definidas en los modelos
2. Carga datos iniciales (catálogos, usuarios de prueba, etc.)
3. Migra los datos existentes en data.py si es necesario
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from database.config import engine, Base, SessionLocal
from database.models import (
    AlcanceSismoModel, ClasificacionSismoModel, MagnitudRichterModel,
    OrigenDeGeneracionModel, EmpleadoModel, UsuarioModel
)
from database.models import EstadoModel


def create_tables():
    """Crea todas las tablas en la base de datos."""
    print("🔨 Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


def load_catalogs(db):
    """Carga los datos de catálogo iniciales."""
    print("\n📚 Cargando catálogos...")
    
    # Alcances de Sismo
    alcances = [
        {"nombre": "Local", "descripcion": "Sismos que afectan áreas menores a 100 km del epicentro"},
        {"nombre": "Regional", "descripcion": "Sismos que afectan regiones de cientos de kilómetros"},
        {"nombre": "Lejano", "descripcion": "Sismos que pueden ser sentidos a miles de kilómetros"},
        {"nombre": "Muy Lejano", "descripcion": "Sismos detectados a escala global"}
    ]
    
    for alcance_data in alcances:
        if not db.query(AlcanceSismoModel).filter(AlcanceSismoModel.nombre == alcance_data["nombre"]).first():
            alcance = AlcanceSismoModel(**alcance_data)
            db.add(alcance)
    
    # Clasificaciones de Sismo (por profundidad)
    clasificaciones = [
        {"nombre": "Superficial", "km_profundidad_desde": 0, "km_profundidad_hasta": 70},
        {"nombre": "Intermedio", "km_profundidad_desde": 70, "km_profundidad_hasta": 300},
        {"nombre": "Profundo", "km_profundidad_desde": 300, "km_profundidad_hasta": 700}
    ]
    
    for clasif_data in clasificaciones:
        if not db.query(ClasificacionSismoModel).filter(ClasificacionSismoModel.nombre == clasif_data["nombre"]).first():
            clasificacion = ClasificacionSismoModel(**clasif_data)
            db.add(clasificacion)
    
    # Magnitudes Richter
    magnitudes = [
        {"numero": 1.0, "descripcion_magnitud": "Micro - No sentido, solo detectado por sismógrafos"},
        {"numero": 2.0, "descripcion_magnitud": "Menor - Sentido levemente por algunas personas"},
        {"numero": 3.0, "descripcion_magnitud": "Ligero - Sentido por personas en reposo"},
        {"numero": 4.0, "descripcion_magnitud": "Moderado - Sentido por la mayoría, objetos colgantes se balancean"},
        {"numero": 5.0, "descripcion_magnitud": "Fuerte - Sentido por todos, algunos daños menores"},
        {"numero": 6.0, "descripcion_magnitud": "Severo - Daños considerables en edificios mal construidos"},
        {"numero": 7.0, "descripcion_magnitud": "Mayor - Daño serio en áreas extensas"},
        {"numero": 8.0, "descripcion_magnitud": "Gran - Destrucción masiva en áreas extensas"},
        {"numero": 9.0, "descripcion_magnitud": "Catastrófico - Devastación total en áreas muy extensas"}
    ]
    
    for mag_data in magnitudes:
        if not db.query(MagnitudRichterModel).filter(MagnitudRichterModel.numero == mag_data["numero"]).first():
            magnitud = MagnitudRichterModel(**mag_data)
            db.add(magnitud)
    
    # Orígenes de Generación
    origenes = [
        {"nombre": "Tectónico", "descripcion": "Originado por movimiento de placas tectónicas"},
        {"nombre": "Volcánico", "descripcion": "Originado por actividad volcánica"},
        {"nombre": "Colapso", "descripcion": "Originado por colapso de cavernas o estructuras subterráneas"},
        {"nombre": "Explosión", "descripcion": "Originado por explosiones artificiales"},
        {"nombre": "Inducido", "descripcion": "Originado por actividades humanas (minería, represas)"}
    ]
    
    for origen_data in origenes:
        if not db.query(OrigenDeGeneracionModel).filter(OrigenDeGeneracionModel.nombre == origen_data["nombre"]).first():
            origen = OrigenDeGeneracionModel(**origen_data)
            db.add(origen)
    
    db.commit()
    print("✅ Catálogos cargados exitosamente")

    # Insertar/actualizar estados canónicos a partir de las subclases en entities.Estado
    print("\n📚 Cargando estados canónicos desde entidades de dominio...")
    import inspect
    import entities.Estado as estado_module

    # Buscar clases definidas en el módulo que heredan de Estado (excluyendo la clase base)
    estado_classes = [
        cls for name, cls in inspect.getmembers(estado_module, inspect.isclass)
        if issubclass(cls, estado_module.Estado) and cls is not estado_module.Estado
    ]

    for cls in estado_classes:
        # Nombre canónico en el código: preferir el atributo nombreEstado si existe
        nombre = getattr(cls, 'nombreEstado', cls.__name__)
        # Descripción: usar la docstring de la clase (strip) si existe
        desc = (cls.__doc__ or '').strip()

        existente = db.query(EstadoModel).filter(EstadoModel.nombre == nombre).first()
        if not existente:
            db.add(EstadoModel(nombre=nombre, descripcion=desc))
        else:
            # Actualizar descripción si difiere y docstring no está vacía
            if desc and (existente.descripcion or '').strip() != desc:
                existente.descripcion = desc

    db.commit()
    print("✅ Estados canónicos sincronizados desde entidades de dominio")


def load_test_users(db):
    """Carga usuarios de prueba."""
    print("\n👤 Cargando usuarios de prueba...")
    
    # Empleados de prueba
    empleados_data = [
        {
            "apellido": "González",
            "nombre": "Juan",
            "mail": "juan.gonzalez@sismologia.gov",
            "telefono": "+54 11 1234-5678"
        },
        {
            "apellido": "Rodríguez",
            "nombre": "María",
            "mail": "maria.rodriguez@sismologia.gov",
            "telefono": "+54 11 2345-6789"
        },
        {
            "apellido": "Pérez",
            "nombre": "Carlos",
            "mail": "carlos.perez@sismologia.gov",
            "telefono": "+54 11 3456-7890"
        }
    ]
    
    for emp_data in empleados_data:
        if not db.query(EmpleadoModel).filter(EmpleadoModel.mail == emp_data["mail"]).first():
            empleado = EmpleadoModel(**emp_data)
            db.add(empleado)
            db.flush()  # Para obtener el ID
            
            # Crear usuario asociado
            usuario_nombre = emp_data["nombre"].lower() + "." + emp_data["apellido"].lower()
            if not db.query(UsuarioModel).filter(UsuarioModel.nombre_usuario == usuario_nombre).first():
                usuario = UsuarioModel(
                    nombre_usuario=usuario_nombre,
                    contraseña="password123",  # En producción usar hashing
                    empleado_id=empleado.id
                )
                db.add(usuario)
    
    db.commit()
    print("✅ Usuarios de prueba cargados exitosamente")


def migrate_existing_data(db):
    """
    Migra datos existentes de data.py a la base de datos.
    Este es opcional y se ejecuta solo si se desea preservar datos de prueba existentes.
    """
    print("\n🔄 Verificando datos existentes en data.py...")
    
    try:
        from data import eventos_sismicos, usuarios
        
        print(f"   Encontrados {len(eventos_sismicos)} eventos sísmicos en data.py")
        print(f"   Encontrados {len(usuarios)} usuarios en data.py")
        
        # TODO: Implementar lógica de migración si es necesario
        # Por ahora solo informamos
        print("⚠️  Migración manual requerida - Revisar data.py para transferir datos")
        
    except ImportError:
        print("   No se encontró data.py o no contiene datos")


def main():
    """Función principal de inicialización."""
    print("=" * 60)
    print("  INICIALIZACIÓN DE BASE DE DATOS - SISTEMA SÍSMICO")
    print("=" * 60)
    
    # Crear tablas
    create_tables()
    
    # Obtener sesión de BD
    db = SessionLocal()
    
    try:
        # Cargar datos iniciales
        load_catalogs(db)
        load_test_users(db)
        
        # Opcional: Migrar datos existentes
        # migrate_existing_data(db)
        
        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("\n📝 Próximos pasos:")
        print("   1. Revisar las tablas creadas en la base de datos")
        print("   2. Ajustar el código de data.py para usar los repositorios")
        print("   3. Actualizar GestorRevisionEventoSismico para usar persistencia")
        print("   4. Ejecutar pruebas de integración")
        
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
