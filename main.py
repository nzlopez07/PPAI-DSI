from flask import Flask, render_template, request, redirect
from interface.PantallaRevisionEventoSismico import PantallaRevisionEventoSismico
#Iniciar Gestor
#gestor = Gestor()


app = Flask(__name__)
pantalla = PantallaRevisionEventoSismico()

# Ruta de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Ruta donde se muestran todos los eventos AutoDetectados y PendientesDeRevision
@app.route('/eventos')
def eventos():
    eventos = pantalla.opcRegistrarResultadoRevisionManual()
    return render_template('seleccionar_evento.html', eventos=eventos)

# Ruta donde se muestran los datos del evento seleccionado
@app.route('/eventos/evento', methods=['POST'])
def eventoSeleccionado():
    indice = int(request.form['eventoSeleccionado'])   
    alcance, origen, clasificacion, estaciones = pantalla.tomarSeleccionEvento(indice)
    for estacion in estaciones:
        print("Nombre estacion: ", estacion)
    return render_template('detalle_evento.html', alcance=alcance, origen=origen, clasificacion=clasificacion, estaciones=estaciones)

@app.route('/eventos/evento/rechazar', methods=['GET'])
def rechazarEvento():
    pantalla.opRechazarEvento()
    return render_template('rechazar.html')

@app.route('/eventos/evento/cancelar', methods=['GET'])
def cancelarEvento():
    pantalla.cancelarRevisionEvento()
    return redirect('/')


@app.route('/eventos/evento/confirmar', methods=['GET'])
def confirmarEvento():
    pantalla.opConfirmarEvento()
    return render_template('confirmar.html', mensaje="El evento fue CONFIRMADO exitosamente.")

@app.route('/eventos/evento/solicitar_experto', methods=['GET'])
def solicitarRevisionExperto():
    pantalla.opSolicitarRevisionExperto()
    return render_template('resultado_final.html', mensaje="La revisión fue solicitada a un experto exitosamente.")


@app.route('/eventos/evento/seleccion_mapa', methods=['POST'])
def tomarSeleccionMapa():
    print("SELECCION MAPA", pantalla.seleccionMapa)
    pantalla.tomarSeleccionMapa(True)
    print("SELECCION MAPA", pantalla.seleccionMapa)
    return ('', 204)

@app.route('/eventos/evento/seleccion_modificar', methods=['POST'])
def tomarSeleccionModificar():
    print("SELECCION MODIFICAR", pantalla.seleccionModificar)
    pantalla.tomarSeleccionModificar(True)
    print("SELECCION MODIFICAR", pantalla.seleccionModificar)
    return ('', 204)


if __name__ == "__main__":
    # Llamar al método para buscar eventos auto detectados
    app.run(debug=True)
    eventos = pantalla.opcionRegistrarRevisionManual()
    print (eventos)
