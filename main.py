import tkinter as tk
from tkinter import PhotoImage, messagebox
from clases.classBanco import Banco
from clases.classSucursal import Sucursales
from adminSucursales import AdminSucursales
from adminSucursales import lista_sucursales
import os
import json

bancoPrincipal = None

#FUNCIONES DEL BANCO

def crear_objeto():
    global bancoPrincipal
    nombre_archivo = "src/config/banco.json"

    if os.path.isfile(nombre_archivo):
        messagebox.showinfo("Información", "El banco ya ha sido registrado.")
        return

    nombreBanco = entry_nombre.get()
    numero = entry_numero.get()
    codigoInternacional = entry_codigo.get()
    montoPrincipal = entry_monto.get()

    if not nombreBanco or not numero or not codigoInternacional or not montoPrincipal:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    # Crear el objeto Banco
    bancoPrincipal = Banco(nombreBanco, numero, codigoInternacional, montoPrincipal)

    # Datos a guardar
    datos = {
        "nombreBanco": nombreBanco,
        "numero": numero,
        "codigoInternacional": codigoInternacional,
        "montoPrincipal": montoPrincipal
    }

    try:
        # Guardar archivo JSON
        os.makedirs("src/config", exist_ok=True)
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        # Mostrar confirmación
        messagebox.showinfo("Información", "Datos guardados correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

def cancelar():
    entry_nombre.delete(0, tk.END)
    entry_numero.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)
    entry_monto.delete(0, tk.END)

def mostrar_informacion():
    nombre_archivo = "src/config/banco.json"
    if not os.path.isfile(nombre_archivo):
        messagebox.showinfo("Información", "El banco no ha sido creado aún.")
        return

    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    banco = Banco(
        datos["nombreBanco"],
        datos["numero"],
        datos["codigoInternacional"],
        datos["montoPrincipal"]
    )
    messagebox.showinfo("Información", banco.mostrar_informacion())

def mostrar_sucursales():
        if not lista_sucursales:
            messagebox.showinfo("Información", "No hay sucursales registradas.")
            return

        for sucursal in lista_sucursales:
            messagebox.showinfo("Sucursal registrada", sucursal.mostrar_informacion())

#PANTALLAS

def pantalla_principal():
    ventana = tk.Tk()
    ventana.title("Banco Internacional de Hyrule")
    ventana.geometry("600x600")
    ventana.configure(background="#A4BB86")

    label_titulo = tk.Label(ventana, text="Menú Principal",
                             font=("bahnschrift", 22, "bold"), bg="#A4BB86")
    label_titulo.pack(pady=15)

    btn_mostrar = tk.Button(ventana, text="Mostrar Información del Banco",
                            width=30, bg="#7BB0FF", command=mostrar_informacion)
    btn_mostrar.pack(pady=10)
    
    btn_mostrar = tk.Button(ventana, text="Agregar Sucursal",
                            width=30, bg="#B97BFF", command=AdminSucursales)
    btn_mostrar.pack(pady=13)

    btn_mostrar = tk.Button(ventana, text="Agregar gerente a Sucursal",
                            width=30, bg="#FF7BE9", command=AdminSucursales)
    btn_mostrar.pack(pady=16)

    btn_mostrar = tk.Button(ventana, text="Agregar cajeros a Sucursal",
                            width=30, bg="#7BFFB6", command=AdminSucursales)
    btn_mostrar.pack(pady=19)

    btn_mostrar = tk.Button(ventana, text="Mostrar Información Sucursales",
                            width=30, bg="#7BFFF8", command=mostrar_sucursales)
    btn_mostrar.pack(pady=20)

    btn_sucursales = tk.Button(ventana, text="Agregar clientes a Sucursal",
                               width=30, bg="#CEBF7D", command=AdminSucursales)
    btn_sucursales.pack(pady=21)

    btn_salir = tk.Button(ventana, text="Salir", width=30, bg="#E57373", command=ventana.destroy)
    btn_salir.pack(pady=24)

    ventana.mainloop()


def pantalla_banco():
    global entry_nombre, entry_numero, entry_codigo, entry_monto

    ventana = tk.Tk()
    ventana.title("Banco Internacional de Hyrule - Registro")
    ventana.configure(background="#A4BB86")

    tk.Label(ventana, text="Nombre del Banco Principal:").grid(row=0, column=0, padx=10, pady=5)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Número del Banco:").grid(row=1, column=0, padx=10, pady=5)
    entry_numero = tk.Entry(ventana)
    entry_numero.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Código Internacional:").grid(row=2, column=0, padx=10, pady=5)
    entry_codigo = tk.Entry(ventana)
    entry_codigo.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Monto Principal:").grid(row=3, column=0, padx=10, pady=5)
    entry_monto = tk.Entry(ventana)
    entry_monto.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(ventana, text="Guardar", command=crear_objeto).grid(row=4, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Cancelar", command=cancelar).grid(row=4, column=1, padx=10, pady=10)
    tk.Button(ventana, text="Mostrar Información", command=mostrar_informacion).grid(row=5, column=0, columnspan=2, pady=10)

    ventana.mainloop()

#pantalla bienvenida
def splash_screen():
    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("Pantalla de Bienvenida")
    ventana_bienvenida.geometry("700x700")
    ventana_bienvenida.configure(background="#A4BB86")

    label_titulo = tk.Label(ventana_bienvenida, text="Sistema Banco Internacional de Hyrule",
                             font=("bahnschrift", 24, "bold"), bg="#A4BB86")
    label_titulo.pack(pady=10)

    try:
        logo = PhotoImage(file="src/img/imgBanco.png")
        logo = logo.subsample(3)
        label_logo = tk.Label(ventana_bienvenida, image=logo, bg="#A4BB86")
        label_logo.image = logo
        label_logo.pack(pady=20)
    except Exception as e:
        print("No se encontró el archivo del logo:", e)

    label_mensaje = tk.Label(ventana_bienvenida, text="Cargando, por favor espere...", font=("bahnschrift", 14), bg="#A4BB86")
    label_mensaje.pack(pady=10)

    def continuar():
        ventana_bienvenida.destroy()
        nombre_archivo = "src/config/banco.json"
        if os.path.isfile(nombre_archivo):
            pantalla_principal()
        else:
            pantalla_banco()

    ventana_bienvenida.after(3000, continuar)
    ventana_bienvenida.mainloop()

if __name__ == "__main__":
    splash_screen()


