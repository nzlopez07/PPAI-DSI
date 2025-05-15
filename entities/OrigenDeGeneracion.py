class OrigenDeGeneracion:
    def __init__(self, nombre, descripcion):
        self.descripcion = descripcion
        self.nombre = nombre

    # Metodos GET
    def getDescripcion(self):
        return self.descripcion
    
    def getNombre(self):
        return self.nombre
    
    # Metodos SET
    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setNombre(self, nombre):
        self.nombre = nombre