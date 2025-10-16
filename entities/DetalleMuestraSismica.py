from entities.TipoDeDato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self,valor, tipoDato:TipoDeDato):
        self.valor = valor
        self.tipoDeDato = tipoDato
        

    def getDatos(self):
        return self.tipoDeDato
    
    def getValor(self):
        return self.valor
    
    

