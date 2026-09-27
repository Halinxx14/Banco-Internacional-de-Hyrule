import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ----------------------------------------------------------
#  ARCHIVO JSON
# ----------------------------------------------------------

RUTA = "src/config/sucursales.json"


def guardar_sucursales_json(lista):
    os.makedirs("src/config", exist_ok=True)
    with open(RUTA, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4, ensure_ascii=False)


def cargar_sucursales_json():
    if not os.path.isfile(RUTA):
        return []
    with open(RUTA, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# ESTA ES LA LISTA GLOBAL (FUNCIÓN DE CARGA)
lista_sucursales = cargar_sucursales_json()


# ----------------------------------------------------------
#     VENTANA PRINCIPAL DE ADMINISTRAR SUCURSALES
# ----------------------------------------------------------

def AdminSucursales():

    ventana = tk.Toplevel()
    ventana.title("Administrar Sucursales")
    ventana.geometry("600x540")
    ventana.configure(bg="white")

    # ------------------------------------------
    #  TÍTULO
    # ------------------------------------------
    label_titulo = tk.Label(
        ventana, text="Administración de Sucursales",
        font=("Arial", 16, "bold"), bg="white"
    )
    label_titulo.pack(pady=10)

    frame_botones = tk.Frame(ventana, bg="white")
    frame_botones.pack()

    # ----------------------------------------------------------
    #  GUARDAR SUCURSAL
    # ----------------------------------------------------------

    def guardar_sucursal():
        nombre = entry_nombreSucursal.get()
        montoBoveda = entry_montoBoveda.get()
        calle = entry_calle.get()
        colonia = entry_colonia.get()
        numero = entry_numero.get()
        pais = combo_pais.get()
        estado = entry_estado.get()
        telefono = entry_telefono.get()
        companiaTel = combo_compTelef.get()

        if pais == "Selecciona un país":
            messagebox.showinfo("Aviso", "Selecciona un país.")
            return

        sucursal = {
            "nombre": nombre,
            "monto": montoBoveda,
            "calle": calle,
            "colonia": colonia,
            "numero": numero,
            "pais": pais,
            "estado": estado,
            "telefono": telefono,
            "companiaTel": companiaTel,
            "empleados": []
        }

        lista_sucursales.append(sucursal)
        guardar_sucursales_json(lista_sucursales)

        messagebox.showinfo("OK", "Sucursal registrada.")
        limpiar_campos()

    # ----------------------------------------------------------
    #  MOSTRAR SUCURSALES (UNA POR UNA)
    # ----------------------------------------------------------

    def mostrar_sucursales():
        if not lista_sucursales:
            messagebox.showinfo("Aviso", "No hay sucursales registradas.")
            return

        for s in lista_sucursales:
            info = (
                f"Sucursal: {s['nombre']}\n"
                f"Monto: {s['monto']}\n"
                f"Dirección: {s['calle']} #{s['numero']}, {s['colonia']}, {s['estado']}, {s['pais']}\n"
                f"Telefono: {s['telefono']} ({s['companiaTel']})\n"
                f"Empleados:\n" +
                ("\n".join(s["empleados"]) if s["empleados"] else "Sin empleados")
            )
            messagebox.showinfo("Sucursal", info)

    # ----------------------------------------------------------
    #  AGREGAR PERSONAL
    # ----------------------------------------------------------

    def agregar_personal():

        if not lista_sucursales:
            messagebox.showinfo("Aviso", "Primero registra una sucursal.")
            return

        ventana_personal = tk.Toplevel(ventana)
        ventana_personal.title("Agregar Personal")
        ventana_personal.geometry("350x430")
        ventana_personal.configure(bg="white")

        # Seleccionar sucursal
        tk.Label(ventana_personal, text="Sucursal:", bg="white").pack()
        combo_sucursal = ttk.Combobox(
            ventana_personal,
            state="readonly",
            values=[s["nombre"] for s in lista_sucursales]
        )
        combo_sucursal.pack(pady=5)

        # Puesto
        tk.Label(ventana_personal, text="Puesto:", bg="white").pack()
        combo_puesto = ttk.Combobox(
            ventana_personal,
            state="readonly",
            values=["Gerente", "Cajero", "Cliente"]
        )
        combo_puesto.pack(pady=5)

        # Datos generales
        tk.Label(ventana_personal, text="Nombre:", bg="white").pack()
        e_nombre = tk.Entry(ventana_personal); e_nombre.pack()

        tk.Label(ventana_personal, text="Telefono:", bg="white").pack()
        e_tel = tk.Entry(ventana_personal); e_tel.pack()

        tk.Label(ventana_personal, text="Direccion:", bg="white").pack()
        e_dir = tk.Entry(ventana_personal); e_dir.pack()

        tk.Label(ventana_personal, text="Pais:", bg="white").pack()
        e_pais = tk.Entry(ventana_personal); e_pais.pack()

        tk.Label(ventana_personal, text="RFC:", bg="white").pack()
        e_rfc = tk.Entry(ventana_personal); e_rfc.pack()

        # Extra para cliente
        tk.Label(ventana_personal, text="Ocupación (cliente):", bg="white").pack()
        e_ocup = tk.Entry(ventana_personal); e_ocup.pack()

        tk.Label(ventana_personal, text="Tipo Cuenta (cliente):", bg="white").pack()
        e_tipo = tk.Entry(ventana_personal); e_tipo.pack()

        def guardar_personal():

            suc_name = combo_sucursal.get()
            puesto = combo_puesto.get()
            nombre = e_nombre.get()

            if suc_name == "" or puesto == "":
                messagebox.showinfo("Aviso", "Selecciona sucursal y puesto.")
                return

            # Buscar sucursal seleccionada
            for s in lista_sucursales:
                if s["nombre"] == suc_name:
                    sucursal_sel = s
                    break

            # Crear texto simple
            if puesto == "Cliente":
                empleado_texto = f"Cliente: {nombre}"
            elif puesto == "Cajero":
                empleado_texto = f"Cajero: {nombre}"
            else:
                empleado_texto = f"Gerente: {nombre}"

            sucursal_sel["empleados"].append(empleado_texto)
            guardar_sucursales_json(lista_sucursales)

            messagebox.showinfo("OK", "Empleado registrado.")
            ventana_personal.destroy()

        tk.Button(ventana_personal, text="Guardar", bg="#7BB0FF",
                  width=15, command=guardar_personal).pack(pady=10)

    # ----------------------------------------------------------
    #  MOSTRAR PERSONAL (UNO POR UNO)
    # ----------------------------------------------------------

    def mostrar_personal():

        if not lista_sucursales:
            messagebox.showinfo("Aviso", "No hay sucursales.")
            return

        for s in lista_sucursales:
            for emp in s["empleados"]:
                info = (
                    f"Sucursal: {s['nombre']}\n"
                    f"Empleado:\n{emp}"
                )
                messagebox.showinfo("Empleado", info)

    # ----------------------------------------------------------
    #  LIMPIAR CAMPOS
    # ----------------------------------------------------------

    def limpiar_campos():
        entry_nombreSucursal.delete(0, tk.END)
        entry_montoBoveda.delete(0, tk.END)
        entry_calle.delete(0, tk.END)
        entry_colonia.delete(0, tk.END)
        entry_numero.delete(0, tk.END)
        combo_pais.set("Selecciona un país")
        entry_estado.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        combo_compTelef.set("Selecciona compañía telefónica")

    # ----------------------------------------------------------
    #  BOTONES DEL MENÚ
    # ----------------------------------------------------------

    tk.Button(frame_botones, text="GUARDAR", width=15, bg="#7BB0FF",
              command=guardar_sucursal).grid(row=0, column=0, padx=5)

    tk.Button(frame_botones, text="MOSTRAR", width=15, bg="#7BB0FF",
              command=mostrar_sucursales).grid(row=0, column=1, padx=5)

    tk.Button(frame_botones, text="AGREGAR PERSONAL", width=18, bg="#F7C97F",
              command=agregar_personal).grid(row=0, column=2, padx=5)

    tk.Button(frame_botones, text="MOSTRAR PERSONAL", width=18, bg="#9BFF9F",
              command=mostrar_personal).grid(row=0, column=3, padx=5)

    # ----------------------------------------------------------
    #  FORMULARIO VISUAL
    # ----------------------------------------------------------

    frameAgregar = tk.Frame(ventana, bg="#B5E3E6", bd=2, relief="groove")
    frameAgregar.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(frameAgregar, text="Nombre de Sucursal:", bg="#B5E3E6").place(x=10, y=10)
    entry_nombreSucursal = tk.Entry(frameAgregar)
    entry_nombreSucursal.place(x=160, y=10, width=180)

    tk.Label(frameAgregar, text="Monto Bóveda:", bg="#B5E3E6").place(x=10, y=40)
    entry_montoBoveda = tk.Entry(frameAgregar)
    entry_montoBoveda.place(x=160, y=40, width=180)

    tk.Label(frameAgregar, text="Dirección", bg="#B5E3E6",
             font=("Arial", 10, "bold")).place(x=10, y=70)

    tk.Label(frameAgregar, text="Calle:", bg="#B5E3E6").place(x=10, y=100)
    entry_calle = tk.Entry(frameAgregar)
    entry_calle.place(x=60, y=100, width=140)

    tk.Label(frameAgregar, text="Colonia:", bg="#B5E3E6").place(x=210, y=100)
    entry_colonia = tk.Entry(frameAgregar)
    entry_colonia.place(x=270, y=100, width=100)

    tk.Label(frameAgregar, text="Número:", bg="#B5E3EE6").place(x=380, y=100)
    entry_numero = tk.Entry(frameAgregar)
    entry_numero.place(x=440, y=100, width=55)

    tk.Label(frameAgregar, text="País:", bg="#B5E3E6").place(x=10, y=130)
    combo_pais = ttk.Combobox(frameAgregar, state="readonly",
                              values=["México", "Canadá", "Estados Unidos", "Guatemala"])
    combo_pais.set("Selecciona un país")
    combo_pais.place(x=60, y=130, width=180)

    tk.Label(frameAgregar, text="Estado:", bg="#B5E3E6").place(x=260, y=130)
    entry_estado = tk.Entry(frameAgregar)
    entry_estado.place(x=320, y=130, width=140)

    tk.Label(frameAgregar, text="Teléfono:", bg="#B5E3E6").place(x=10, y=170)
    entry_telefono = tk.Entry(frameAgregar)
    entry_telefono.place(x=80, y=170, width=120)

    tk.Label(frameAgregar, text="Compañía:", bg="#B5E3E6").place(x=210, y=170)
    combo_compTelef = ttk.Combobox(frameAgregar, state="readonly",
                                   values=["Telcel", "Movistar", "AT&T", "Unefon"])
    combo_compTelef.set("Selecciona compañía telefónica")
    combo_compTelef.place(x=280, y=170, width=150)

    tk.Button(frameAgregar, text="Cerrar", bg="#FF7B7B", width=12,
              command=ventana.destroy).place(x=230, y=260)


# FIN DEL ARCHIVO
