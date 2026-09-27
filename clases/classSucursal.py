class Sucursales:
    # constructor
    def __init__(self, nombre, montoBoveda, calle, colonia, numero, pais, estado, telefono, companiaTel, empleados=None):
        self.__nombre = nombre
        self.__montoBoveda = montoBoveda
        self.__calle = calle
        self.__colonia = colonia
        self.__numero = numero
        self.__pais = pais
        self.__estado = estado
        self.__telefono = telefono
        self.__companiaTel = companiaTel
        self.__empleados = empleados if empleados is not None else []

    # getters
    def getNombre(self):
        return self.__nombre

    def getMontoBoveda(self):
        return self.__montoBoveda

    def getDireccion(self):
        return f"{self.__calle} #{self.__numero}, {self.__colonia}, {self.__estado}, {self.__pais}"

    def getTelefono(self):
        return f"{self.__telefono} ({self.__companiaTel})"

    def getEmpleados(self):
        return self.__empleados

    # setters
    def setNombre(self, nombre):
        if nombre == "":
            print("Favor de escribir un nombre para la sucursal")
        else:
            self.__nombre = nombre
            print("Nombre de la sucursal actualizado con exito.")

    def setMontoBoveda(self, monto):
        if monto < 0:
            print("El monto no puede ser negativo.")
        else:
            self.__montoBoveda = monto

    # metodos
    def agregarEmpleado(self, empleado):
        self.__empleados.append(empleado)

    def mostrar_informacion(self):
        return (f"Sucursal: {self.__nombre}\n"
                f"Direccion: {self.getDireccion()}\n"
                f"Telefono: {self.getTelefono()}\n"
                f"Monto de Boveda: {self.__montoBoveda}\n"
                f"Empleados: {len(self.__empleados)}")