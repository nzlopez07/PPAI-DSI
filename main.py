
from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico as Gestor
from flask import Flask, render_template, request, redirect
from interface.PantallaRevisionEventoSismico import PantallaRevisionEventoSismico




#Iniciar Gestor
#gestor = Gestor()


app = Flask(__name__)
pantalla = PantallaRevisionEventoSismico()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/eventos')
def eventos():
    eventos = pantalla.opcRegistrarResultadoRevisionManual()
    return render_template('seleccionar_evento.html', eventos=eventos)

"""
@app.route('/eventos/evento')
def eventos():
    evento = pantalla.mostrarYSolicitarSeleccionEvento()
    return render_template('detalle_evento.html', eventos=eventos)
"""

"""
@app.route('/evento', methods=['POST'])
def evento():
    evento_id = int(request.form['evento_id'])
    evento = pantalla.obtener_evento_por_id(evento_id)
    return render_template('detalle_evento.html', evento=evento)

@app.route('/editar/<int:id>')
def editar(id):
    evento = pantalla.obtener_evento_por_id(id)
    return render_template('editar_evento.html', evento=evento)

@app.route('/guardar_edicion/<int:id>', methods=['POST'])
def guardar_edicion(id):
    datos = {
        'magnitud': request.form['magnitud'],
        'alcance': request.form['alcance'],
        'origen': request.form['origen']
    }
    pantalla.actualizar_evento(id, datos)
    return redirect(f'/confirmar/{id}')

@app.route('/confirmar/<int:id>')
def confirmar(id):
    evento = pantalla.obtener_evento_por_id(id)
    return render_template('confirmar_evento.html', evento=evento)

@app.route('/resultado_final/<int:id>', methods=['POST'])
def resultado_final(id):
    accion = request.form['accion']
    resultado = pantalla.finalizar_evento(id, accion)
    return render_template('resultado_final.html', resultado=resultado)
"""


if __name__ == "__main__":
    # Llamar al método para buscar eventos auto detectados
    app.run(debug=True)
    eventos = pantalla.opcionRegistrarRevisionManual()
    print (eventos)
    