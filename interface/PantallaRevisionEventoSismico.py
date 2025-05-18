from controllers.GestorRevisionEventoSismico import GestorRevisionEventoSismico

class PantallaRevisionEventoSismico:
    def __init__(self):
        self.gestorRevision:GestorRevisionEventoSismico = GestorRevisionEventoSismico()
        
    def opcRegistrarResultadoRevisionManual(self):
        return self.habilitarPantalla()

    def habilitarPantalla(self):
        return self.gestorRevision.opcRegistrarResultadoRevisionManual()
        
    
