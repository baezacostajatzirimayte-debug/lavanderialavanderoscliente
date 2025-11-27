import tkinter as tk
from tkinter import messagebox
from datetime import datetime
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ------------------------------
# PALETA (TONOS AZULES)
# ------------------------------
AZUL_OSCURO = "#0D3B66"
AZUL_MEDIO = "#1E5F9F"
AZUL_CLARO = "#4E89AE"
AZUL_MUY_CLARO = "#A9D6E5"
FONDO = "#EAF6FF"
TEXTO = "#ffffff"
BTN_BG = AZUL_MEDIO
BTN_HOVER = AZUL_CLARO


# ------------------------------
# CARGAR LOGO REAL
# ------------------------------
def cargar_logo():
    if not PIL_AVAILABLE:
        return None
    try:
        img = Image.open("logo_lavanderia.png")
        img = img.resize((180, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

LOGO_IMG = cargar_logo()


# ------------------------------
#  ARREGLOS / DATOS DEL SISTEMA
# ------------------------------

usuarios = {
    "cliente1": {
        "nombre": "Ana Pérez",
        "correo": "ana@gmail.com",
        "telefono": "2221234567",
        "password": "pass123",
        "direccion": "Calle Falsa 123",
        "historial": [],
        "facturas": []
    }
}

pedidos = []
contactos = []

usuario_actual = {"username": None}


# ------------------------------
# FUNCIONES DE ESTILO
# ------------------------------
def aplicar_estilo_boton(btn):
    btn.config(bg=BTN_BG, fg="white", activebackground=BTN_HOVER,
               relief="flat", bd=0, padx=8, pady=6)


def crear_encabezado(root):
    header = tk.Frame(root, bg=AZUL_OSCURO, height=100)
    header.pack(fill="x")

    # LOGO EN EL ENCABEZADO
    if LOGO_IMG:
        lbl = tk.Label(header, image=LOGO_IMG, bg=AZUL_OSCURO)
        lbl.image = LOGO_IMG
        lbl.place(x=20, y=5)
    else:
        tk.Label(header, text="Lavandería Lavanderos",
                 font=("Arial", 22, "bold"),
                 bg=AZUL_OSCURO, fg="white").place(x=20, y=30)


def crear_footer(root):
    footer = tk.Frame(root, bg=AZUL_MEDIO, height=70)
    footer.pack(fill="x", side="bottom")

    tk.Label(footer, text="Desarrollado por: Lavanderos Digital",
             fg="white", bg=AZUL_MEDIO).pack()
    tk.Label(footer, text="Contacto: info@lavanderos.mx  |  Tel: 222-000-0000",
             fg="white", bg=AZUL_MEDIO).pack()


def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()


# ------------------------------
# PANTALLA DE INICIO
# ------------------------------
def pantalla_inicio():
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Bienvenido a Lavandería Lavanderos",
             font=("Arial", 26, "bold"), bg=FONDO,
             fg=AZUL_OSCURO).pack(pady=20)

    tk.Label(frame,
             text="Servicio profesional de lavado, secado y planchado.\n"
                  "Registra tu pedido, revisa tu historial y más.",
             font=("Arial", 14), bg=FONDO, fg=AZUL_OSCURO).pack(pady=10)

    b1 = tk.Button(frame, text="Login Cliente",
                   font=("Arial", 14), width=22,
                   command=pantalla_login_cliente)
    aplicar_estilo_boton(b1)
    b1.pack(pady=8)

    b2 = tk.Button(frame, text="Crear Cuenta",
                   font=("Arial", 14), width=22,
                   command=pantalla_registro)
    aplicar_estilo_boton(b2)
    b2.pack(pady=8)

    b3 = tk.Button(frame, text="Contacto / Soporte",
                   font=("Arial", 14), width=22,
                   command=pantalla_contacto)
    aplicar_estilo_boton(b3)
    b3.pack(pady=8)

    crear_footer(root)


# ------------------------------
# LOGIN CLIENTE
# ------------------------------
def pantalla_login_cliente():
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Login Cliente",
             font=("Arial", 22, "bold"),
             bg=FONDO, fg=AZUL_OSCURO).pack(pady=12)

    tk.Label(frame, text="Usuario:", bg=FONDO, fg=AZUL_OSCURO).pack()
    usuario_entry = tk.Entry(frame, width=35)
    usuario_entry.pack()

    tk.Label(frame, text="Contraseña:", bg=FONDO, fg=AZUL_OSCURO).pack()
    pass_entry = tk.Entry(frame, show="*", width=35)
    pass_entry.pack()

    def validar():
        u = usuario_entry.get().strip()
        p = pass_entry.get().strip()

        if u in usuarios and usuarios[u]["password"] == p:
            usuario_actual["username"] = u
            messagebox.showinfo("Bienvenido", f"Hola {usuarios[u]['nombre']}!")
            pantalla_panel_cliente()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn = tk.Button(frame, text="Ingresar", width=18, command=validar)
    aplicar_estilo_boton(btn)
    btn.pack(pady=12)

    volver = tk.Button(frame, text="Volver", command=pantalla_inicio)
    aplicar_estilo_boton(volver)
    volver.pack()

    crear_footer(root)


