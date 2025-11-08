# Capa de Persistencia con SQLAlchemy

## 📋 Contenido

- [Arquitectura](#arquitectura)
- [Modelos ORM](#modelos-orm)
- [Repositorios (Data Mapper)](#repositorios-data-mapper)
- [Configuración](#configuración)
- [Uso](#uso)
- [Manejo del Patrón State](#manejo-del-patrón-state)
- [Instalación](#instalación)

---

## 🏗️ Arquitectura

La capa de persistencia implementa el patrón **Data Mapper** para separar la lógica de dominio de la lógica de persistencia:

```
┌─────────────────────────────────────────────────────────┐
│                   CAPA DE DOMINIO                       │
│  (EventoSismico, Estado, CambioEstado, etc.)            │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ usa
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CAPA DE REPOSITORIOS                       │
│  EventoSismicoRepository, EmpleadoRepository            │
│  (Materialize / Desmaterialize)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ mapea
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 CAPA DE ORM                             │
│  EventoSismicoModel, CambioEstadoModel, etc.            │
│  (SQLAlchemy Models)                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ persiste
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  BASE DE DATOS                          │
│        (SQLite / PostgreSQL / MySQL)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modelos ORM

Los modelos ORM están en `database/models.py` y mapean la estructura del diagrama de clases:

### Jerarquía de Tablas

#### **Catálogos (Tablas Maestras)**
- `alcances_sismo` - Alcances sísmicos
- `clasificaciones_sismo` - Clasificaciones por profundidad
- `magnitudes_richter` - Escalas de magnitud
- `origenes_generacion` - Orígenes del evento
- `tipos_de_dato` - Tipos de datos medidos

#### **Usuarios y Sesiones**
- `empleados` - Empleados del sistema
- `usuarios` - Usuarios con credenciales
- `sesiones` - Sesiones activas/históricas

#### **Infraestructura Sísmica**
- `estaciones_sismologicas` - Estaciones de monitoreo
- `sismografos` - Instrumentos de medición

#### **Eventos y Estados**
- `eventos_sismicos` - Eventos sísmicos registrados
- `cambios_estado` - Historial de transiciones de estado

#### **Series Temporales y Mediciones**
- `series_temporales` - Series de tiempo
- `muestras_sismicas` - Muestras individuales
- `detalles_muestra_sismica` - Detalles de ondas

### Diagrama de Relaciones

```
eventos_sismicos
    ├── clasificaciones_sismo (Many-to-One)
    ├── magnitudes_richter (Many-to-One)
    ├── origenes_generacion (Many-to-One)
    ├── alcances_sismo (Many-to-One)
    ├── cambios_estado (One-to-Many, cascade)
    └── series_temporales (One-to-Many, cascade)

cambios_estado
    ├── eventos_sismicos (Many-to-One)
    └── empleados (Many-to-One) [responsable]

series_temporales
    ├── sismografos (Many-to-One)
    ├── eventos_sismicos (Many-to-One)
    └── muestras_sismicas (One-to-Many, cascade)

muestras_sismicas
    ├── series_temporales (Many-to-One)
    └── detalles_muestra_sismica (One-to-Many, cascade)
```

---

## 🗄️ Repositorios (Data Mapper)

Los repositorios están en `database/repositories.py` y encapsulan la lógica de persistencia.

### EventoSismicoRepository

```python
from database.config import SessionLocal
from database.repositories import EventoSismicoRepository

# Obtener sesión de BD
db = SessionLocal()

# Crear repositorio
repo = EventoSismicoRepository(db)

# OPERACIONES CRUD

# 1. Obtener evento por ID
evento = repo.get_by_id(evento_id=1)

# 2. Obtener eventos por estado
eventos_auto = repo.get_by_estado("AutoDetectado")
eventos_pendientes = repo.get_by_estado("PendienteDeRevision")

# 3. Obtener eventos AutoDetectados y PendientesDeRevision
eventos = repo.get_auto_detectados_y_pendientes()

# 4. Guardar evento (crear o actualizar)
repo.save(evento)

# 5. Eliminar evento
repo.delete(evento_id=1)
```

### EmpleadoRepository y UsuarioRepository

```python
from database.repositories import EmpleadoRepository, UsuarioRepository

# Empleados
empleado_repo = EmpleadoRepository(db)
empleado = empleado_repo.get_by_mail("juan.gonzalez@sismologia.gov")
empleado_repo.save(nuevo_empleado)

# Usuarios
usuario_repo = UsuarioRepository(db)
usuario = usuario_repo.get_by_nombre_usuario("juan.gonzalez")
usuario_repo.save(nuevo_usuario, empleado_mail="juan@mail.com")
```

---

## ⚙️ Configuración

### Archivo: `database/config.py`

```python
# URL de conexión (configurable vía variable de entorno)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eventos_sismicos.db")

# Para PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Para MySQL:
# DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
```

### Funciones de Utilidad

```python
from database.config import init_db, drop_all_tables

# Crear todas las tablas
init_db()

# Eliminar todas las tablas (CUIDADO!)
drop_all_tables()
```

---

## 🚀 Uso

### 1. Inicializar la Base de Datos

```bash
python database/init_db.py
```

Esto creará:
- ✅ Todas las tablas
- ✅ Datos de catálogo (alcances, clasificaciones, magnitudes, orígenes)
- ✅ Usuarios de prueba (juan.gonzalez, maria.rodriguez, carlos.perez)

### 2. Integrar en el Gestor

Modifica `controllers/GestorRevisionEventoSismico.py`:

```python
from database.config import SessionLocal
from database.repositories import EventoSismicoRepository

class GestorRevisionEventoSismico:
    def __init__(self, pantalla):
        self.pantallaRevision = pantalla
        
        # Inicializar repositorio
        self.db = SessionLocal()
        self.repo_eventos = EventoSismicoRepository(self.db)
        
        # Cargar eventos desde BD en lugar de data.py
        self.eventosSismicosAutoDetectados = (
            self.repo_eventos.get_auto_detectados_y_pendientes()
        )
        
        # ... resto del código
    
    def opcRegistrarResultadoRevisionManual(self):
        # Obtener eventos desde BD
        eventos = self.repo_eventos.get_auto_detectados_y_pendientes()
        
        if not eventos:
            return None
        
        # ... resto de la lógica
        
        return self.pantallaRevision.mostrarEventosParaSeleccion(eventos)
    
    def rechazarEventoSismico(self):
        # ... lógica de rechazo
        
        # IMPORTANTE: Guardar cambios en BD
        self.repo_eventos.save(self.eventoSismicoSeleccionado)
        
        # ... resto del código
```

### 3. Cerrar Sesión al Finalizar

```python
# En Flask, puedes usar un contexto:
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.close()

# O manualmente:
gestor.db.close()
```

---

## 🎭 Manejo del Patrón State

El patrón State presenta un desafío para la persistencia porque SQLAlchemy no puede mapear polimorfismo de forma directa. La solución implementada:

### 1. Almacenar el Nombre de la Clase

En la tabla `eventos_sismicos`:
```python
estado_actual_nombre = Column(String(100), nullable=False)
# Valores: "AutoDetectado", "BloqueadoEnRevision", "Confirmado", etc.
```

En la tabla `cambios_estado`:
```python
estado_nombre = Column(String(100), nullable=False)
# Mismo formato que arriba
```

### 2. Mapeo Bidireccional

En `repositories.py`:

```python
ESTADO_CLASS_MAP = {
    "AutoDetectado": AutoDetectado,
    "PendienteDeRevision": PendienteDeRevision,
    "BloqueadoEnRevision": BloqueadoEnRevision,
    "Confirmado": Confirmado,
    "Rechazado": Rechazado,
    "SolicitadoRevisionExperto": SolicitadoRevisionExperto
}

# Convertir nombre → instancia
def nombre_estado_to_instance(nombre_clase: str):
    estado_class = ESTADO_CLASS_MAP.get(nombre_clase)
    return estado_class()

# Convertir instancia → nombre
def instance_to_nombre_estado(estado_instance) -> str:
    return estado_instance.__class__.__name__
```

### 3. Flujo de Persistencia

**Al guardar:**
```python
evento_model.estado_actual_nombre = "BloqueadoEnRevision"
# Se guarda solo el string, no el objeto
```

**Al cargar:**
```python
estado_actual = nombre_estado_to_instance(evento_model.estado_actual_nombre)
# Se reconstruye el objeto Estado concreto
```

### 4. Ventajas de esta Solución

✅ Simple y directa
✅ No requiere herencia en SQLAlchemy
✅ Fácil de debuggear (puedes ver el estado en SQL)
✅ No rompe el patrón State en el dominio
✅ Compatible con cualquier base de datos

---

## 📦 Instalación

### 1. Instalar SQLAlchemy

```bash
pip install sqlalchemy
```

### 2. Instalar Driver de Base de Datos

**SQLite (incluido en Python):**
```bash
# No requiere instalación adicional
```

**PostgreSQL:**
```bash
pip install psycopg2-binary
```

**MySQL:**
```bash
pip install pymysql
```

### 3. Configurar Variable de Entorno (Opcional)

```bash
# Linux/Mac
export DATABASE_URL="postgresql://user:password@localhost/eventos_sismicos"

# Windows (PowerShell)
$env:DATABASE_URL="postgresql://user:password@localhost/eventos_sismicos"
```

### 4. Inicializar Base de Datos

```bash
python database/init_db.py
```

---

## 🔍 Ejemplo Completo de Uso

```python
from datetime import datetime
from database.config import SessionLocal, init_db
from database.repositories import EventoSismicoRepository
from entities.EventoSismico import EventoSismico
from entities.Estado import AutoDetectado, BloqueadoEnRevision
from entities.CambioEstado import CambioEstado
from entities.AlcanceSismo import AlcanceSismo
from entities.ClasificacionSismo import ClasificacionSismo
from entities.MagnitudRichter import MagnitudRichter
from entities.OrigenDeGeneracion import OrigenDeGeneracion

# 1. Inicializar BD (solo la primera vez)
init_db()

# 2. Crear sesión
db = SessionLocal()
repo = EventoSismicoRepository(db)

# 3. Crear nuevo evento
evento = EventoSismico(
    clasificacion=ClasificacionSismo(0, 70, "Superficial"),
    magnitud=MagnitudRichter("Moderado", 4.5),
    origenGeneracion=OrigenDeGeneracion("Tectónico", "Placas"),
    alcanceSismo=AlcanceSismo("Local", "Local"),
    estadoActual=AutoDetectado(),
    cambiosEstado=[
        CambioEstado(datetime.now(), AutoDetectado(), None)
    ],
    serieTemporal=[],
    fechaHoraOcurrencia=datetime.now(),
    latitudEpicentro=-34.6037,
    latitudHipocentro=-34.6037,
    longitudEpicentro=-58.3816,
    longitudHipocentro=-58.3816,
    valorMagnitud=4.5
)

# 4. Guardar en BD
repo.save(evento)
print(f"✅ Evento guardado con ID: {evento._db_id}")

# 5. Recuperar desde BD
evento_recuperado = repo.get_by_id(evento._db_id)
print(f"Estado actual: {evento_recuperado.estadoActual.nombreEstado}")

# 6. Transicionar de estado
evento_recuperado.bloquearEventoRevision()

# 7. Actualizar en BD
repo.save(evento_recuperado)
print("✅ Evento actualizado con nuevo estado")

# 8. Listar eventos AutoDetectados
eventos_auto = repo.get_by_estado("AutoDetectado")
print(f"📋 Eventos AutoDetectados: {len(eventos_auto)}")

# 9. Cerrar sesión
db.close()
```

---

## 🐛 Troubleshooting

### Error: `No module named 'sqlalchemy'`
```bash
pip install sqlalchemy
```

### Error: `no such table: eventos_sismicos`
```bash
python database/init_db.py
```

### Error: `database is locked` (SQLite)
- SQLite no soporta escrituras concurrentes
- Considera migrar a PostgreSQL para producción

### Error: `Foreign key constraint failed`
- Asegúrate de que los catálogos existan (ejecuta `init_db.py`)
- Verifica que los empleados existan antes de crear usuarios

---

## 📝 Próximos Pasos

1. ✅ Integrar repositorios en `GestorRevisionEventoSismico`
2. ✅ Reemplazar `data.py` por consultas a BD
3. ✅ Agregar pruebas unitarias de repositorios
4. ⬜ Implementar migrations con Alembic
5. ⬜ Agregar índices para optimización de consultas
6. ⬜ Implementar caché con Redis (opcional)
7. ⬜ Migrar a PostgreSQL para producción

---

## 📚 Referencias

- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [Data Mapper Pattern](https://martinfowler.com/eaaCatalog/dataMapper.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

**Autor:** Sistema de Monitoreo Sísmico - DSI 2025
**Fecha:** Noviembre 2025
