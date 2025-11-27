import tkinter as tk
from tkinter import ttk, messagebox
try:
    from PIL import Image, ImageTk
    # Esta línea simula la carga de una imagen si tienes PIL instalado
    # Asegúrate de tener una imagen llamada 'logo_lavanderia.png' en el mismo directorio.
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ------------------------------
# PALETA DE COLORES (Alto Contraste y Visibilidad Máxima)
# ------------------------------
AZUL_OSCURO = "#031F4B"       # Encabezado y texto principal
AZUL_PRINCIPAL = "#007BFF"    # Botones de Acción (BG, Azul eléctrico)
AZUL_CLARO = "#E0F7FF"        # Fondo de la Aplicación (Cian muy claro)
BLANCO_PURO = "white"         # Texto y Fondo de Contenido
GRIS_TEXTO = "#333333"        # Texto secundario

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
        "facturas": [] 
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

def cargar_logo():
    if not PIL_AVAILABLE: return None
    try:
        img = Image.open("logo_lavanderia.png") 
        img = img.resize((80, 80))
        return ImageTk.PhotoImage(img)
    except Exception: return None

LOGO_IMG = cargar_logo()

class LavanderosWebApp:
    def __init__(self, root):
        self.root = root
        root.title("Lavandería Lavanderos")
        root.geometry("900x700") 
        root.configure(bg=AZUL_CLARO)
        
        # Variables de control para el formulario de servicios
        self.kilos = tk.StringVar(value="5")
        self.tipo_servicio = tk.StringVar(value="Servicio completo (Lavado/Secado)")
        self.direccion_servicio = tk.StringVar()
        self.es_domicilio = tk.BooleanVar(value=True)
        
        # Inicialización de botones de menú como None (necesario para update_user_nav si se llama antes)
        # Aunque ahora la llamada está retrasada, es una buena práctica si se llama en __init__
        self.btn_historial = None
        self.btn_servicios = None

        # --- ESTILOS (Máxima Visibilidad Garantizada) ---
        self.style = ttk.Style()
        self.style.configure("Content.TFrame", background=BLANCO_PURO) 
        self.style.configure("TLabel", background=BLANCO_PURO, foreground=GRIS_TEXTO, font=('Arial', 12))
        
        # Encabezado
        self.style.configure("Header.TFrame", background=AZUL_OSCURO)
        self.style.configure("Header.TLabel", background=AZUL_OSCURO, foreground=BLANCO_PURO, font=('Arial', 20, 'bold'))
        
        # Botones de Navegación del Menú Superior
        self.style.configure("Nav.TButton", background=AZUL_OSCURO, foreground=BLANCO_PURO, font=('Arial', 11, 'bold'), padding=[10, 5], relief="flat")
        self.style.map("Nav.TButton", background=[('active', AZUL_PRINCIPAL)], foreground=[('active', BLANCO_PURO)]) 
        
        # Botones de Acción (Grandes, Azules y Blancos)
        self.style.configure("TButton", background=AZUL_PRINCIPAL, foreground=BLANCO_PURO, font=('Arial', 16, 'bold'), padding=15, relief="raised")
        self.style.map("TButton", background=[('active', AZUL_OSCURO)]) 
        
        # --- ESTRUCTURA ---
        self.crear_encabezado()
        
        self.content_frame = ttk.Frame(root, padding=40, style="Content.TFrame") 
        self.content_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.crear_footer()

        self.show_inicio()
    
    # --- Estructura UI: Encabezado con Menú Superior ---
    def crear_encabezado(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", height=120)
        header_frame.pack(fill="x")
        
        # --- Fila 1: Logo y Título ---
        title_frame = ttk.Frame(header_frame, style="Header.TFrame")
        title_frame.pack(fill="x", pady=(5, 0))
        
        if LOGO_IMG:
            lbl_logo = tk.Label(title_frame, image=LOGO_IMG, bg=AZUL_OSCURO)
            lbl_logo.image = LOGO_IMG
            lbl_logo.pack(side="left", padx=15, pady=5)
        
        self.header_title = ttk.Label(title_frame, text="LAVANDERÍA LAVANDEROS", style="Header.TLabel")
        self.header_title.pack(side="left", padx=20, pady=20)
        
        # Navegación de Usuario (Login/Perfil)
        self.user_nav_frame = ttk.Frame(title_frame, style="Header.TFrame")
        self.user_nav_frame.pack(side="right", padx=15)
        # La llamada a update_user_nav() se mueve al final de esta función.

        # --- Fila 2: Menú de Navegación (Solicitado) ---
        menu_frame = ttk.Frame(header_frame, style="Header.TFrame")
        menu_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Button(menu_frame, text="🏠 Inicio", command=self.show_inicio, style="Nav.TButton").pack(side="left", padx=10)
        
        # CREACIÓN DE BOTONES COMO ATRIBUTOS DE LA CLASE
        self.btn_servicios = ttk.Button(menu_frame, text="🧺 Servicios", command=self.show_register_order, style="Nav.TButton")
        self.btn_servicios.pack(side="left", padx=10)
        
        ttk.Button(menu_frame, text="📞 Contacto", command=self.show_contact_form, style="Nav.TButton").pack(side="left", padx=10)
        
        self.btn_historial = ttk.Button(menu_frame, text="💳 Mi Historial de Pagos", command=self.show_payment_history, style="Nav.TButton")
        self.btn_historial.pack(side="left", padx=10)
        
        # --- LLAMADA CORREGIDA ---
        # Ahora que self.btn_historial existe, podemos llamar a la función que lo configura.
        self.update_user_nav() 

    def crear_footer(self):
        footer = tk.Frame(self.root, bg=AZUL_OSCURO, height=60)
        footer.pack(fill="x", side="bottom")

        tk.Label(footer, text="Lavandería Lavanderos - Cuidado Profesional a Domicilio",
                 fg=BLANCO_PURO, bg=AZUL_OSCURO, font=('Arial', 10, 'bold')).pack(pady=(5, 2))
        
        social_frame = tk.Frame(footer, bg=AZUL_OSCURO)
        social_frame.pack(pady=5)
        
        # Pie de página con redes sociales
        tk.Label(social_frame, text="Síguenos: 📘 Facebook | 📸 Instagram | 📞 +52 123 456 7890",
                 fg=AZUL_CLARO, bg=AZUL_OSCURO, font=('Arial', 9)).pack()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_user_nav(self):
        for widget in self.user_nav_frame.winfo_children(): widget.destroy()
        username = usuario_actual["username"]
        if username:
            ttk.Label(self.user_nav_frame, text=f"Hola, {usuarios[username]['nombre'].split()[0]}",
                      background=AZUL_OSCURO, foreground=BLANCO_PURO, font=('Arial', 11)).pack(pady=5)
            ttk.Button(self.user_nav_frame, text="👤 Perfil", command=self.show_edit_profile, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="❌ Salir", command=self.logout, style="Nav.TButton").pack(side="left", padx=5)
        else:
            ttk.Button(self.user_nav_frame, text="🔑 Login", command=self.show_login, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="➕ Crear Cuenta", command=self.show_register, style="Nav.TButton").pack(side="left", padx=5)
        
        # Actualizar visibilidad del botón de Historial (Ahora que sabemos que self.btn_historial existe)
        if self.btn_historial:
            if username:
                self.btn_historial.config(state=tk.NORMAL)
            else:
                self.btn_historial.config(state=tk.DISABLED)

    # --- Pantalla Principal (Eslogan e Historia) ---
    def show_inicio(self):
        self.clear_content()
        self.header_title.config(text="LAVANDERÍA LAVANDEROS")

        # Eslogan (Prominente)
        ttk.Label(self.content_frame, 
                  text="✨ ¡Tu Ropa, Como Nueva, Sin Esfuerzo! ✨", 
                  font=('Arial', 24, 'bold'), 
                  background=BLANCO_PURO,
                  foreground=AZUL_PRINCIPAL).pack(pady=(25, 15))
        
        # Pequeña Historia/Descripción
        ttk.Label(self.content_frame, 
                  text="Somos Lavandería Lavanderos, dedicados a ofrecer un servicio de cuidado textil profesional, rápido y conveniente. Desde nuestro inicio, nos hemos comprometido a utilizar procesos ecológicos y detergentes de alta calidad para garantizar que tu ropa reciba el mejor trato. Nuestro servicio a domicilio elimina la molestia de la lavandería de tu vida, permitiéndote concentrarte en lo importante.", 
                  font=('Arial', 14), 
                  foreground=GRIS_TEXTO,
                  background=BLANCO_PURO,
                  justify="center",
                  wraplength=750).pack(pady=(0, 40))

        # Botón de llamada a la acción (Máxima visibilidad)
        ttk.Button(self.content_frame, text="🧺 ¡Solicitar Servicio Ahora!", command=self.show_register_order).pack(pady=20)
        
        # Módulo de Login Rápido (para usuarios no logueados)
        if not usuario_actual["username"]:
            login_quick_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
            login_quick_frame.pack(pady=30, padx=50, fill="x")
            ttk.Label(login_quick_frame, text="¿Ya eres cliente? Inicia sesión rápido aquí:", font=('Arial', 12, 'bold'), foreground=AZUL_OSCURO).pack()
            ttk.Button(login_quick_frame, text="🔑 Iniciar Sesión", command=self.show_login, style="Nav.TButton").pack(pady=10)
            ttk.Button(login_quick_frame, text="➕ Crear Cuenta", command=self.show_register, style="Nav.TButton").pack()

    # --- Pantalla de Servicios ---

    def show_register_order(self):
        self.clear_content()
        self.header_title.config(text="CONTRATAR SERVICIOS")
        
        is_logged_in = bool(usuario_actual["username"])

        if is_logged_in:
            user = usuarios[usuario_actual["username"]]
            self.direccion_servicio.set(user["direccion"])
        else:
            self.direccion_servicio.set("Inicia sesión para usar tu dirección registrada")


        form_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=30)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="📝 Detalle de tu Pedido", 
                  font=("Arial", 18, 'bold'), foreground=AZUL_OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # R = Row counter
        r = 1
        # Kilos de Ropa
        ttk.Label(form_frame, text="1. Kilos de Ropa (kg):", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        ttk.Entry(form_frame, textvariable=self.kilos, width=20, font=('Arial', 12)).grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1

        # Tipo de Servicio
        ttk.Label(form_frame, text="2. Tipo de Servicio:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        servicios_opciones = list(COSTOS_SERVICIOS.keys())
        service_combo = ttk.Combobox(form_frame, textvariable=self.tipo_servicio, values=servicios_opciones, state="readonly", width=30, font=('Arial', 12))
        service_combo.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1

        # Opción a Domicilio
        def toggle_direccion():
            state = tk.NORMAL if self.es_domicilio.get() and is_logged_in else tk.DISABLED
            entry_direccion.config(state=state)

        ttk.Label(form_frame, text="3. Modalidad:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        check_domicilio = ttk.Checkbutton(form_frame, text="Servicio a Domicilio (Recolección y Entrega)", variable=self.es_domicilio, command=toggle_direccion, style='TCheckbutton')
        check_domicilio.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1
        
        # Dirección
        ttk.Label(form_frame, text="Dirección de Servicio:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        entry_direccion = ttk.Entry(form_frame, textvariable=self.direccion_servicio, width=35, font=('Arial', 12))
        entry_direccion.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        entry_direccion.config(state=tk.DISABLED if not is_logged_in else tk.NORMAL)
        r += 1
        
        def go_to_payment_or_login():
            if not is_logged_in:
                messagebox.showwarning("Acceso Requerido", "Debes iniciar sesión para **Proceder al Pago** y generar tu pedido.")
                return self.show_login()

            try:
                kilos_val = float(self.kilos.get())
                if kilos_val <= 0:
                    messagebox.showerror("Error", "Por favor, ingresa un peso válido (mayor a 0 kg).")
                    return
            except ValueError:
                 messagebox.showerror("Error", "Formato de kilos inválido.")
                 return

            servicio_val = self.tipo_servicio.get()
            domicilio_val = self.es_domicilio.get()
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

        # Botón de Pago (Máxima Visibilidad)
        ttk.Button(self.content_frame, 
                   text="💰 Proceder al Pago", 
                   command=go_to_payment_or_login,
                   style="TButton").pack(pady=30)
        
        if not is_logged_in:
             ttk.Label(self.content_frame, text="⚠ Inicia sesión para habilitar el botón de pago y tu dirección a domicilio.", 
                       font=('Arial', 12, 'italic'), foreground="#CC0000", background=BLANCO_PURO).pack(pady=10)

    # --- Pantalla de Pago ---

    def calcular_total(self, kilos, servicio, domicilio):
        try: kilos = float(kilos);
        except ValueError: return 0.0
        multiplicador = COSTOS_SERVICIOS.get(servicio, 1.0)
        subtotal = kilos * TARIFA_BASE_KG * multiplicador
        costo_envio = COSTO_DOMICILIO if domicilio else 0.0
        return subtotal + costo_envio

    def show_payment(self, pedido):
        self.clear_content()
        self.header_title.config(text="PROCESO DE PAGO")

        payment_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=30)
        payment_frame.pack(pady=20)
        
        ttk.Label(payment_frame, text="💸 Resumen y Forma de Pago", font=("Arial", 18, 'bold'), foreground=AZUL_OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Fila de Total
        ttk.Label(payment_frame, text="TOTAL A PAGAR:", font=('Arial', 14, 'bold')).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(payment_frame, text=f"${pedido['total']:.2f} MXN", font=('Arial', 18, 'bold'), foreground="#CC0000").grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Fila de Forma de Pago
        ttk.Label(payment_frame, text="Forma de Pago:", font=('Arial', 14, 'bold')).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        metodo_pago = tk.StringVar(value="Tarjeta de Crédito")
        formas = ["Tarjeta de Crédito", "Transferencia Bancaria", "Efectivo (en Recolección)"]
        combo_pago = ttk.Combobox(payment_frame, textvariable=metodo_pago, values=formas, state="readonly", width=25, font=('Arial', 12))
        combo_pago.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Botones de Acción de Pago
        def realizar_pago():
            pedido["estado"] = "Pagado - " + metodo_pago.get()
            usuarios[pedido["cliente"]]["facturas"].append(pedido)
            
            # Limpiar y mostrar botones de finalización
            self.clear_content()
            self.header_title.config(text="TRANSACCIÓN EXITOSA")

            ttk.Label(self.content_frame, text="🎉 ¡Pago Confirmado! 🎉", font=("Arial", 24, 'bold'), foreground="#388E3C").pack(pady=20)
            ttk.Label(self.content_frame, text=f"Tu pedido ID **{pedido['id']}** ha sido agendado. Total pagado: **${pedido['total']:.2f}**").pack(pady=10)
            
            # Contenedor para botones de finalización
            final_btn_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
            final_btn_frame.pack(pady=30)
            
            ttk.Button(final_btn_frame, text="🖨️ Imprimir Comprobante", command=lambda: messagebox.showinfo("Imprimir", f"Imprimiendo comprobante del Pedido ID {pedido['id']}...")).pack(side="left", padx=15)
            ttk.Button(final_btn_frame, text="💳 Ver Historial de Pagos", command=self.show_payment_history).pack(side="left", padx=15)
            ttk.Button(self.content_frame, text="🏠 Finalizar / Volver al Inicio", command=self.show_inicio).pack(pady=20)

        ttk.Button(self.content_frame, text="✅ Botón para Pagar", command=realizar_pago, style="TButton").pack(pady=30)
        ttk.Button(self.content_frame, text="Volver a Servicios", command=self.show_register_order, style="Nav.TButton").pack()

    def show_payment_history(self):
        self.clear_content()
        self.header_title.config(text="HISTORIAL DE PAGOS")
        
        username = usuario_actual["username"]
        if not username: 
            messagebox.showwarning("Acceso Requerido", "Debes iniciar sesión para ver tu historial.")
            return self.show_login()

        historial = usuarios[username]["facturas"]
        
        historial_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        historial_frame.pack(pady=20, fill="x", padx=50)

        ttk.Label(historial_frame, text="📋 Mis Facturas y Pagos", font=("Arial", 16, 'bold'), foreground=AZUL_OSCURO).pack(pady=10)

        if not historial:
            ttk.Label(historial_frame, text="No se han encontrado pagos o facturas en tu historial.", font=('Arial', 12, 'italic')).pack(pady=20)
        else:
            for item in historial:
                info = (f"ID: {item['id']} | Servicio: {item['servicio']} | Kilos: {item['kilos']} kg | "
                        f"Total: **${item['total']:.2f}** | Estado: {item['estado']}")
                ttk.Label(historial_frame, text=info, justify="left", wraplength=700).pack(anchor="w", pady=5)

        ttk.Button(self.content_frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack(pady=20)

    # --- Otras Funciones (Autenticación/Perfil/Contacto) ---
    
    def show_register(self):
        self.clear_content()
        self.header_title.config(text="CREAR CUENTA")
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="Crear Cuenta de Cliente", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        labels_texts = ["Usuario (Para Login):", "Nombre completo:", "Correo:", "Teléfono:", "Dirección:", "Contraseña:"]
        entries = []; 
        for text in labels_texts:
            ttk.Label(frame, text=text).pack(); e = ttk.Entry(frame, width=40);
            if "Contraseña" in text: e.config(show="*");
            e.pack(); entries.append(e)
        def registrar():
            u, n, c, t, d, p = [e.get().strip() for e in entries]
            if u in usuarios: messagebox.showerror("Error", "Ese usuario ya existe."); return
            if not all([u, n, c, t, d, p]): messagebox.showwarning("Advertencia", "Todos los campos son obligatorios."); return
            usuarios[u] = {"nombre": n, "correo": c, "telefono": t, "password": p, "direccion": d, "historial": [], "facturas": []}
            messagebox.showinfo("Registrado", "Cuenta creada con éxito. Ya puedes iniciar sesión."); self.show_login()
        ttk.Button(frame, text="✅ Registrar", command=registrar).pack(pady=15)

    def show_login(self):
        self.clear_content()
        self.header_title.config(text="LOGIN DE CLIENTE")
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="🔑 Iniciar Sesión", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        ttk.Label(frame, text="Usuario:").pack(); user_entry = ttk.Entry(frame, width=30); user_entry.pack()
        ttk.Label(frame, text="Contraseña:").pack(); pass_entry = ttk.Entry(frame, show="*", width=30); pass_entry.pack()
        def validar():
            u = user_entry.get().strip(); p = pass_entry.get().strip()
            if u in usuarios and usuarios[u]["password"] == p:
                usuario_actual["username"] = u
                messagebox.showinfo("Éxito", f"Bienvenido, {usuarios[u]['nombre'].split()[0]}!")
                self.update_user_nav(); self.show_inicio()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos."); pass_entry.delete(0, tk.END)
        ttk.Button(frame, text="Ingresar", command=validar).pack(pady=15)

    def show_edit_profile(self):
        self.clear_content()
        username = usuario_actual["username"]
        if not username: self.show_login(); return
        self.header_title.config(text="EDITAR PERFIL DE CLIENTE"); user = usuarios[username]
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="✏️ Datos de Mi Cuenta", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        fields = ["Nombre completo", "Correo", "Teléfono", "Dirección"]
        entries = {}; keys_map = {"Nombre completo": "nombre", "Correo": "correo", "Teléfono": "telefono", "Dirección": "direccion"}
        for text in fields:
            key = keys_map[text]; ttk.Label(frame, text=f"{text}:").pack(pady=(5, 0)); e = ttk.Entry(frame, width=40); e.insert(0, user[key]); e.pack(); entries[key] = e
        def guardar():
            changes_made = False
            for key, entry in entries.items():
                new_value = entry.get()
                if new_value != user[key]: user[key] = new_value; changes_made = True
            if changes_made: messagebox.showinfo("Guardado", "Perfil actualizado con éxito.")
            else: messagebox.showinfo("Sin Cambios", "No se detectaron modificaciones en el perfil.")
            self.show_inicio()
        ttk.Button(frame, text="✅ Guardar Cambios", command=guardar).pack(pady=15)
        

    def show_contact_form(self):
        self.clear_content()
        self.header_title.config(text="FORMULARIO DE CONTACTO")
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="✉️ Déjanos un Mensaje", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        fields = {"Tu Nombre": tk.StringVar(), "Tu Email": tk.StringVar(), "Asunto": tk.StringVar()}; entries = {}
        for text, var in fields.items():
            ttk.Label(frame, text=f"{text}:").pack(pady=(5, 0)); e = ttk.Entry(frame, textvariable=var, width=40); e.pack(); entries[text] = e
        ttk.Label(frame, text="Mensaje:").pack(pady=(5, 0)); mensaje_text = tk.Text(frame, height=5, width=40); mensaje_text.pack()
        def send_contact():
            data = {k: v.get() for k, v in fields.items()}; data["Mensaje"] = mensaje_text.get("1.0", tk.END).strip()
            if not all(data.values()): messagebox.showerror("Error", "Todos los campos del formulario son obligatorios."); return
            contactos.append(data); messagebox.showinfo("Mensaje Enviado", f"Mensaje enviado por {data['Tu Nombre']}. Pronto nos pondremos en contacto."); self.show_inicio()
        ttk.Button(frame, text="Enviar Mensaje", command=send_contact).pack(pady=15)
        

    def logout(self):
        usuario_actual["username"] = None
        messagebox.showinfo("Sesión cerrada", "Has cerrado la sesión correctamente.")
        self.update_user_nav()
        self.show_inicio()


if __name__ == "__main__":
    root = tk.Tk()
    app = LavanderosWebApp(root)
    root.mainloop()