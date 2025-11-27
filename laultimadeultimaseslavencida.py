import tkinter as tk
from tkinter import ttk, messagebox
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ------------------------------
# PALETA DE COLORES (Azules combinables - Visibilidad Mejorada)
# ------------------------------
AZUL_OSCURO = "#091A6F"        # Encabezado
AZUL_MEDIO = "#1E88E5"         # Botones de Acción (BG)
AZUL_CLARO = "#5B92E5"         # Botones de Navegación (BG)
FONDO_PRINCIPAL = "#E1F5FE"    # Fondo de contenido (Cian claro)
# ESTA ES LA ÚNICA LÍNEA QUE NECESITAS CAMBIAR
TEXTO_BOTON = "black"          # Texto en botones (AHORA NEGRO)
TEXTO_OSCURO = "#003366"       # Texto de títulos y labels
TEXTO_NORMAL = "black"

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
        "facturas": [] # Arreglo para historial de pagos
    }
}
pedidos = []
contactos = []
usuario_actual = {"username": None}

# ------------------------------
# PRECIOS SIMULADOS (Para la lógica de pago)
# ------------------------------
TARIFA_BASE_KG = 25.0
COSTO_DOMICILIO = 45.0
COSTOS_SERVICIOS = {
    "Servicio completo (Lavado/Secado)": 1.0, # Multiplicador de 1.0
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
        root.geometry("850x650") # Tamaño ajustado
        root.configure(bg=FONDO_PRINCIPAL)
        
        # Variables para el formulario de servicios
        self.kilos = tk.StringVar(value="5")
        self.tipo_servicio = tk.StringVar(value="Servicio completo (Lavado/Secado)")
        self.direccion_servicio = tk.StringVar()
        self.es_domicilio = tk.BooleanVar(value=True)

        # --- ESTILOS (Mejora de visibilidad) ---
        self.style = ttk.Style()
        self.style.configure("Content.TFrame", background=FONDO_PRINCIPAL) 
        self.style.configure("TLabel", background=FONDO_PRINCIPAL, foreground=TEXTO_NORMAL, font=('Arial', 12))
        self.style.configure("Header.TFrame", background=AZUL_OSCURO)
        self.style.configure("Header.TLabel", background=AZUL_OSCURO, foreground="white", font=('Arial', 20, 'bold'))
        
        # Botones de Navegación (Ahora con texto negro)
        self.style.configure("Nav.TButton", background=AZUL_CLARO, foreground=TEXTO_BOTON, font=('Arial', 12, 'bold'), padding=[15, 8], relief="flat")
        # Para el hover del botón de navegación, mantenemos el texto blanco sobre fondo oscuro (AZUL_OSCURO) para buen contraste
        self.style.map("Nav.TButton", background=[('active', AZUL_OSCURO)], foreground=[('active', 'white')]) 
        
        # Botones de Acción (Ahora con texto negro)
        self.style.configure("TButton", background=AZUL_MEDIO, foreground=TEXTO_BOTON, font=('Arial', 13, 'bold'), padding=10)
        # Para el hover del botón de acción, mantenemos el texto negro (TEXTO_BOTON) sobre AZUL_OSCURO. 
        # ATENCIÓN: Por ser negro sobre azul oscuro, el contraste es BAJO. Si quieres buen contraste, cambia el 'foreground' del 'active' a 'white'.
        self.style.map("TButton", background=[('active', AZUL_OSCURO)], foreground=[('active', 'white')]) 
        
        # --- ESTRUCTURA ---
        self.crear_encabezado()
        self.content_frame = ttk.Frame(root, padding=30, style="Content.TFrame") 
        self.content_frame.pack(expand=True, fill="both")
        self.crear_footer()

        self.show_inicio()

    def crear_encabezado(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame", height=90)
        header_frame.pack(fill="x")
        
        if LOGO_IMG:
            lbl_logo = tk.Label(header_frame, image=LOGO_IMG, bg=AZUL_OSCURO)
            lbl_logo.image = LOGO_IMG
            lbl_logo.pack(side="left", padx=15, pady=5)
        else:
            ttk.Label(header_frame, text="🧺 Lavanderos", style="Header.TLabel").pack(side="left", padx=15, pady=20)
        
        self.header_title = ttk.Label(header_frame, text="Sistema de Cliente", style="Header.TLabel")
        self.header_title.pack(side="left", padx=20, pady=20)
        
        self.user_nav_frame = ttk.Frame(header_frame, style="Header.TFrame")
        self.user_nav_frame.pack(side="right", padx=15)
        self.update_user_nav()

    def crear_footer(self):
        footer = tk.Frame(self.root, bg=AZUL_OSCURO, height=60)
        footer.pack(fill="x", side="bottom")

        tk.Label(footer, text="Lavandería Lavanderos - Contacto y Servicios",
                 fg="white", bg=AZUL_OSCURO, font=('Arial', 10, 'bold')).pack(pady=(5, 2))
        
        # Contenedor para Redes Sociales
        social_frame = tk.Frame(footer, bg=AZUL_OSCURO)
        social_frame.pack(pady=5)
        
        # Simulación de botones/enlaces a redes sociales
        tk.Label(social_frame, text="Síguenos: 📘 Facebook | 📸 Instagram | 📞 +52 123 456 7890",
                 fg=FONDO_PRINCIPAL, bg=AZUL_OSCURO, font=('Arial', 9)).pack()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_user_nav(self):
        for widget in self.user_nav_frame.winfo_children(): widget.destroy()
        username = usuario_actual["username"]
        if username:
            ttk.Label(self.user_nav_frame, text=f"Hola, {usuarios[username]['nombre'].split()[0]}",
                      background=AZUL_OSCURO, foreground="white", font=('Arial', 11)).pack(pady=5)
            ttk.Button(self.user_nav_frame, text="👤 Perfil", command=self.show_edit_profile, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="❌ Salir", command=self.logout, style="Nav.TButton").pack(side="left", padx=5)
        else:
            ttk.Button(self.user_nav_frame, text="🔑 Login", command=self.show_login, style="Nav.TButton").pack(side="left", padx=5)
            ttk.Button(self.user_nav_frame, text="➕ Crear Cuenta", command=self.show_register, style="Nav.TButton").pack(side="left", padx=5)

    def show_inicio(self):
        self.clear_content()
        self.header_title.config(text="LAVANDERÍA LAVANDEROS (Inicio)")

        # Eslogan principal (más grande)
        ttk.Label(self.content_frame, 
                  text="🧼 ¡Lavandería Lavanderos! 🧺", 
                  font=('Arial', 20, 'bold'), 
                  background=FONDO_PRINCIPAL,
                  foreground=AZUL_OSCURO).pack(pady=(20, 10))
        
        ttk.Label(self.content_frame, 
                  text="La mejor lavandería a domicilio: Recolección, lavado de calidad y entrega puntual.", 
                  font=('Arial', 14, 'italic'), 
                  foreground=TEXTO_OSCURO,
                  background=FONDO_PRINCIPAL,
                  justify="center").pack()

        # Botones de navegación (USANDO ttk.Button)
        menu_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        menu_frame.pack(pady=40)
        
        def create_menu_button(parent, text, command):
            # Usamos ttk.Button y el estilo Nav.TButton
            btn = ttk.Button(parent, text=text, command=command, style="Nav.TButton", width=22)
            btn.pack(side="left", padx=20)
        
        if usuario_actual["username"]:
            create_menu_button(menu_frame, "🧺 Contratar Servicios", self.show_register_order)
            create_menu_button(menu_frame, "💳 Ver Historial de Pagos", self.show_payment_history)
        else:
            create_menu_button(menu_frame, "➕ Crear Cuenta", self.show_register)
            create_menu_button(menu_frame, "🔑 Login", self.show_login)
            
        # Botón de Contacto siempre visible
        ttk.Button(self.content_frame, text="✉️ Formulario de Contacto", command=self.show_contact_form, style="Nav.TButton").pack(pady=20)

    # --- Lógica de Servicios y Pago ---
    
    def calcular_total(self, kilos, servicio, domicilio):
        try:
            kilos = float(kilos)
            if kilos <= 0: return 0.0
        except ValueError:
            return 0.0

        multiplicador = COSTOS_SERVICIOS.get(servicio, 1.0)
        
        subtotal = kilos * TARIFA_BASE_KG * multiplicador
        costo_envio = COSTO_DOMICILIO if domicilio else 0.0
        
        total = subtotal + costo_envio
        return total

    def show_register_order(self):
        self.clear_content()
        if not usuario_actual["username"]: 
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para contratar servicios.")
            return self.show_login()
            
        self.header_title.config(text="Contratar Servicios")
        user = usuarios[usuario_actual["username"]]
        self.direccion_servicio.set(user["direccion"])

        form_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=25)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Selección de Servicio de Lavandería", 
                  font=("Arial", 16, 'bold'), foreground=AZUL_OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        r = 1
        # Kilos de Ropa
        ttk.Label(form_frame, text="1. Kilos de Ropa (kg):", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        ttk.Entry(form_frame, textvariable=self.kilos, width=20, font=('Arial', 12)).grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1

        # Tipo de Servicio
        ttk.Label(form_frame, text="2. Tipo de Servicio:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        servicios_opciones = ["Servicio completo (Lavado/Secado)", "Tintorería", "Industrial", "Ecológica (Ahorro de Agua)"]

        service_combo = ttk.Combobox(form_frame, textvariable=self.tipo_servicio, values=servicios_opciones, state="readonly", width=30, font=('Arial', 12))
        service_combo.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1

        # Opción a Domicilio
        def toggle_direccion():
            if self.es_domicilio.get():
                entry_direccion.config(state=tk.NORMAL)
            else:
                entry_direccion.config(state=tk.DISABLED)

        ttk.Label(form_frame, text="3. Modalidad:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        check_domicilio = ttk.Checkbutton(form_frame, text="Servicio a Domicilio (Recolección y Entrega)", variable=self.es_domicilio, 
                                          command=toggle_direccion, style='TCheckbutton')
        check_domicilio.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1
        
        # Dirección
        ttk.Label(form_frame, text="Dirección de Servicio:", font=('Arial', 12, 'bold')).grid(row=r, column=0, sticky="w", padx=10, pady=10)
        entry_direccion = ttk.Entry(form_frame, textvariable=self.direccion_servicio, width=35, font=('Arial', 12))
        entry_direccion.grid(row=r, column=1, sticky="w", padx=10, pady=10)
        r += 1
        
        toggle_direccion()

        def go_to_payment():
            kilos_val = self.kilos.get()
            servicio_val = self.tipo_servicio.get()
            domicilio_val = self.es_domicilio.get()
            direccion_val = self.direccion_servicio.get()
            
            total = self.calcular_total(kilos_val, servicio_val, domicilio_val)

            if total <= 0:
                messagebox.showerror("Error", "Por favor, ingresa un peso válido (mayor a 0 kg).")
                return

            current_pedido = {
                "id": len(pedidos) + 1,
                "cliente": usuario_actual["username"],
                "kilos": kilos_val,
                "servicio": servicio_val,
                "domicilio": domicilio_val,
                "direccion": direccion_val if domicilio_val else "Presencial",
                "total": total,
                "estado": "Pendiente de Pago"
            }
            pedidos.append(current_pedido)
            self.show_payment(current_pedido)


        ttk.Button(self.content_frame, text="💰 Proceder al Pago", command=go_to_payment).pack(pady=30)
        ttk.Button(self.content_frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack(pady=10)


    def show_payment(self, pedido):
        self.clear_content()
        self.header_title.config(text="Proceso de Pago")

        payment_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=30)
        payment_frame.pack(pady=20)
        
        ttk.Label(payment_frame, text="💸 Resumen de Pago", font=("Arial", 18, 'bold'), foreground=AZUL_OSCURO).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Información del total
        ttk.Label(payment_frame, text="Total a Pagar:", font=('Arial', 14, 'bold')).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(payment_frame, text=f"${pedido['total']:.2f} MXN", font=('Arial', 16, 'bold'), foreground="#C62828").grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Forma de Pago
        ttk.Label(payment_frame, text="Forma de Pago:", font=('Arial', 14, 'bold')).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        metodo_pago = tk.StringVar(value="Tarjeta de Crédito")
        formas = ["Tarjeta de Crédito", "Transferencia Bancaria", "Efectivo (en Recolección)"]
        combo_pago = ttk.Combobox(payment_frame, textvariable=metodo_pago, values=formas, state="readonly", width=25, font=('Arial', 12))
        combo_pago.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        def realizar_pago():
            # SIMULACIÓN DE PAGO
            pedido["estado"] = "Pagado - " + metodo_pago.get()
            usuarios[pedido["cliente"]]["facturas"].append(pedido)
            
            messagebox.showinfo("Pago Exitoso", f"Pago de ${pedido['total']:.2f} realizado con éxito.\nTu pedido ID {pedido['id']} ha sido confirmado.")
            
            for widget in payment_frame.winfo_children(): widget.destroy()
            
            ttk.Label(payment_frame, text="🎉 ¡Operación Exitosa! 🎉", font=("Arial", 20, 'bold'), foreground="#388E3C").pack(pady=20)
            ttk.Label(payment_frame, text=f"Pedido ID: {pedido['id']} | Total: ${pedido['total']:.2f}").pack()
            
            # Estos botones usan el estilo "TButton" y "Nav.TButton" con texto negro
            ttk.Button(self.content_frame, text="🖨️ Imprimir Comprobante", command=lambda: messagebox.showinfo("Imprimir", f"Imprimiendo comprobante del Pedido ID {pedido['id']}...")).pack(pady=10)
            ttk.Button(self.content_frame, text="💳 Ver Historial de Pagos", command=self.show_payment_history).pack(pady=10)
            ttk.Button(self.content_frame, text="Finalizar / Volver al Inicio", command=self.show_inicio).pack(pady=20)
            
            btn_pago.destroy()


        btn_pago = ttk.Button(self.content_frame, text="✅ Pagar Ahora", command=realizar_pago)
        btn_pago.pack(pady=30)
        ttk.Button(self.content_frame, text="Volver a Servicios", command=self.show_register_order, style="Nav.TButton").pack()

    def show_payment_history(self):
        self.clear_content()
        self.header_title.config(text="Historial de Pagos")
        
        username = usuario_actual["username"]
        if not username: return self.show_login()

        historial = usuarios[username]["facturas"]
        
        historial_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        historial_frame.pack(pady=20, fill="x", padx=50)

        ttk.Label(historial_frame, text="💳 Historial de Facturas/Pagos", font=("Arial", 16, 'bold'), foreground=AZUL_OSCURO).pack(pady=10)

        if not historial:
            ttk.Label(historial_frame, text="No se han encontrado pagos o facturas en tu historial.", font=('Arial', 12, 'italic')).pack(pady=20)
        else:
            for item in historial:
                info = (f"ID: {item['id']} | Servicio: {item['servicio']} | Kilos: {item['kilos']} kg | "
                        f"Total: ${item['total']:.2f} | Estado: {item['estado']}")
                ttk.Label(historial_frame, text=info, justify="left", wraplength=700).pack(anchor="w", pady=5)

        ttk.Button(self.content_frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack(pady=20)

    def show_register(self):
        self.clear_content()
        self.header_title.config(text="Crear Cuenta")
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
            if u in usuarios:
                messagebox.showerror("Error", "Ese usuario ya existe."); return
            if not all([u, n, c, t, d, p]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios."); return
            usuarios[u] = {"nombre": n, "correo": c, "telefono": t, "password": p, "direccion": d, "historial": [], "facturas": []}
            messagebox.showinfo("Registrado", "Cuenta creada con éxito. Ya puedes iniciar sesión."); self.show_login()
        ttk.Button(frame, text="✅ Registrar", command=registrar).pack(pady=15)
        ttk.Button(frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack()

    def show_login(self):
        self.clear_content()
        self.header_title.config(text="Login de Cliente")
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="🔑 Iniciar Sesión", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        ttk.Label(frame, text="Usuario:").pack(); user_entry = ttk.Entry(frame, width=30); user_entry.pack()
        ttk.Label(frame, text="Contraseña:").pack(); pass_entry = ttk.Entry(frame, show="*", width=30); pass_entry.pack()
        def validar():
            u = user_entry.get().strip(); p = pass_entry.get().strip()
            if u in usuarios and usuarios[u]["password"] == p:
                usuario_actual["username"] = u
                messagebox.showinfo("Éxito", f"Bienvenido, {usuarios[u]['nombre'].split()[0]}!")
                self.update_user_nav(); self.show_edit_profile()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos."); pass_entry.delete(0, tk.END)
        ttk.Button(frame, text="Ingresar", command=validar).pack(pady=15)
        ttk.Button(frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack()

    def show_contact_form(self):
        self.clear_content()
        self.header_title.config(text="Formulario de Contacto")
        frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20); frame.pack(pady=20)
        ttk.Label(frame, text="✉️ Déjanos un Mensaje", font=("Arial", 16, "bold"), foreground=AZUL_OSCURO).pack(pady=8)
        fields = {"Tu Nombre": tk.StringVar(), "Tu Email": tk.StringVar(), "Asunto": tk.StringVar()}; entries = {}
        for text, var in fields.items():
            ttk.Label(frame, text=f"{text}:").pack(pady=(5, 0)); e = ttk.Entry(frame, textvariable=var, width=40); e.pack(); entries[text] = e
        ttk.Label(frame, text="Mensaje:").pack(pady=(5, 0)); mensaje_text = tk.Text(frame, height=5, width=40); mensaje_text.pack()
        def send_contact():
            data = {k: v.get() for k, v in fields.items()}; data["Mensaje"] = mensaje_text.get("1.0", tk.END).strip()
            if not all(data.values()):
                messagebox.showerror("Error", "Todos los campos del formulario son obligatorios."); return
            contactos.append(data); messagebox.showinfo("Mensaje Enviado", f"Mensaje enviado por {data['Tu Nombre']}. Pronto nos pondremos en contacto."); self.show_inicio()
        ttk.Button(frame, text="Enviar Mensaje", command=send_contact).pack(pady=15)
        ttk.Button(frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack()

    def show_edit_profile(self):
        self.clear_content()
        username = usuario_actual["username"]
        if not username: self.show_login(); return
        self.header_title.config(text="Editar Perfil de Cliente"); user = usuarios[username]
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
        ttk.Button(frame, text="Volver al Inicio", command=self.show_inicio, style="Nav.TButton").pack(pady=5)


    def logout(self):
        usuario_actual["username"] = None
        messagebox.showinfo("Sesión cerrada", "Has cerrado la sesión correctamente.")
        self.update_user_nav()
        self.show_inicio()


if __name__ == "__main__":
    root = tk.Tk()
    app = LavanderosWebApp(root)
    root.mainloop()