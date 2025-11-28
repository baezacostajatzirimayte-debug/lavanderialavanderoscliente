import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

# Intentar importar PIL (Pillow)
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ------------------------------
# PALETA DE COLORES (Alto Contraste y Visibilidad Oscura)
# ------------------------------
AZUL_OSCURO = "#001F3F"
VERDE_ESMERALDA = "#008080"
VERDE_OSCURO = "#004D4D"
AZUL_CLARO = "#F0FFFF"
BLANCO_PURO = "white"
GRIS_TEXTO = "#222222"

# ------------------------------
# ARREGLOS / DATOS DEL SISTEMA
# ------------------------------
usuarios = {
    "cliente": {
        "nombre": "Cliente Frecuente",
        "correo": "cliente.frecuente@mail.com",
        "telefono": "5512345678",
        "password": "1234",
        "direccion": "Calle Ficción #123, Col. Limpio",
        "historial": [],
        "facturas": [],
        "imagen_path": None  # ruta de imagen del perfil si el usuario la sube
    }
}
pedidos = []
contactos = []
usuario_actual = {"username": None}

# ------------------------------
# PRECIOS SIMULADOS
# ------------------------------
TARIFA_BASE_KG = 25.0
COSTO_DOMICILIO = 45.0
COSTOS_SERVICIOS = {
    "Servicio completo (Lavado/Secado)": 1.0,
    "Tintorería": 2.5,
    "Industrial": 1.8,
    "Ecológica (Ahorro de Agua)": 1.3
}

# ------------------------------
# MAPA DE IMÁGENES POR VISTA (archivos locales)
# ------------------------------
IMAGENES_VISTA = {
    "inicio": "Lavanderia.png",
    "servicios": "lavadoras.png",
    "pago": "pagos.png",
    "historial": "historial.png",
    "registro": "registro.png",
    "login": "login.png", # Corregido a .png por consistencia (originalmente era .py)
    "perfil": "perfil.png",
    "contacto": "contacto.png"
}

