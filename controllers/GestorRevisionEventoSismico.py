from datetime import datetime
from entities.EventoSismico import EventoSismico
from entities.CambioEstado import CambioEstado
from entities.Sesion import Sesion
from collections import defaultdict
from sqlalchemy.orm import Session

# Importar repositorios
from database.repositories import EventoSismicoRepository, UsuarioRepository


class GestorRevisionEventoSismico:
    def __init__(self, pantalla, db_session: Session):
        self.pantallaRevision = pantalla
        self.db = db_session
        self.evento_repo = EventoSismicoRepository(db_session)
        self.usuario_repo = UsuarioRepository(db_session)
        self.horaFechaFinCambioEstado = None
        self.eventosSismicosAutoDetectados: list[EventoSismico] = [] # Colección de todos los eventos sísmicos con estado actual "AutoDetectado"
        self.eventoSismicoSeleccionado: EventoSismico = None
        self.estadoBloqueadoEnRevision = None  # Ya no necesita type hint Estado
        self.estadoRechazado = None
        self.estadoConfirmado = None
        self.estadoRevisionExperto = None
        self.cambioEstadoActual: CambioEstado = None
        self.nombreAlcance = None
        self.nombreOrigen = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.accionSeleccionada = None 
        self.sesionActiva = None  # Se inicializará después con el usuario de BD
        self.usuarioActivo = None


    #Métodos get y set si corresponden
    def getEventosSismicosAutoDetectados(self):
        return self.eventosSismicosAutoDetectados

    # Lógica del CU
    def opcRegistrarResultadoRevisionManual(self):
        self.obtenerUsuarioLogueado()
        return self.buscarEventosAutoDetectados()

    def calcularFechaHoraActual(self):
    # Método para calcular fecha y hora en el momento    
        return datetime.now()
    
    # Buscar eventos autodetectados o pendientes de revision para mostrar al inicio
    def buscarEventosAutoDetectados(self):
        """
        Busca eventos en estado AutoDetectado o PendienteDeRevision desde la BD.
        """
        self.eventosSismicosAutoDetectados = []
        
        # Buscar eventos autodetectados desde la BD
        eventos_auto = self.evento_repo.get_by_estado("AutoDetectado")
        self.eventosSismicosAutoDetectados.extend(eventos_auto)
        
        # Buscar eventos pendientes de revisión desde la BD
        eventos_pendientes = self.evento_repo.get_by_estado("PendienteDeRevision")
        self.eventosSismicosAutoDetectados.extend(eventos_pendientes)
        
        print(f"[LOG] Eventos encontrados desde BD: {len(self.eventosSismicosAutoDetectados)}")
        
        # Ordena los eventos sísmicos a mostrar
        self.ordenarPorFechaYHora(self.eventosSismicosAutoDetectados)
        # Los manda
        self.pantallaRevision.mostrarYSolicitarSeleccionEvento(self.eventosSismicosAutoDetectados)


    def ordenarPorFechaYHora(self, eventosSismicos:list[EventoSismico]):
        n = len(eventosSismicos)
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if (eventosSismicos[i].getFechaHoraOcurrencia()) > (eventosSismicos[j].getFechaHoraOcurrencia()):
                    eventosSismicos[i], eventosSismicos[j] = eventosSismicos[j], eventosSismicos[i]
    
    # Seleccionar un evento
    def tomarSeleccionEvento(self, evento):
        """
        Mensaje 7 del diagrama de secuencia: tomarSeleccionEvento(evento)
        """
        self.eventoSismicoSeleccionado = evento
        self.bloquearEventoSismico()
        self.buscarDatosEventoSismico()
        self.buscarDatosSeriesPorEstacion()
        self.llamarCU18()
        self.pantallaRevision.mostrarDatosEventosSismicos(self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion, self.datosEventoPorEstacion)
        
    def bloquearEventoSismico(self):
        """
        Mensaje 8 del diagrama de secuencia: bloquearEventoSismico()
        Ahora usa el patrón State: delega la transición al evento.
        """
        print(f"[LOG] Bloqueando evento sísmico usando patrón State")
        
        # El evento maneja la transición internamente
        try:
            self.eventoSismicoSeleccionado.bloquearEventoEnRevision()
            
            # Actualizar responsable en el cambio de estado actual
            cambio_actual = self.eventoSismicoSeleccionado.obtenerEstadoActual()
            if cambio_actual and self.usuarioActivo:
                cambio_actual.setResponsableInspeccion(self.usuarioActivo)
            
            # Persistir cambios en la BD
            self.evento_repo.save(self.eventoSismicoSeleccionado)
            self.db.commit()
            print(f"[LOG] Evento bloqueado y persistido en BD")
                
        except ValueError as e:
            self.db.rollback()
            print(f"[ERROR] No se pudo bloquear el evento: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Error al persistir evento bloqueado: {e}")
    
    def buscarDatosEventoSismico(self):
        """
        Mensaje 9 del diagrama de secuencia: buscarDatosEventoSismico()
        """
        self.nombreAlcance, self.nombreOrigen, self.nombreClasificacion = self.eventoSismicoSeleccionado.obtenerDatosEvento()


    def buscarDatosSeriesPorEstacion(self):
        """
        Mensaje 10 del diagrama de secuencia: buscarDatosSeriesPorEstacion()
        Obtiene los datos por estación desde el repositorio (sin acceder directo a modelos).
        """
        self.datosEventoPorEstacion = self.evento_repo.get_datos_evento_por_estacion(
            self.eventoSismicoSeleccionado._db_id
        )
        total_items = sum(len(v) for v in self.datosEventoPorEstacion.values())
        print(f"[LOG] Datos por estación cargados: {len(self.datosEventoPorEstacion)} estaciones, {total_items} muestras")


    def llamarCU18(self):
        """
        Mensaje 11 del diagrama de secuencia: llamarCU18()
        """
        print("[LOG] Llamada al CU18 - Generar sismogramas")

    def opRechazarEvento(self,accionSeleccionada):
        self.accionSeleccionada = accionSeleccionada
        if(self.validarAccionSeleccionada(self.accionSeleccionada)):
            if(self.eventoSismicoSeleccionado.validarDatos()):
                self.rechazarEventoSismico()
            else:
                print("Datos inválidos")

    def validarAccionSeleccionada(self, opcion):
        if (opcion in ["Rechazar evento", "Confirmar evento", "Solicitar Revision a experto"]):
            return True

    def obtenerUsuarioLogueado(self):
        """
        Obtiene el usuario logueado. Por ahora usa un usuario de prueba de la BD.
        """
        if not self.sesionActiva:
            # Buscar un usuario de prueba en la BD (el primero disponible)
            # Preferimos el nombre explícito del método para evitar problemas de aliasing
            usuario = self.usuario_repo.get_by_nombre_usuario("juan.gonzález")
            if usuario:
                self.sesionActiva = Sesion(datetime.now(), usuario)
                self.usuarioActivo = usuario.getEmpleado()
                print(f"[LOG] Usuario activo: {self.usuarioActivo.getNombre()} {self.usuarioActivo.getApellido()}")
            else:
                print("[ERROR] No se encontró usuario de prueba en la BD")
        else:
            self.usuarioActivo = self.sesionActiva.getUsuarioActivo().getEmpleado()

    def rechazarEventoSismico(self):
        """
        Mensaje 18 del diagrama de secuencia: rechazarEventoSismico()
        Ahora usa el patrón State: delega la transición al evento.
        """
        print(f"[LOG] Rechazando evento sísmico usando patrón State")
        
        try:
            self.eventoSismicoSeleccionado.rechazarEvento()
            
            # Actualizar responsable en el cambio de estado actual
            cambio_actual = self.eventoSismicoSeleccionado.obtenerEstadoActual()
            if cambio_actual and self.usuarioActivo:
                cambio_actual.setResponsableInspeccion(self.usuarioActivo)
            
            # Persistir cambios en la BD
            self.evento_repo.save(self.eventoSismicoSeleccionado)
            self.db.commit()
            print(f"[LOG] Evento rechazado y persistido en BD")
            
            # Log del historial
            print(f"[LOG] Evento rechazado. Estado actual: {self.eventoSismicoSeleccionado.getEstadoActual().getNombreEstado()}")
            print(f"[LOG] Historial de cambios de estado:")
            for idx, cambio in enumerate(self.eventoSismicoSeleccionado.getCambioEstado()):
                responsable_nombre = getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))() if cambio.getResponsableInspeccion() else "N/A"
                print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {responsable_nombre}")
                
        except ValueError as e:
            self.db.rollback()
            print(f"[ERROR] No se pudo rechazar el evento: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Error al persistir evento rechazado: {e}")
            
        self.finCU()

    def cancelarRevisionEventoSismico(self):
        """
        Mensaje 21 del diagrama de secuencia: cancelarRevisionEventoSismico()
        Ahora usa el patrón State: delega la transición al evento.
        """
        if not self.eventoSismicoSeleccionado:
            print("[LOG] No hay evento sísmico seleccionado.")
            return
        
        print(f"[LOG] Cancelando revisión usando patrón State")
        
        try:
            # El evento maneja la transición internamente
            self.eventoSismicoSeleccionado.cancelarRevision()
            
            # Persistir cambios en la BD
            self.evento_repo.save(self.eventoSismicoSeleccionado)
            self.db.commit()
            print(f"[LOG] Revisión cancelada y persistida en BD. Estado actual: {self.eventoSismicoSeleccionado.getEstadoActual().getNombreEstado()}")
            
        except ValueError as e:
            self.db.rollback()
            print(f"[ERROR] No se pudo cancelar la revisión: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Error al persistir cancelación: {e}")
            
        self.finCU()


    def finCU(self):
        # Fin del caso de uso
        print("Fin del caso de uso")
        self.eventoSismicoSeleccionado = None
        self.estadoBloqueadoEnRevision = None
        self.estadoRechazado = None 
        self.cambioEstadoActual = None
        self.nombreAlcance = None
        self.nombreOrigen = None
        self.nombreClasificacion = None
        self.datosEventoPorEstacion = None
        self.pantallaRevision.finCU()

    def opConfirmarEvento(self, accionSeleccionada):
        self.accionSeleccionada = accionSeleccionada
        if(self.validarAccionSeleccionada(self.accionSeleccionada)):
            if(self.eventoSismicoSeleccionado.validarDatos()):
                self.confirmarEventoSismico()
            else:
                print("Datos inválidos")
    
    def confirmarEventoSismico(self):
        """
        Mensaje 15 del diagrama de secuencia: confirmarEventoSismico()
        Ahora usa el patrón State: delega la transición al evento.
        """
        print(f"[LOG] Confirmando evento sísmico usando patrón State")
        
        try:
            self.eventoSismicoSeleccionado.confirmarEvento()
            
            # Actualizar responsable en el cambio de estado actual
            cambio_actual = self.eventoSismicoSeleccionado.obtenerEstadoActual()
            if cambio_actual and self.usuarioActivo:
                cambio_actual.setResponsableInspeccion(self.usuarioActivo)
            
            # Persistir cambios en la BD
            self.evento_repo.save(self.eventoSismicoSeleccionado)
            self.db.commit()
            print(f"[LOG] Evento confirmado y persistido en BD")
            
            # Log del historial
            print(f"[LOG] Evento confirmado. Estado actual: {self.eventoSismicoSeleccionado.getEstadoActual().getNombreEstado()}")
            print(f"[LOG] Historial de cambios de estado:")
            for idx, cambio in enumerate(self.eventoSismicoSeleccionado.getCambioEstado()):
                responsable_nombre = getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))() if cambio.getResponsableInspeccion() else "N/A"
                print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {responsable_nombre}")
                
        except ValueError as e:
            self.db.rollback()
            print(f"[ERROR] No se pudo confirmar el evento: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Error al persistir evento confirmado: {e}")
            
        self.finCU()
        
    def opSolicitarRevisionExperto(self, accionSeleccionada):
        self.accionSeleccionada = accionSeleccionada
        if(self.validarAccionSeleccionada(self.accionSeleccionada)):
            if(self.eventoSismicoSeleccionado.validarDatos()):
                self.solicitarRevisionExperto()
            else:
                print("Datos inválidos")

    def solicitarRevisionExperto(self):
        """
        Mensaje 16 del diagrama de secuencia: solicitarRevisionExperto()
        Ahora usa el patrón State: delega la transición al evento.
        """
        print(f"[LOG] Solicitando revisión a experto usando patrón State")
        
        try:
            self.eventoSismicoSeleccionado.solicitarRevisionExpertoEvento()
            
            # Actualizar responsable en el cambio de estado actual
            cambio_actual = self.eventoSismicoSeleccionado.obtenerEstadoActual()
            if cambio_actual and self.usuarioActivo:
                cambio_actual.setResponsableInspeccion(self.usuarioActivo)
            
            # Persistir cambios en la BD
            self.evento_repo.save(self.eventoSismicoSeleccionado)
            self.db.commit()
            print(f"[LOG] Revisión a experto solicitada y persistida en BD")
            
            # Log del historial
            print(f"[LOG] Revisión solicitada a experto. Estado actual: {self.eventoSismicoSeleccionado.getEstadoActual().getNombreEstado()}")
            print(f"[LOG] Historial de cambios de estado:")
            for idx, cambio in enumerate(self.eventoSismicoSeleccionado.getCambioEstado()):
                responsable_nombre = getattr(cambio.getResponsableInspeccion(), 'getNombre', lambda: str(cambio.getResponsableInspeccion()))() if cambio.getResponsableInspeccion() else "N/A"
                print(f"  #{idx+1}: {cambio.getEstado().getNombreEstado()} | Inicio: {cambio.getFechaHoraInicio()} | Fin: {cambio.getFechaHoraFin()} | Responsable: {responsable_nombre}")
                
        except ValueError as e:
            self.db.rollback()
            print(f"[ERROR] No se pudo solicitar revisión a experto: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Error al persistir solicitud de revisión: {e}")
            
        self.finCU()
        