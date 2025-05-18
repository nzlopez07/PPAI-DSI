class AlcanceSismo:
    def __init__(self, nombre, descripcion):
        self.descripcion = descripcion
        self.nombre = nombre

    # Métodos GET
    def getDescripcion(self):
        return self.descripcion

    def getNombre(self):
        return self.nombre

    # Métodos SET
    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setNombre(self, nombre):
        self.nombre = nombre
