# Análisis comparativo: Diagrama de secuencia vs Código

- Proyecto: PPAI_Copia
- Fecha: 2025-10-16
- Diagrama base: `PPAI - Realización CU Registrar resultado de revisión manual-Diag de secuencia.drawio.pdf`

## 🎯 Resumen del Caso de Uso

- Nombre: Registrar Resultado de Revisión Manual de Evento Sísmico
- Actor Principal: Empleado Revisor
- Descripción: El sistema permite seleccionar un evento autodetectado/pendiente, bloquearlo, visualizar sus datos y registrar un resultado (rechazar/confirmar/solicitar experto) con traza de cambios de estado.

## 🗂️ Estructura del Proyecto (relevante)

- `interface/PantallaRevisionEventoSismico.py` (Boundary)
- `controllers/GestorRevisionEventoSismico.py` (Control)
- `entities/*` (Entity): `EventoSismico`, `Estado`, `CambioEstado`, `SerieTemporal`, `MuestraSismica`, `DetalleMuestraSismica`, `AlcanceSismo`, `ClasificacionSismo`, `OrigenDeGeneracion`, `Sismografo`, `EstacionSismologica`, `Usuario`, `Empleado`, `Sesion`
- `main.py` (Flask - endpoints)

---

## 🔁 Comparación 1 a 1 por fases

### Fase 1: Inicio del caso de uso

| # | Mensaje (Diagrama) | Método (Código) | Clase | Estado |
|---|---|---|---|---|
| 1 | opcRegistrarResultadoRevisionManual() | opcRegistrarResultadoRevisionManual() | PantallaRevisionEventoSismico | ✅ |
| 2 | habilitarPantalla() | habilitarPantalla() | PantallaRevisionEventoSismico | ✅ |
| 3 | new GestorRevisionEventoSismico | GestorRevisionEventoSismico(self) | PantallaRevisionEventoSismico | ✅ |
| 4 | opcRegistrarResultadoRevisionManual() | opcRegistrarResultadoRevisionManual() | GestorRevisionEventoSismico | ✅ |
| 5 | obtenerUsuarioLogueado() | obtenerUsuarioLogueado() | GestorRevisionEventoSismico | ✅ |
| 6 | getUsuarioActivo() | getUsuarioActivo() | Sesion | ✅ |
| 7 | getEmpleado() | getEmpleado() | Usuario | ✅ |

### Fase 2: Búsqueda y filtrado de eventos

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 8 | buscarEventosAutoDetectados() | buscarEventosAutoDetectados() | GestorRevisionEventoSismico | ✅ |
| 9 | Loop eventos | for evento in eventos_mock | GestorRevisionEventoSismico | ✅ |
| 10 | estaAutoDetectado() | estaAutoDetectado() | EventoSismico | ✅ |
| 11 | esAutoDetectado() | esAutoDetectado() | Estado | ✅ |
| 12 | estaPendienteDeRevision() | estaPendienteDeRevision() | EventoSismico | ✅ |
| 13 | esPendienteDeRevision() | esPendienteDeRevision() | Estado | ✅ |
| 14 | ordenarPorFechaYHora() | ordenarPorFechaYHora() | GestorRevisionEventoSismico | ✅ |
| 15 | mostrarYSolicitarSeleccionEvento() | mostrarYSolicitarSeleccionEvento() | PantallaRevisionEventoSismico | ✅ |

### Fase 3: Selección y bloqueo de evento

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 16 | tomarSeleccionEvento() | tomarSeleccionEvento(indice) | PantallaRevisionEventoSismico | ✅ |
| 17 | tomarSeleccionEvento() | tomarSeleccionEvento(evento) | GestorRevisionEventoSismico | ✅ |
| 18 | bloquearEventoSismico() | bloquearEventoSismico() | GestorRevisionEventoSismico | ✅ |
| 19 | Loop estados | for estado in estados_mock | GestorRevisionEventoSismico | ✅ |
| 20 | esAmbito() | esAmbitoEventoSismico() | Estado | ⚠️ nombre distinto |
| 21 | esBloqueadoEnRevision() | esBloqueadoEnRevision() | Estado | ✅ |
| 22 | obtenerEstadoActual() | obtenerEstadoActual() | EventoSismico | ✅ |
| 23 | esEstadoActual() | esEstadoActual() | CambioEstado | ✅ |
| 24 | calcularFechaHoraActual() | calcularFechaHoraActual() | GestorRevisionEventoSismico | ✅ |
| 25 | setEstadoActual() | setEstadoActual() | EventoSismico | ✅ |
| 26 | bloquearEnRevision() | bloquearEnRevision() | EventoSismico | ✅ |
| 27 | setFechaHoraFin() | setFechaHoraFin() | CambioEstado | ✅ |
| 28 | setResponsableInspeccion() | setResponsableInspeccion() | CambioEstado | ✅ |
| 29 | new CambioEstado | CambioEstado(...) | EventoSismico | ✅ |

### Fase 4: Obtención de datos del evento

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 30 | buscarDatosEventoSismico() | buscarDatosEventoSismico() | GestorRevisionEventoSismico | ✅ |
| 31 | obtenerDatosEvento() | obtenerDatosEvento() | EventoSismico | ✅ |
| 32 | getNombre() | getNombre() | AlcanceSismo | ✅ |
| 33 | getNombre() | getNombre() | OrigenDeGeneracion | ✅ |
| 34 | getNombre() | getNombre() | ClasificacionSismo | ✅ |

