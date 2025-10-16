from flask import Flask, render_template, request, redirect
from interface.PantallaRevisionEventoSismico import PantallaRevisionEventoSismico
#Iniciar Gestor
#gestor = Gestor()


app = Flask(__name__)
pantalla = PantallaRevisionEventoSismico()


# Ruta de inicio
@app.route('/')
def home():
    """
    Mensaje 0: home()
    """
    return render_template('index.html')

# Ruta donde se muestran todos los eventos AutoDetectados y PendientesDeRevision
@app.route('/eventos')
def eventos():
    """
    Mensaje 1: eventos()
    """
    eventos = pantalla.opcRegistrarResultadoRevisionManual()
    print(f"[LOG] Mostrando eventos autodetectados y pendientes de revisión: {len(eventos)} eventos")
    return render_template('seleccionar_evento.html', eventos=eventos)

# Ruta donde se muestran los datos del evento seleccionado
@app.route('/eventos/evento', methods=['POST'])
def eventoSeleccionado():
    """
    Mensaje 4: eventoSeleccionado()
    """
    indice = int(request.form['eventoSeleccionado'])   
    alcance, origen, clasificacion, estaciones = pantalla.tomarSeleccionEvento(indice)
    print(f"[LOG] Evento seleccionado: {indice}, Origen={origen}, Alcance={alcance}, Clasificación={clasificacion}")
    return render_template('detalle_evento.html', alcance=alcance, origen=origen, clasificacion=clasificacion, estaciones=estaciones)

@app.route('/eventos/evento/rechazar', methods=['GET'])
def rechazarEvento():
    """
    Mensaje 6: rechazarEvento()
    """
    pantalla.opRechazarEvento()
    print("[LOG] Evento rechazado desde la vista")
    return render_template('rechazar.html')

@app.route('/eventos/evento/cancelar', methods=['GET'])
def cancelarEvento():
    """
    Mensaje 20: cancelarEvento()
    """
    pantalla.cancelarRevisionEvento()
    print("[LOG] Cancelación de revisión de evento desde la vista")
    return redirect('/')

@app.route('/eventos/evento/confirmar', methods=['GET'])
def confirmarEvento():
    """
    Mensaje 14: confirmarEvento()
    """
    pantalla.opConfirmarEvento()
    print("[LOG] Evento confirmado desde la vista")
    return render_template('confirmar.html', mensaje="El evento fue CONFIRMADO exitosamente.")

@app.route('/eventos/evento/solicitar_experto', methods=['GET'])
def solicitarRevisionExperto():
    """
    Mensaje 15: solicitarRevisionExperto()
    """
    pantalla.opSolicitarRevisionExperto()
    print("[LOG] Solicitud de revisión a experto desde la vista")
    return render_template('resultado_final.html', mensaje="La revisión fue solicitada a un experto exitosamente.")

@app.route('/eventos/evento/seleccion_mapa', methods=['POST'])
def tomarSeleccionMapa():
    """
    Mensaje extra: tomarSeleccionMapa()
    """
    pantalla.tomarSeleccionMapa(True)
    print(f"[LOG] Selección de mapa activada: {pantalla.seleccionMapa}")
    return ('', 204)

@app.route('/eventos/evento/seleccion_modificar', methods=['POST'])
def tomarSeleccionModificar():
    """
    Mensaje extra: tomarSeleccionModificar()
    """
    pantalla.tomarSeleccionModificar(True)
    print(f"[LOG] Selección de modificar activada: {pantalla.seleccionModificar}")
    return ('', 204)


if __name__ == "__main__":
    # Llamar al método para buscar eventos auto detectados
    app.run(debug=True)
    eventos = pantalla.opcionRegistrarRevisionManual()
    print (eventos)
