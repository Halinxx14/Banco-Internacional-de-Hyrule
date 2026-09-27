from clases.classPersonal import Personal

class Cliente(Personal):

    def __init__(self, nombre, telefono, direccion, pais, rfc, numeroCaja):
        super().__init__(nombre, telefono, direccion, pais, rfc)
        self.numeroCaja = numeroCaja

    def mostrar_informacion(self):
        return (f"Nombre: {self.nombre}\n"
                f"Telefono: {self.telefono}\n"
                f"Direccion: {self.direccion}\n"
                f"Pais: {self.pais}\n"
                f"RFC: {self.rfc}\n"
                f"Numero de Caja: {self.numeroCaja}")
