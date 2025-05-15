class ClasificacionSismo:
    def __init__(self,kmProfundidadDesde,kmProfundidadHasta,nombre):
        self.kmProfundidadDesde = kmProfundidadDesde
        self.kmProfunidadHasta = kmProfundidadHasta
        self.nombre = nombre
    
    # Metodos GET

    def getKmProfundidadDesde(self):
        return self.kmProfundidadDesde
    
    def getKmProfundidadHasta(self):
        return self.kmProfunidadHasta
    
    def getNombre(self):
        return self.nombre
    
    # Metodos SET
    
    def setKmProfundidaDesde(self, kmProfundidadDesde):
         self.kmProfundidadDesde = kmProfundidadDesde

    def setKmProfundidaHasta(self, kmProfundidadHasta):
         self.kmProfundidadHasta = kmProfundidadHasta

    def setNombre(self, nombre):
        self.nombre = nombre 