# ------------------------------
# REGISTRO DE CLIENTE
# ------------------------------
def pantalla_registro():
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Crear Cuenta de Cliente",
             font=("Arial", 20, "bold"),
             bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    labels = ["Usuario:", "Nombre completo:", "Correo:",
              "Teléfono:", "Dirección:", "Contraseña:"]
    entries = []

    for t in labels:
        tk.Label(frame, text=t, bg=FONDO, fg=AZUL_OSCURO).pack()
        e = tk.Entry(frame, width=40)
        e.pack()
        entries.append(e)

    def registrar():
        u = entries[0].get().strip()
        if u in usuarios:
            messagebox.showerror("Error", "Ese usuario ya existe.")
            return

        usuarios[u] = {
            "nombre": entries[1].get(),
            "correo": entries[2].get(),
            "telefono": entries[3].get(),
            "direccion": entries[4].get(),
            "password": entries[5].get(),
            "historial": [],
            "facturas": []
        }

        messagebox.showinfo("Registrado", "Cuenta creada con éxito.")
        pantalla_login_cliente()

    btn = tk.Button(frame, text="Registrar", command=registrar, width=18)
    aplicar_estilo_boton(btn)
    btn.pack(pady=10)

    volver = tk.Button(frame, text="Volver", command=pantalla_inicio)
    aplicar_estilo_boton(volver)
    volver.pack()

    crear_footer(root)


# ------------------------------
# PANEL DEL CLIENTE
# ------------------------------
def pantalla_panel_cliente():
    limpiar_pantalla()
    crear_encabezado(root)

    username = usuario_actual["username"]
    user = usuarios[username]

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Bienvenido, {user['nombre']}",
             font=("Arial", 20, "bold"),
             bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    def crear_boton(txt, cmd):
        b = tk.Button(frame, text=txt, command=cmd, width=25)
        aplicar_estilo_boton(b)
        b.pack(pady=5)

    crear_boton("Registrar Pedido", lambda: pantalla_registrar_pedido(username))
    crear_boton("Mis Pedidos Activos", lambda: pantalla_pedidos_activos(username))
    crear_boton("Historial de Servicios", lambda: pantalla_historial(username))
    crear_boton("Facturas", lambda: pantalla_facturas(username))
    crear_boton("Métodos de Pago (Simulado)", lambda: pantalla_metodos_pago(username))
    crear_boton("Mi Perfil", lambda: pantalla_perfil(username))
    crear_boton("Contacto", pantalla_contacto)

    salir = tk.Button(frame, text="Cerrar Sesión",
                      command=cerrar_sesion)
    aplicar_estilo_boton(salir)
    salir.pack(pady=8)

    crear_footer(root)


# ------------------------------
# CERRAR SESIÓN
# ------------------------------
def cerrar_sesion():
    usuario_actual["username"] = None
    messagebox.showinfo("Sesión cerrada", "Has cerrado sesión.")
    pantalla_inicio()


