from clases.classPersonal import Personal

class Gerente(Personal):
    # constructor
    def __init__(self, nombre, telefono, direccion, pais, rfc):
        super().__init__(nombre, telefono, direccion, pais, rfc)
        self.puesto = "Gerente"          # atributo normal
        self.claveDeAcceso = "ACCESO-01" # atributo EXCLUSIVO del gerente

    def mostrar_informacion(self):
        return (f"Nombre: {self.nombre}\n"
                f"Telefono: {self.telefono}\n"
                f"Direccion: {self.direccion}\n"
                f"Pais: {self.pais}\n"
                f"RFC: {self.rfc}\n"
                f"Puesto: {self.puesto}\n"
                f"Clave de Acceso: {self.claveDeAcceso}\n")

