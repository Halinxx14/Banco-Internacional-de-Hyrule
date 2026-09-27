class Personal:
    # constructor
    def __init__(self, nombre, telefono, direccion, pais, rfc):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.pais = pais
        self.rfc = rfc

    def mostrar_informacion(self):
        return (f"Nombre: {self.nombre}\n"
                f"Telefono: {self.telefono}\n"
                f"Direccion: {self.direccion}\n"
                f"Pais: {self.pais}\n"
                f"Registro Federal de Contribuyentes: {self.rfc}\n")
