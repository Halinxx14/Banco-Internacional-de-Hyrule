class Banco:
    # Constructor
    def __init__(self, nombreBanco, numero, codigoInternacional, montoPrincipal):
        self._nombreBanco = nombreBanco
        self._numero = numero
        self._codigoInternacional = codigoInternacional
        self._montoPrincipal = montoPrincipal

    # Getters
    def getnombreBanco(self):
        return self._nombreBanco

    def getnumero(self):
        return self._numero

    def getcodigoInternacional(self):
        return self._codigoInternacional

    def getmontoPrincipal(self):
        return self._montoPrincipal

    # Setters
    def setnombreBanco(self, nombreBanco):
        if nombreBanco.strip() != "":
            self._nombreBanco = nombreBanco
        else:
            raise ValueError("El nombre del banco no puede estar vacío")

    def setnumero(self, numero):
        self._numero = numero

    def setcodigoInternacional(self, codigoInternacional):
        self._codigoInternacional = codigoInternacional

    def setmontoPrincipal(self, montoPrincipal):
        self._montoPrincipal = montoPrincipal

    # Metodo
    def mostrar_informacion(self):
        return (
            f"Nombre del Banco Principal: {self._nombreBanco}\n"
            f"No: {self._numero}\n"
            f"Código Internacional: {self._codigoInternacional}\n"
            f"Monto: {self._montoPrincipal}"
        )