### Fase 5: Datos por estación / series temporales

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 35 | buscarDatosSeriePorEstacion() | buscarDatosSeriesPorEstacion() | GestorRevisionEventoSismico | ⚠️ singular/plural |
| 36 | Loop series | for serie in ...getSerieTemporal() | GestorRevisionEventoSismico | ✅ |
| 37 | obtenerNombreEstacion() | obtenerNombreEstacion(sismografos) | SerieTemporal | ✅ |
| 38 | esTuSerie() | esTuSerie(self) | Sismografo | ✅ |
| 39 | getNombre() | getNombre() | EstacionSismologica | ✅ |
| 40 | Loop muestras | for muestra in serie.getMuestraSismica() | GestorRevisionEventoSismico | ✅ |
| 41 | getFechaHoraMuestra() | getFechaHoraMuestra() | MuestraSismica | ✅ |
| 42 | Loop detalles | for detalle in muestra.getDetalleMuestraSismica() | GestorRevisionEventoSismico | ✅ |
| 43 | getDatos() | getDatos() | DetalleMuestraSismica | ✅ |
| 44 | esTuDenominacion() | esTuDenominacion("Longitud/Frecuencia/Velocidad") | TipoDeDato | ✅ |
| 45 | getValor() | getValor() | DetalleMuestraSismica | ✅ |

### Fase 6: CU18 y mostrar datos

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 46 | llamarCU18() | llamarCU18() | GestorRevisionEventoSismico | ✅ (simulado) |
| 47 | <<include>> CU18 | print("LLAMADA AL CU18...") | GestorRevisionEventoSismico | ✅ (simulado) |
| 48 | mostrarDatosEventoSismico() | mostrarDatosEventosSismicos() | PantallaRevisionEventoSismico | ⚠️ singular/plural |

### Fase 7: Interacciones opcionales

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 49 | tomarSeleccionMapa() | tomarSeleccionMapa() | PantallaRevisionEventoSismico | ✅ |
| 50 | tomarSeleccionModificar() | tomarSeleccionModificar() | PantallaRevisionEventoSismico | ✅ |

### Fase 8: Rechazar evento (alternativo)

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 51 | opRechazarEvento() (Pantalla) | opRechazarEvento() | PantallaRevisionEventoSismico | ✅ |
| 52 | opRecharEvento() (Gestor) | opRechazarEvento(accion) | GestorRevisionEventoSismico | ⚠️ typo en diagrama |
| 53 | validarAccionSeleccionada() | validarAccionSeleccionada() | GestorRevisionEventoSismico | ✅ |
| 54 | validarDatos() | validarDatos() | EventoSismico | ✅ |
| 55 | rechazarEventoSismico() | rechazarEventoSismico() | GestorRevisionEventoSismico | ✅ |
| 56 | Loop estados | for estado in estados_mock | GestorRevisionEventoSismico | ✅ |
| 57 | esAmbito() | esAmbitoEventoSismico() | Estado | ⚠️ nombre distinto |
| 58 | esRechazado() | esRechazado() | Estado | ✅ |
| 59 | obtenerEstadoActual() | obtenerEstadoActual() | EventoSismico | ✅ |
| 60 | esEstadoActual() | esEstadoActual() | CambioEstado | ✅ |
| 61 | calcularFechaHoraActual() | calcularFechaHoraActual() | GestorRevisionEventoSismico | ✅ |
| 62 | setEstadoActual() | setEstadoActual() | EventoSismico | ✅ |
| 63 | rechazar() | rechazar() | EventoSismico | ✅ |
| 64 | setFechaHoraFin() | setFechaHoraFin() | CambioEstado | ✅ |
| 65 | setResponsableInspeccion() | setResponsableInspeccion() | CambioEstado | ✅ |
| 66 | new CambioEstado | CambioEstado(...) | EventoSismico | ✅ |

### Fase 9: Finalización

| # | Mensaje | Método | Clase | Estado |
|---|---|---|---|---|
| 67 | finCU() | finCU() | PantallaRevisionEventoSismico | ✅ |

---

## 📈 Resumen estadístico

- Coincidencias exactas: 62 (~92.5%)
- Diferencias menores de nombre: 5 (~7.5%)
- Métodos faltantes: 0
- Total mensajes comparados: 67

## ⚠️ Diferencias detectadas

- `Estado.esAmbito()` (diagrama) vs `Estado.esAmbitoEventoSismico()` (código): el código es más específico.
- `buscarDatosSeriePorEstacion()` (diagrama) vs `buscarDatosSeriesPorEstacion()` (código): singular/plural.
- `mostrarDatosEventoSismico()` (diagrama) vs `mostrarDatosEventosSismicos()` (código): singular/plural.
- `opRecharEvento()` (diagrama) vs `opRechazarEvento()` (código): error tipográfico en diagrama.

## ✅ Fortalezas

- Fuerte adherencia al diagrama (flujo y mensajes).
- Máquina de estados correcta en `EventoSismico` con historial en `CambioEstado`.
- Separación de capas (Boundary / Control / Entity) consistente.
- Trazabilidad de responsable y timestamp en transiciones.

## 🚀 Oportunidades de mejora

- Unificar nomenclatura (diagrama ↔ código) para evitar confusiones.
- Reemplazar bubble sort por `sorted()` nativo (mejor rendimiento).
- Ampliar validaciones más allá de `None` (rangos, formatos, consistencia).
- Desacoplar `data.py` (mocks) mediante repositorios o inyección de dependencias.
- Sustituir `print` por `logging` estructurado.

## 🏁 Conclusión

La implementación es fiel al diagrama de secuencia con coincidencia casi total. Las diferencias son nominales y no afectan la funcionalidad. El diseño de la máquina de estados y las colaboraciones entre capas están correctamente realizadas.

**Calificación general**: 9.5/10.

---

### Notas de edición
- Este archivo está pensado para ser ajustado fácilmente (agregar/quitar filas, comentarios, etc.).
- Si se agregan nuevos flujos (confirmar/solicitar experto), puede añadirse una tabla simétrica a la de rechazo.
