# adminSucursales.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# tus clases (asegúrate de tener estos archivos en la carpeta clases)
from clases.classSucursal import Sucursales
from clases.classGerente import Gerente
from clases.classCajeros import Cajero
from clases.classCliente import Cliente

# Rutas JSON
RUTA_SUC = "src/config/sucursales.json"
RUTA_PER = "src/config/personal.json"

# Listas en memoria
lista_sucursales = []        # contendrá objetos Sucursales
lista_personal_objs = []     # contendrá objetos Gerente/Cajero/Cliente

# ---------- Funciones JSON ----------
def guardar_json(ruta, datos):
    os.makedirs("src/config", exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_json(ruta):
    if not os.path.isfile(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- Convertir objetos a dicts simples para guardar ----------
def personal_objs_a_dicts():
    datos = []
    for p in lista_personal_objs:
        tipo = p.__class__.__name__
        d = {
            "tipo": tipo,
            "nombre": getattr(p, "nombre", ""),
            "telefono": getattr(p, "telefono", ""),
            "direccion": getattr(p, "direccion", ""),
            "pais": getattr(p, "pais", ""),
            "rfc": getattr(p, "rfc", ""),
            "numeroCaja": getattr(p, "numeroCaja", ""),
            "ocupacion": getattr(p, "ocupacion", ""),
            "tipoCuenta": getattr(p, "tipodecuenta", getattr(p, "tipoCuenta", "")),
            "claveAcceso": getattr(p, "claveDeAcceso", ""),
            "sucursal": getattr(p, "sucursal", "")
        }
        datos.append(d)
    return datos

def sucursales_objs_a_dicts():
    datos = []
    for s in lista_sucursales:
        datos.append({
            "nombre": s.getNombre(),
            "montoBoveda": s.getMontoBoveda(),
            "calle": s._Sucursales__calle,
            "colonia": s._Sucursales__colonia,
            "numero": s._Sucursales__numero,
            "pais": s._Sucursales__pais,
            "estado": s._Sucursales__estado,
            "telefono": s._Sucursales__telefono,
            "companiaTel": s._Sucursales__companiaTel
        })
    return datos

# ---------- Cargar desde JSON ----------
def cargar_todo():
    # cargar sucursales
    lista_sucursales.clear()
    suc_data = cargar_json(RUTA_SUC)
    for s in suc_data:
        obj = Sucursales(
            s.get("nombre", ""),
            s.get("montoBoveda", ""),
            s.get("calle", ""),
            s.get("colonia", ""),
            s.get("numero", ""),
            s.get("pais", ""),
            s.get("estado", ""),
            s.get("telefono", ""),
            s.get("companiaTel", ""),
            []  
        )
        lista_sucursales.append(obj)

    # cargar personal
    lista_personal_objs.clear()
    per_data = cargar_json(RUTA_PER)
    for p in per_data:
        tipo = p.get("tipo", "")
        nombre = p.get("nombre", "")
        telefono = p.get("telefono", "")
        direccion = p.get("direccion", "")
        pais = p.get("pais", "")
        rfc = p.get("rfc", "")
        sucursal_nombre = p.get("sucursal", "")

        if tipo == "Gerente":
            persona = Gerente(nombre, telefono, direccion, pais, rfc)
            if "claveAcceso" in p and p["claveAcceso"]:
                try: persona.claveDeAcceso = p["claveAcceso"]
                except: pass
        elif tipo == "Cajero":
            persona = Cajero(nombre, telefono, direccion, pais, rfc, p.get("numeroCaja", ""))
        else:
            persona = Cliente(nombre, telefono, direccion, pais, rfc, p.get("ocupacion",""), p.get("tipoCuenta",""))

        try: persona.sucursal = sucursal_nombre
        except: pass

        lista_personal_objs.append(persona)

        # agregar al objeto sucursal
        for s_obj in lista_sucursales:
            if s_obj.getNombre() == sucursal_nombre:
                s_obj.agregarEmpleado(persona)
                break

# ---------- Guardar todo ----------
def guardar_todo():
    guardar_json(RUTA_PER, personal_objs_a_dicts())
    guardar_json(RUTA_SUC, sucursales_objs_a_dicts())

# ---------- INTERFAZ ----------
def AdminSucursales():
    cargar_todo()

    root = tk.Tk()
    root.title("Administrar Sucursales")
    root.geometry("720x650")
    root.configure(bg="white")

    tk.Label(root, text="Administración de Sucursales", font=("Arial", 16, "bold"), bg="white").pack(pady=8)

    frame_bot = tk.Frame(root, bg="white")
    frame_bot.pack(pady=6)

    # ---------- botones ----------
    tk.Button(frame_bot, text="Guardar Sucursal", width=18, bg="#7BB0FF", command=lambda: guardar_sucursal()).grid(row=0, column=0, padx=6, pady=6)
    tk.Button(frame_bot, text="Mostrar Sucursales", width=18, bg="#7BB0FF", command=lambda: mostrar_sucursales()).grid(row=0, column=1, padx=6, pady=6)
    tk.Button(frame_bot, text="Agregar Personal", width=18, bg="#F7C97F", command=lambda: agregar_personal()).grid(row=1, column=0, padx=6, pady=6)
    tk.Button(frame_bot, text="Mostrar Personal", width=18, bg="#9BFF9F", command=lambda: mostrar_personal()).grid(row=1, column=1, padx=6, pady=6)

    # ---------- Formulario Sucursal ----------
    frame_form = tk.Frame(root, bg="#B5E3E6", bd=2, relief="groove")
    frame_form.pack(padx=10, pady=10, fill="both", expand=True)

    tk.Label(frame_form, text="Nombre de Sucursal:", bg="#B5E3E6").place(x=10, y=10)
    entry_nombre = tk.Entry(frame_form); entry_nombre.place(x=160, y=10, width=200)
    tk.Label(frame_form, text="Monto Bóveda:", bg="#B5E3E6").place(x=10, y=40)
    entry_monto = tk.Entry(frame_form); entry_monto.place(x=160, y=40, width=200)

    tk.Label(frame_form, text="--- Dirección ---", bg="#B5E3E6", font=("Arial", 9, "bold")).place(x=10, y=70)
    tk.Label(frame_form, text="Calle:", bg="#B5E3E6").place(x=10, y=100)
    entry_calle = tk.Entry(frame_form); entry_calle.place(x=60, y=100, width=160)
    tk.Label(frame_form, text="Colonia:", bg="#B5E3E6").place(x=230, y=100)
    entry_colonia = tk.Entry(frame_form); entry_colonia.place(x=290, y=100, width=140)
    tk.Label(frame_form, text="Número:", bg="#B5E3E6").place(x=440, y=100)
    entry_num = tk.Entry(frame_form); entry_num.place(x=490, y=100, width=80)

    tk.Label(frame_form, text="País:", bg="#B5E3E6").place(x=10, y=130)
    combo_pais = ttk.Combobox(frame_form, state="readonly", values=["México", "Canadá", "Estados Unidos", "Guatemala"])
    combo_pais.set("Selecciona un país"); combo_pais.place(x=60, y=130, width=160)

    tk.Label(frame_form, text="Estado:", bg="#B5E3E6").place(x=240, y=130)
    entry_estado = tk.Entry(frame_form); entry_estado.place(x=290, y=130, width=140)

    tk.Label(frame_form, text="Teléfono:", bg="#B5E3E6").place(x=10, y=160)
    entry_tel_suc = tk.Entry(frame_form); entry_tel_suc.place(x=80, y=160, width=120)

    tk.Label(frame_form, text="Compañía:", bg="#B5E3E6").place(x=230, y=160)
    combo_comp = ttk.Combobox(frame_form, state="readonly", values=["Telcel", "Movistar", "AT&T", "Unefon"])
    combo_comp.set("Selecciona compañía telefónica"); combo_comp.place(x=300, y=160, width=140)

    # ---------- Funciones ----------
    def guardar_sucursal():
        nombre = entry_nombre.get()
        monto = entry_monto.get()
        calle = entry_calle.get()
        colonia = entry_colonia.get()
        numero = entry_num.get()
        pais = combo_pais.get()
        estado = entry_estado.get()
        telefono = entry_tel_suc.get()
        compania = combo_comp.get()

        if nombre == "":
            messagebox.showinfo("Aviso", "Escribe nombre de sucursal.")
            return

        s_obj = Sucursales(nombre, monto, calle, colonia, numero, pais, estado, telefono, compania, [])
        lista_sucursales.append(s_obj)
        guardar_json(RUTA_SUC, sucursales_objs_a_dicts())
        messagebox.showinfo("Listo", "Sucursal guardada.")
        entry_nombre.delete(0, tk.END); entry_monto.delete(0, tk.END)
        entry_calle.delete(0, tk.END); entry_colonia.delete(0, tk.END); entry_num.delete(0, tk.END)
        combo_pais.set("Selecciona un país"); entry_estado.delete(0, tk.END)
        entry_tel_suc.delete(0, tk.END); combo_comp.set("Selecciona compañía telefónica")

    def agregar_personal():
        if not lista_sucursales:
            messagebox.showinfo("Aviso", "Registra una sucursal primero.")
            return

        top = tk.Toplevel()
        top.title("Agregar Personal")
        top.geometry("500x650")
        top.configure(bg="white")

        tk.Label(top, text="Sucursal:", bg="white").pack(pady=2)
        cb_suc = ttk.Combobox(top, state="readonly", values=[s.getNombre() for s in lista_sucursales])
        cb_suc.pack(pady=2)

        tk.Label(top, text="Puesto:", bg="white").pack(pady=2)
        cb_puesto = ttk.Combobox(top, state="readonly", values=["Gerente", "Cajero", "Cliente"])
        cb_puesto.pack(pady=2)

        tk.Label(top, text="--- Datos personales ---", font=("Arial", 10, "bold"), bg="white").pack(pady=6)
        tk.Label(top, text="Nombre:", bg="white").pack(); e_nombre = tk.Entry(top); e_nombre.pack(pady=2)
        tk.Label(top, text="Teléfono:", bg="white").pack(); e_tel = tk.Entry(top); e_tel.pack(pady=2)
        tk.Label(top, text="Dirección:", bg="white").pack(); e_dir = tk.Entry(top); e_dir.pack(pady=2)
        tk.Label(top, text="País:", bg="white").pack(); e_pais = tk.Entry(top); e_pais.pack(pady=2)
        tk.Label(top, text="RFC:", bg="white").pack(); e_rfc = tk.Entry(top); e_rfc.pack(pady=2)

        tk.Label(top, text="--- Datos extra (solo los que aplican) ---", font=("Arial", 10, "bold"), bg="white").pack(pady=6)
        tk.Label(top, text="Número de caja (Cajero):", bg="white").pack(); e_numc = tk.Entry(top); e_numc.pack(pady=2)
        tk.Label(top, text="Ocupación (Cliente):", bg="white").pack(); e_ocup = tk.Entry(top); e_ocup.pack(pady=2)
        tk.Label(top, text="Tipo de cuenta (Cliente):", bg="white").pack(); e_tipo = tk.Entry(top); e_tipo.pack(pady=2)
        tk.Label(top, text="Clave acceso (Gerente):", bg="white").pack(); e_clave = tk.Entry(top); e_clave.pack(pady=2)

        def guardar_persona():
            suc_name = cb_suc.get()
            puesto = cb_puesto.get()
            nombre = e_nombre.get()
            telefono = e_tel.get()
            direccion = e_dir.get()
            pais = e_pais.get()
            rfc = e_rfc.get()
            numc = e_numc.get()
            ocup = e_ocup.get()
            tipoCuenta = e_tipo.get()
            clave = e_clave.get()

            if suc_name == "" or puesto == "" or nombre == "":
                messagebox.showinfo("Aviso", "Selecciona sucursal, puesto y escribe nombre.")
                return

            if puesto == "Gerente":
                persona = Gerente(nombre, telefono, direccion, pais, rfc)
                try: persona.claveDeAcceso = clave
                except: pass
            elif puesto == "Cajero":
                persona = Cajero(nombre, telefono, direccion, pais, rfc, numc)
            else:
                persona = Cliente(nombre, telefono, direccion, pais, rfc, ocup, tipoCuenta)

            try: persona.sucursal = suc_name
            except: pass

            lista_personal_objs.append(persona)
            for s_obj in lista_sucursales:
                if s_obj.getNombre() == suc_name:
                    s_obj.agregarEmpleado(persona)
                    break

            guardar_json(RUTA_PER, personal_objs_a_dicts())
            guardar_json(RUTA_SUC, sucursales_objs_a_dicts())
            messagebox.showinfo("Listo", "Personal guardado.")
            top.destroy()

        tk.Button(top, text="Guardar personal", bg="#7BB0FF", width=20, command=guardar_persona).pack(pady=10)

    def mostrar_sucursales():
        if not lista_sucursales:
            messagebox.showinfo("Aviso", "No hay sucursales.")
            return
        for s in lista_sucursales:
            nombres = []
            try: empleados = s.getEmpleados()
            except: empleados = []
            for emp in empleados:
                nom = getattr(emp, "nombre", str(emp))
                nombres.append(nom)

            info = (
                f"Sucursal: {s.getNombre()}\n"
                f"Monto: {s.getMontoBoveda()}\n"
                f"Dirección: {s._Sucursales__calle} #{s._Sucursales__numero}, {s._Sucursales__colonia}, {s._Sucursales__estado}, {s._Sucursales__pais}\n"
                f"Tel: {s._Sucursales__telefono} ({s._Sucursales__companiaTel})\n\n"
                f"Empleados:\n" + (", ".join(nombres) if nombres else "Sin empleados")
            )
            messagebox.showinfo("Sucursal", info)

    def mostrar_personal():
        if not lista_personal_objs:
            messagebox.showinfo("Aviso", "No hay personal registrado.")
            return
        for p in lista_personal_objs:
            tipo = p.__class__.__name__
            info = f"Tipo: {tipo}\n\n{p.mostrar_informacion()}"
            messagebox.showinfo("Personal", info)

    root.mainloop()

# Ejecutar la ventana si se corre este archivo directamente
if __name__ == "__main__":
    AdminSucursales()