# ------------------------------
# PANTALLA DE PERFIL
# ------------------------------
def pantalla_perfil(username):
    limpiar_pantalla()
    crear_encabezado(root)

    user = usuarios[username]

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Mi Perfil", font=("Arial", 22, "bold"),
             bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    # Entradas
    nombre = tk.Entry(frame); nombre.insert(0, user["nombre"]); nombre.pack()
    correo = tk.Entry(frame); correo.insert(0, user["correo"]); correo.pack()
    tel = tk.Entry(frame); tel.insert(0, user["telefono"]); tel.pack()
    direccion = tk.Entry(frame); direccion.insert(0, user["direccion"]); direccion.pack()

    def guardar():
        user["nombre"] = nombre.get()
        user["correo"] = correo.get()
        user["telefono"] = tel.get()
        user["direccion"] = direccion.get()
        messagebox.showinfo("Guardado", "Perfil actualizado.")
        pantalla_panel_cliente()

    btn = tk.Button(frame, text="Guardar Cambios", command=guardar)
    aplicar_estilo_boton(btn)
    btn.pack(pady=8)

    volver = tk.Button(frame, text="Volver", command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack(pady=5)

    crear_footer(root)


# ------------------------------
# REGISTRAR PEDIDO
# ------------------------------
def pantalla_registrar_pedido(username):
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Registrar Pedido",
             font=("Arial", 20, "bold"), bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    servicios = {"Lavado": tk.IntVar(), "Secado": tk.IntVar(),
                 "Planchado": tk.IntVar(), "Paquete Completo": tk.IntVar()}

    tk.Label(frame, text="Selecciona servicios:",
             bg=FONDO, fg=AZUL_OSCURO).pack()

    for s, v in servicios.items():
        tk.Checkbutton(frame, text=s, variable=v,
                       bg=FONDO).pack(anchor="w")

    tk.Label(frame, text="¿Cómo entregarás tu ropa?",
             bg=FONDO, fg=AZUL_OSCURO).pack()

    opcion = tk.StringVar(value="presencial")

    tk.Radiobutton(frame, text="Llevaré mi ropa",
                   variable=opcion, value="presencial",
                   bg=FONDO).pack(anchor="w")

    tk.Radiobutton(frame, text="Recolección a domicilio",
                   variable=opcion, value="domicilio",
                   bg=FONDO).pack(anchor="w")

    tk.Label(frame, text="Observaciones:",
             bg=FONDO, fg=AZUL_OSCURO).pack()
    obs = tk.Entry(frame, width=50)
    obs.pack()

    def enviar():
        serv = [s for s, v in servicios.items() if v.get() == 1]
        if not serv:
            messagebox.showwarning("Error", "Debes seleccionar al menos un servicio.")
            return

        pedido = {
            "cliente": username,
            "servicios": serv,
            "modo": opcion.get(),
            "observaciones": obs.get(),
            "estado": "Pendiente",
            "id": len(pedidos) + 1
        }

        pedidos.append(pedido)
        usuarios[username]["historial"].append(pedido)

        messagebox.showinfo("Registrado", f"Pedido registrado con ID {pedido['id']}")
        pantalla_panel_cliente()

    btn = tk.Button(frame, text="Enviar Pedido", command=enviar)
    aplicar_estilo_boton(btn)
    btn.pack(pady=10)

    volver = tk.Button(frame, text="Volver", command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack()

    crear_footer(root)


# ------------------------------
# PEDIDOS ACTIVOS
# ------------------------------
def pantalla_pedidos_activos(username):
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Pedidos Activos",
             font=("Arial", 20, "bold"), bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    activos = [p for p in pedidos if p["cliente"] == username and p["estado"] != "Entregado"]

    if not activos:
        tk.Label(frame, text="No tienes pedidos en proceso.",
                 bg=FONDO, fg=AZUL_OSCURO).pack()
    else:
        for p in activos:
            tk.Label(frame,
                     text=f"ID:{p['id']} - {p['servicios']} - Estado: {p['estado']}",
                     bg=FONDO, fg=AZUL_OSCURO).pack(anchor="w", padx=10)

    volver = tk.Button(frame, text="Volver", command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack(pady=10)

    crear_footer(root)


# ------------------------------
# HISTORIAL
# ------------------------------
def pantalla_historial(username):
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Historial de Servicios",
             font=("Arial", 20, "bold"), bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    h = usuarios[username]["historial"]

    if not h:
        tk.Label(frame, text="No hay historial.",
                 bg=FONDO, fg=AZUL_OSCURO).pack()
    else:
        for p in h:
            tk.Label(frame,
                     text=f"ID:{p['id']} - {p['servicios']} - Estado: {p['estado']}",
                     bg=FONDO, fg=AZUL_OSCURO).pack(anchor="w", padx=10)

    volver = tk.Button(frame, text="Volver", command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack(pady=10)

    crear_footer(root)


# ------------------------------
# FACTURAS (SIMULADO)
# ------------------------------
def pantalla_facturas(username):
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Facturas",
             font=("Arial", 20, "bold"), bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    facturas = usuarios[username]["facturas"]

    if not facturas:
        tk.Label(frame, text="No tienes facturas generadas.",
                 bg=FONDO, fg=AZUL_OSCURO).pack()
    else:
        for f in facturas:
            tk.Label(frame,
                     text=f"Factura {f['id']} - Monto: {f['monto']} - Fecha: {f['fecha']}",
                     bg=FONDO, fg=AZUL_OSCURO).pack(anchor="w", padx=10)

    def generar_factura_demo():
        factura = {
            "id": len(facturas) + 1,
            "monto": 100,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        facturas.append(factura)
        messagebox.showinfo("Factura generada",
                            f"Tu factura {factura['id']} fue creada.")
        pantalla_facturas(username)

    btn = tk.Button(frame, text="Generar factura demo", command=generar_factura_demo)
    aplicar_estilo_boton(btn)
    btn.pack(pady=10)

    volver = tk.Button(frame, text="Volver", command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack(pady=5)

    crear_footer(root)


# ------------------------------
# MÉTODOS DE PAGO (SIMULADO)
# ------------------------------
def pantalla_metodos_pago(username):
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Métodos de Pago",
             font=("Arial", 20, "bold"), bg=FONDO, fg=AZUL_OSCURO).pack(pady=8)

    def pagar(metodo):
        comp = tk.simpledialog.askstring("Comprobante",
                                         f"Inserta comprobante de {metodo}:")
        if comp:
            messagebox.showinfo("Pago registrado",
                                f"Pago con {metodo} registrado.")
        else:
            messagebox.showwarning("Error", "No se ingresó comprobante.")

    b1 = tk.Button(frame, text="Pagar con PayPal (Simulado)",
                   command=lambda: pagar("PayPal"))
    aplicar_estilo_boton(b1)
    b1.pack(pady=5)

    b2 = tk.Button(frame, text="Pagar con MercadoPago (Simulado)",
                   command=lambda: pagar("MercadoPago"))
    aplicar_estilo_boton(b2)
    b2.pack(pady=5)

    volver = tk.Button(frame, text="Volver",
                       command=pantalla_panel_cliente)
    aplicar_estilo_boton(volver)
    volver.pack(pady=10)

    crear_footer(root)


# ------------------------------
# CONTACTO
# ------------------------------
def pantalla_contacto():
    limpiar_pantalla()
    crear_encabezado(root)

    frame = tk.Frame(root, bg=FONDO)
    frame.pack(expand=True)

    tk.Label(frame, text="Contacto / Soporte",
             font=("Arial", 20, "bold"),
             bg=FONDO, fg=AZUL_OSCURO).pack(pady=10)

    tk.Label(frame, text="Nombre:", bg=FONDO, fg=AZUL_OSCURO).pack()
    nom = tk.Entry(frame, width=50); nom.pack()

    tk.Label(frame, text="Correo:", bg=FONDO, fg=AZUL_OSCURO).pack()
    cor = tk.Entry(frame, width=50); cor.pack()

    tk.Label(frame, text="Mensaje:", bg=FONDO, fg=AZUL_OSCURO).pack()
    msg = tk.Text(frame, width=60, height=6); msg.pack()

    def enviar():
        contactos.append({
            "nombre": nom.get(),
            "correo": cor.get(),
            "mensaje": msg.get("1.0", "end"),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        messagebox.showinfo("Enviado", "Gracias por contactarnos.")
        pantalla_inicio()

    b1 = tk.Button(frame, text="Enviar", command=enviar)
    aplicar_estilo_boton(b1)
    b1.pack(pady=8)

    b2 = tk.Button(frame, text="Volver", command=pantalla_inicio)
    aplicar_estilo_boton(b2)
    b2.pack()

    crear_footer(root)


# ------------------------------
# INICIO DEL PROGRAMA
# ------------------------------
root = tk.Tk()
root.title("Lavandería Lavanderos - Sistema")
root.geometry("980x680")
root.configure(bg=FONDO)

pantalla_inicio()

root.mainloop()