def load_image_for_view(view_key, size=(300, 200)):
    """
    Retorna una tupla (PhotoImage, ruta) o (None, None) si no es posible cargar.
    - view_key: clave en IMAGENES_VISTA
    - size: (ancho, alto) al que se redimensiona la imagen (si PIL está disponible)
    """
    if not PIL_AVAILABLE:
        return None, None

    filename = IMAGENES_VISTA.get(view_key)
    if not filename:
        return None, None

    # Buscar en el directorio actual y en carpeta 'images' por si existe
    posibles_rutas = [filename, os.path.join("images", filename)]
    found = None
    for p in posibles_rutas:
        if os.path.isfile(p):
            found = p
            break
    if not found:
        return None, None

    try:
        img = Image.open(found)
        img.thumbnail(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        return photo, found
    except Exception:
        return None, None

def cargar_logo(size=(80, 80)):
    """
    Intenta cargar el logo (inicio) y retorna PhotoImage o None.
    """
    if not PIL_AVAILABLE:
        return None
    photo, path = load_image_for_view("inicio", size=size)
    return photo

# Inicializa logo
LOGO_IMG = cargar_logo(size=(80, 80))


class LavanderosWebApp:
    def __init__(self, root):
        self.root = root
        root.title("Lavandería Lavanderos")
        # MODIFICACIÓN: Ventana más grande para que los botones se vean mejor
        root.geometry("1200x800")
        root.configure(bg=AZUL_CLARO)

        # cache de imágenes para evitar GC
        self.images = {}

        # Variables de control para el formulario de servicios
        self.kilos = tk.StringVar(value="5")
        self.tipo_servicio = tk.StringVar(value="Servicio completo (Lavado/Secado)")
        self.direccion_servicio = tk.StringVar(value="Inicia sesión para usar o editar la dirección")
        self.es_domicilio = tk.BooleanVar(value=True)

        self.current_view_image_ref = None

        # --- ESTILOS ---
        self.style = ttk.Style()
        self.style.configure("Content.TFrame", background=BLANCO_PURO)
        self.style.configure("TLabel", background=BLANCO_PURO, foreground=GRIS_TEXTO, font=('Arial', 12))
        self.style.configure("TCheckbutton", background=BLANCO_PURO, foreground=GRIS_TEXTO, font=('Arial', 12))

        self.style.configure("Header.TFrame", background=AZUL_OSCURO)
        self.style.configure("Header.TLabel", background=AZUL_OSCURO, foreground=BLANCO_PURO, font=('Arial', 20, 'bold'))

        # MODIFICACIÓN: Reducimos padding y fuente para botones de navegación
        self.style.configure("Nav.TButton", background=AZUL_CLARO, foreground=GRIS_TEXTO, font=('Arial', 10, 'bold'), padding=[10, 8], relief="flat")
        self.style.map("Nav.TButton",
                       background=[('active', VERDE_ESMERALDA), ('pressed', VERDE_OSCURO)],
                       foreground=[('active', BLANCO_PURO), ('pressed', BLANCO_PURO)])

        self.style.configure("TButton", background=VERDE_ESMERALDA, foreground=GRIS_TEXTO, font=('Arial', 16, 'bold'), padding=15, relief="raised")
        self.style.map("TButton",
                       background=[('active', VERDE_OSCURO)],
                       foreground=[('active', BLANCO_PURO)])

        # --- ESTRUCTURA ---
        self.crear_encabezado()
        
        # MODIFICACIÓN: Añadimos el footer antes del content_frame para que este se ajuste al espacio restante.
        self.crear_footer()

        self.content_frame = ttk.Frame(root, padding=40, style="Content.TFrame")
        self.content_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.show_inicio()

    # --- Implementación del Menú Hamburguesa ☰ ---
    def show_hamburger_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg=BLANCO_PURO, fg=GRIS_TEXTO, font=('Arial', 12, 'bold'))

        menu.add_command(label="🏠 Inicio", command=self.show_inicio)
        menu.add_command(label="🧺 Servicios", command=self.show_register_order)
        menu.add_command(label="📞 Contacto", command=self.show_contact_form)

        if not usuario_actual["username"]:
            menu.add_command(label="💳 Mi Historial de Pagos (Login Requerido)", state=tk.DISABLED)
        else:
            menu.add_command(label="💳 Mi Historial de Pagos", command=self.show_payment_history)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def crear_encabezado(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", height=100)
        header_frame.pack(fill="x")

        title_nav_bar_frame = ttk.Frame(header_frame, style="Header.TFrame")
        title_nav_bar_frame.pack(fill="x", pady=5)

        # 1. Logo (Extrema Izquierda)
        if LOGO_IMG:
            lbl_logo = tk.Label(title_nav_bar_frame, image=LOGO_IMG, bg=AZUL_OSCURO)
            lbl_logo.image = LOGO_IMG
            lbl_logo.pack(side="left", padx=15, pady=5)
            # guardar en cache
            self.images['logo'] = LOGO_IMG

        # 2. Título
        self.header_title = ttk.Label(title_nav_bar_frame, text="LAVANDERÍA LAVANDEROS", style="Header.TLabel")
        self.header_title.pack(side="left", padx=(5, 40), pady=10)

        # 3. Menú Hamburguesa
        self.hamburger_btn = ttk.Button(title_nav_bar_frame,
                                        text="☰ Menú",
                                        style="Nav.TButton",
                                        command=lambda: self.hamburger_btn.event_generate('<Button-1>'))
        self.hamburger_btn.bind('<Button-1>', self.show_hamburger_menu)
        self.hamburger_btn.pack(side="left", padx=10)

        # 4. Navegación de Usuario (Extrema Derecha)
        self.user_nav_frame = ttk.Frame(title_nav_bar_frame, style="Header.TFrame")
        self.user_nav_frame.pack(side="right", padx=15)

        self.update_user_nav()

    def crear_footer(self):
        # Implementación del pie de página
        footer = tk.Frame(self.root, bg=AZUL_OSCURO, height=60)
        footer.pack(fill="x", side="bottom")

        tk.Label(footer, text="Lavandería Lavanderos - Cuidado Profesional a Domicilio",
                 fg=BLANCO_PURO, bg=AZUL_OSCURO, font=('Arial', 10, 'bold')).pack(pady=(5, 2))

        social_frame = tk.Frame(footer, bg=AZUL_OSCURO)
        social_frame.pack(pady=5)

        tk.Label(social_frame, text="Síguenos: 📘 Facebook | 📸 Instagram | 📞 +52 123 456 7890",
                 fg=AZUL_CLARO, bg=AZUL_OSCURO, font=('Arial', 9)).pack()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_user_nav(self):
        for widget in self.user_nav_frame.winfo_children():
            widget.destroy()
        username = usuario_actual["username"]

        if username:
            # saludo como tk.Label para controlar bg/fg
            saludo = tk.Label(self.user_nav_frame, text=f"Hola, {usuarios[username]['nombre'].split()[0]}",
                              bg=AZUL_OSCURO, fg=BLANCO_PURO, font=('Arial', 11))
            saludo.pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="👤 Perfil", command=self.show_edit_profile, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="❌ Salir", command=self.logout, style="Nav.TButton").pack(side="left", padx=5)
        else:
            # MODIFICACIÓN: Estos botones se verán mejor con el nuevo padding y fuente.
            ttk.Button(self.user_nav_frame, text="🔑 Login", command=self.show_login, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="➕ Crear Cuenta", command=self.show_register, style="Nav.TButton").pack(side="left", padx=5)

    # --- Pantalla Principal ---
    def show_inicio(self):
        self.clear_content()
        self.header_title.config(text="LAVANDERÍA LAVANDEROS")

        img_tk, _ = load_image_for_view("inicio", size=(400, 200)) # Reducido un poco para la nueva ventana
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['inicio'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(10, 0))

        ttk.Label(self.content_frame,
                  text="✨ ¡Tu Ropa, Como Nueva, Sin Esfuerzo! ✨",
                  font=('Arial', 20, 'bold'), # Reducida fuente
                  ).pack(pady=(25, 15))

        ttk.Label(self.content_frame,
                  text="Somos Lavandería Lavanderos, dedicados a ofrecer un servicio de cuidado textil profesional, rápido y conveniente. Desde nuestro inicio, nos hemos comprometido a utilizar procesos ecológicos y detergentes de alta calidad para garantizar que tu ropa reciba el mejor trato. Nuestro servicio a domicilio elimina la molestia de la lavandería de tu vida, permitiéndote concentrarte en lo importante.",
                  font=('Arial', 12), # Reducida fuente
                  justify="center",
                  wraplength=650).pack(pady=(0, 20)) # Reducido wraplength

        ttk.Button(self.content_frame, text="🧺 ¡Solicitar Servicio Ahora!", command=self.show_register_order).pack(pady=10)

        if not usuario_actual["username"]:
            login_quick_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
            login_quick_frame.pack(pady=15, padx=50, fill="x")
            ttk.Label(login_quick_frame, text="¿Ya eres cliente? Inicia sesión rápido aquí:", font=('Arial', 11, 'bold')).pack()

            quick_buttons_frame = ttk.Frame(login_quick_frame, style="Content.TFrame")
            quick_buttons_frame.pack(pady=5)
            ttk.Button(quick_buttons_frame, text="🔑 Iniciar Sesión", command=self.show_login, style="Nav.TButton").pack(side="left", padx=10)
            ttk.Button(quick_buttons_frame, text="➕ Crear Cuenta", command=self.show_register, style="Nav.TButton").pack(side="left", padx=10)

    # --- Pantalla de Servicios ---
    def show_register_order(self):
        self.clear_content()
        self.header_title.config(text="CONTRATAR SERVICIOS")

        is_logged_in = bool(usuario_actual["username"])

        if is_logged_in:
            user = usuarios[usuario_actual["username"]]
            self.direccion_servicio.set(user["direccion"])
        else:
            self.direccion_servicio.set("Inicia sesión para usar o editar la dirección")

        img_tk, _ = load_image_for_view("servicios", size=(300, 100))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['servicios'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 15))

        form_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="📝 Detalle de tu Pedido",
                  font=("Arial", 16, 'bold'), foreground=AZUL_OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        r = 1
        ttk.Label(form_frame, text="1. Kilos de Ropa (kg):", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(form_frame, textvariable=self.kilos, width=20, font=('Arial', 11)).grid(row=r, column=1, sticky="w", padx=10, pady=5)
        r += 1

        ttk.Label(form_frame, text="2. Tipo de Servicio:", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=5)
        servicios_opciones = list(COSTOS_SERVICIOS.keys())
        service_combo = ttk.Combobox(form_frame, textvariable=self.tipo_servicio, values=servicios_opciones, state="readonly", width=30, font=('Arial', 11))
        service_combo.grid(row=r, column=1, sticky="w", padx=10, pady=5)
        r += 1

        def toggle_direccion():
            state = tk.NORMAL if self.es_domicilio.get() and is_logged_in else tk.DISABLED
            if not is_logged_in:
                entry_direccion.config(state=tk.DISABLED)
            else:
                entry_direccion.config(state=state)

            if not self.es_domicilio.get():
                self.direccion_servicio.set("Presencial")
            elif is_logged_in:
                self.direccion_servicio.set(usuarios[usuario_actual["username"]]["direccion"])
            else:
                self.direccion_servicio.set("Inicia sesión para usar o editar la dirección")

        ttk.Label(form_frame, text="3. Modalidad:", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=5)
        check_domicilio = ttk.Checkbutton(form_frame, text="Servicio a Domicilio (Recolección y Entrega)", variable=self.es_domicilio, command=toggle_direccion, style='TCheckbutton')
        check_domicilio.grid(row=r, column=1, sticky="w", padx=10, pady=5)
        r += 1

        ttk.Label(form_frame, text="Dirección de Servicio:", font=('Arial', 11, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=5)
        entry_direccion = ttk.Entry(form_frame, textvariable=self.direccion_servicio, width=35, font=('Arial', 11))
        entry_direccion.grid(row=r, column=1, sticky="w", padx=10, pady=5)

        entry_direccion.config(state=tk.DISABLED if not is_logged_in or not self.es_domicilio.get() else tk.NORMAL)
        r += 1

        def go_to_payment_or_login():
            if not is_logged_in:
                messagebox.showwarning("Acceso Requerido", "Debes iniciar sesión para proceder al pago y generar tu pedido.")
                return self.show_login()

            try:
                kilos_val = float(self.kilos.get())
                if kilos_val <= 0:
                    messagebox.showerror("Error", "Por favor, ingresa un peso válido (mayor a 0 kg).")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de kilos inválido.")
                return

            domicilio_val = self.es_domicilio.get()
            direccion_actual = self.direccion_servicio.get().strip()
            if domicilio_val and (not direccion_actual or direccion_actual == "Inicia sesión para usar o editar la dirección"):
                messagebox.showerror("Error", "Por favor, ingresa una dirección de servicio válida.")
                return

            servicio_val = self.tipo_servicio.get()
            total = self.calcular_total(kilos_val, servicio_val, domicilio_val)

            current_pedido = {
                "id": len(pedidos) + 1,
                "cliente": usuario_actual["username"],
                "kilos": kilos_val,
                "servicio": servicio_val,
                "domicilio": domicilio_val,
                "direccion": self.direccion_servicio.get() if domicilio_val else "Presencial",
                "total": total,
                "estado": "Pendiente de Pago"
            }
            pedidos.append(current_pedido)
            self.show_payment(current_pedido)

        ttk.Button(self.content_frame,
                   text="💰 Proceder al Pago",
                   command=go_to_payment_or_login,
                   style="TButton").pack(pady=20)

        if not is_logged_in:
            ttk.Label(self.content_frame, text="⚠ Inicia sesión para habilitar el botón de pago y tu dirección a domicilio.",
                      font=('Arial', 11, 'italic')).pack(pady=5)

    # --- Pago ---
    def calcular_total(self, kilos, servicio, domicilio):
        try:
            kilos = float(kilos)
        except ValueError:
            return 0.0
        multiplicador = COSTOS_SERVICIOS.get(servicio, 1.0)
        subtotal = kilos * TARIFA_BASE_KG * multiplicador
        costo_envio = COSTO_DOMICILIO if domicilio else 0.0
        return subtotal + costo_envio

    def show_payment(self, pedido):
        self.clear_content()
        self.header_title.config(text="PROCESO DE PAGO")

        img_tk, _ = load_image_for_view("pago", size=(200, 80))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['pago'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 15))

        payment_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        payment_frame.pack(pady=10)

        ttk.Label(payment_frame, text="💸 Resumen y Forma de Pago", font=("Arial", 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(payment_frame, text="TOTAL A PAGAR:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(payment_frame, text=f"${pedido['total']:.2f} MXN", font=('Arial', 16, 'bold')).grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(payment_frame, text="Forma de Pago:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        metodo_pago = tk.StringVar(value="Tarjeta de Crédito")
        formas = ["Tarjeta de Crédito", "Transferencia Bancaria", "Efectivo (en Recolección)"]
        combo_pago = ttk.Combobox(payment_frame, textvariable=metodo_pago, values=formas, state="readonly", width=25, font=('Arial', 11))
        combo_pago.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        def realizar_pago():
            pedido["estado"] = "Pagado - " + metodo_pago.get()
            if pedido["cliente"]:
                usuarios[pedido["cliente"]]["facturas"].append(pedido)

            self.clear_content()
            self.header_title.config(text="TRANSACCIÓN EXITOSA")

            img_tk2, _ = load_image_for_view("pago", size=(200, 80))
            if img_tk2:
                self.current_view_image_ref = img_tk2
                self.images['pago2'] = img_tk2
                lbl_img = tk.Label(self.content_frame, image=img_tk2, bg=BLANCO_PURO)
                lbl_img.pack(pady=(0, 15))

            ttk.Label(self.content_frame, text="🎉 ¡Pago Confirmado! 🎉", font=("Arial", 22, 'bold'), foreground=VERDE_ESMERALDA).pack(pady=15)
            ttk.Label(self.content_frame, text=f"Tu pedido ID {pedido['id']} ha sido agendado. Total pagado: ${pedido['total']:.2f}",
                      ).pack(pady=5)

            final_btn_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
            final_btn_frame.pack(pady=20)

            ttk.Button(final_btn_frame, text="🖨️ Imprimir Comprobante", command=lambda: messagebox.showinfo("Imprimir", f"Imprimiendo comprobante del Pedido ID {pedido['id']}...")).pack(side="left", padx=10)
            ttk.Button(final_btn_frame, text="💳 Ver Historial de Pagos", command=self.show_payment_history).pack(side="left", padx=10)
            ttk.Button(self.content_frame, text="🏠 Volver al Inicio", command=self.show_inicio).pack(pady=10)

        ttk.Button(self.content_frame, text="✅ Botón para Pagar", command=realizar_pago, style="TButton").pack(pady=20)
        ttk.Button(self.content_frame, text="Volver a Servicios", command=self.show_register_order, style="Nav.TButton").pack()

    # --- Historial ---
    def show_payment_history(self):
        self.clear_content()
        self.header_title.config(text="HISTORIAL DE PAGOS")

        username = usuario_actual["username"]
        if not username:
            messagebox.showwarning("Acceso Requerido", "Debes iniciar sesión para ver tu historial.")
            return self.show_login()

        historial = usuarios[username]["facturas"]

        img_tk, _ = load_image_for_view("historial", size=(300, 100))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['historial'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 15))

        historial_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=15)
        historial_frame.pack(pady=10, fill="x", padx=40)

        ttk.Label(historial_frame, text="📋 Mis Facturas y Pagos", font=("Arial", 14, 'bold')).pack(pady=5)

        if not historial:
            ttk.Label(historial_frame, text="No se han encontrado pagos o facturas en tu historial.", font=('Arial', 11, 'italic')).pack(pady=10)
        else:
            for item in historial:
                info = (f"ID: {item['id']} | Servicio: {item['servicio']} | Kilos: {item['kilos']} kg | "
                        f"Total: ${item['total']:.2f} | Estado: {item['estado']}")
                ttk.Label(historial_frame, text=info, justify="left", wraplength=600).pack(anchor="w", pady=3)

        ttk.Button(self.content_frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack(pady=15)

    # --- Registro ---
    def show_register(self):
        self.clear_content()
        self.header_title.config(text="CREAR CUENTA")

        img_tk, _ = load_image_for_view("registro", size=(150, 150))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['registro'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 5))

        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=15)
        frame.pack(pady=15)
        ttk.Label(frame, text="Crear Cuenta de Cliente", font=("Arial", 14, "bold")).pack(pady=5)
        labels_texts = ["Usuario (Para Login):", "Nombre completo:", "Correo:", "Teléfono:", "Dirección:", "Contraseña:"]
        entries = []
        for text in labels_texts:
            ttk.Label(frame, text=text, font=('Arial', 11)).pack()
            e = ttk.Entry(frame, width=35)
            if "Contraseña" in text:
                e.config(show="*")
            e.pack()
            entries.append(e)

        def registrar():
            u, n, c, t, d, p = [e.get().strip() for e in entries]
            if u in usuarios:
                messagebox.showerror("Error", "Ese usuario ya existe.")
                return
            if not all([u, n, c, t, d, p]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return
            usuarios[u] = {"nombre": n, "correo": c, "telefono": t, "password": p, "direccion": d, "historial": [], "facturas": [], "imagen_path": None}
            messagebox.showinfo("Registrado", "Cuenta creada con éxito. Ya puedes iniciar sesión.")
            self.show_login()

        ttk.Button(frame, text="✅ Registrar", command=registrar).pack(pady=10)

    # --- Login ---
    def show_login(self):
        self.clear_content()
        self.header_title.config(text="LOGIN DE CLIENTE")

        img_tk, _ = load_image_for_view("login", size=(150, 150))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['login'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 5))

        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=15)
        frame.pack(pady=15)
        ttk.Label(frame, text="🔑 Iniciar Sesión", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(frame, text="Usuario:", font=('Arial', 11)).pack()
        user_entry = ttk.Entry(frame, width=30)
        user_entry.pack()
        ttk.Label(frame, text="Contraseña:", font=('Arial', 11)).pack()
        pass_entry = ttk.Entry(frame, show="*", width=30)
        pass_entry.pack()

        def validar():
            u = user_entry.get().strip()
            p = pass_entry.get().strip()
            if u in usuarios and usuarios[u]["password"] == p:
                usuario_actual["username"] = u
                messagebox.showinfo("Éxito", f"Bienvenido, {usuarios[u]['nombre'].split()[0]}!")
                self.update_user_nav()
                self.show_inicio()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                pass_entry.delete(0, tk.END)

        ttk.Button(frame, text="Ingresar", command=validar).pack(pady=10)

    # --- Editar perfil (incluye subir imagen) ---
    def show_edit_profile(self):
        self.clear_content()
        username = usuario_actual["username"]
        if not username:
            self.show_login()
            return
        self.header_title.config(text="EDITAR PERFIL DE CLIENTE")
        user = usuarios[username]

        img_tk, _ = load_image_for_view("perfil", size=(150, 150))
        profile_img_label = None
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['perfil_default'] = img_tk
            profile_img_label = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            profile_img_label.pack(pady=(0, 5))

        # Si el usuario tiene imagen cargada, mostrarla
        if user.get("imagen_path") and PIL_AVAILABLE and os.path.isfile(user["imagen_path"]):
            try:
                img_user = Image.open(user["imagen_path"])
                img_user.thumbnail((150, 150), Image.LANCZOS)
                photo_user = ImageTk.PhotoImage(img_user)
                self.images['perfil_user'] = photo_user
                if profile_img_label:
                    profile_img_label.config(image=photo_user)
                    profile_img_label.image = photo_user
                else:
                    profile_img_label = tk.Label(self.content_frame, image=photo_user, bg=BLANCO_PURO)
                    profile_img_label.pack(pady=(0, 5))
            except Exception:
                pass

        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=15)
        frame.pack(pady=15)
        ttk.Label(frame, text="✏️ Datos de Mi Cuenta", font=("Arial", 14, "bold")).pack(pady=5)
        fields = ["Nombre completo", "Correo", "Teléfono", "Dirección"]
        entries = {}
        keys_map = {"Nombre completo": "nombre", "Correo": "correo", "Teléfono": "telefono", "Dirección": "direccion"}
        for text in fields:
            key = keys_map[text]
            ttk.Label(frame, text=f"{text}:", font=('Arial', 11)).pack(pady=(3, 0))
            e = ttk.Entry(frame, width=40)
            e.insert(0, user[key])
            e.pack()
            entries[key] = e

        def guardar():
            changes_made = False
            for key, entry in entries.items():
                new_value = entry.get().strip()
                if new_value != user[key]:
                    user[key] = new_value
                    changes_made = True
            if changes_made:
                messagebox.showinfo("Guardado", "Perfil actualizado con éxito.")
            else:
                messagebox.showinfo("Sin Cambios", "No se detectaron modificaciones en el perfil.")
            self.show_inicio()

        def subir_imagen_perfil():
            if not PIL_AVAILABLE:
                messagebox.showwarning("Pillow no disponible", "Para subir y mostrar imágenes instala Pillow: pip install pillow")
                return
            ruta = filedialog.askopenfilename(title="Seleccionar imagen de perfil", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
            if not ruta:
                return
            try:
                # Guardar ruta en usuario
                usuarios[username]['imagen_path'] = ruta
                # Mostrar preview inmediato
                img_user = Image.open(ruta)
                img_user.thumbnail((150, 150), Image.LANCZOS)
                photo_user = ImageTk.PhotoImage(img_user)
                self.images['perfil_user'] = photo_user
                # Si ya existe etiqueta, actualizarla; si no, crearla arriba del frame
                nonlocal_label = None
                # buscar si existe label previamente creado (primer widget del content_frame si es imagen)
                for w in self.content_frame.winfo_children():
                    if isinstance(w, tk.Label) and getattr(w, "image", None) is not None:
                        nonlocal_label = w
                        break
                if nonlocal_label:
                    nonlocal_label.config(image=photo_user)
                    nonlocal_label.image = photo_user
                else:
                    lbl = tk.Label(self.content_frame, image=photo_user, bg=BLANCO_PURO)
                    lbl.pack(pady=(0, 5))
                    lbl.image = photo_user
                messagebox.showinfo("Imagen subida", "Imagen de perfil cargada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="✅ Guardar Cambios", command=guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📷 Subir Imagen de Perfil", command=subir_imagen_perfil).pack(side="left", padx=5)

    # --- Contacto ---
    def show_contact_form(self):
        self.clear_content()
        self.header_title.config(text="FORMULARIO DE CONTACTO")

        img_tk, _ = load_image_for_view("contacto", size=(200, 100))
        if img_tk:
            self.current_view_image_ref = img_tk
            self.images['contacto'] = img_tk
            lbl_img = tk.Label(self.content_frame, image=img_tk, bg=BLANCO_PURO)
            lbl_img.pack(pady=(0, 5))

        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=15)
        frame.pack(pady=15)
        ttk.Label(frame, text="✉️ Déjanos un Mensaje", font=("Arial", 14, "bold")).pack(pady=5)
        fields = {"Tu Nombre": tk.StringVar(), "Tu Email": tk.StringVar(), "Asunto": tk.StringVar()}
        entries = {}
        for text, var in fields.items():
            ttk.Label(frame, text=f"{text}:", font=('Arial', 11)).pack(pady=(3, 0))
            e = ttk.Entry(frame, textvariable=var, width=40)
            e.pack()
            entries[text] = e
        ttk.Label(frame, text="Mensaje:", font=('Arial', 11)).pack(pady=(3, 0))
        mensaje_text = tk.Text(frame, height=5, width=40)
        mensaje_text.pack()

        def send_contact():
            data = {k: v.get().strip() for k, v in fields.items()}
            data["Mensaje"] = mensaje_text.get("1.0", tk.END).strip()
            if not all(data.values()):
                messagebox.showerror("Error", "Todos los campos del formulario son obligatorios.")
                return
            contactos.append(data)
            messagebox.showinfo("Mensaje Enviado", f"Mensaje enviado por {data['Tu Nombre']}. Pronto nos pondremos en contacto.")
            self.show_inicio()

        ttk.Button(frame, text="Enviar Mensaje", command=send_contact).pack(pady=10)

    def logout(self):
        self.direccion_servicio.set("Inicia sesión para usar o editar la dirección")
        self.es_domicilio.set(True)
        usuario_actual["username"] = None
        messagebox.showinfo("Sesión cerrada", "Has cerrado la sesión con éxito.")
        self.update_user_nav()
        self.show_inicio()

# --- INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LavanderosWebApp(root)
    root.mainloop()
