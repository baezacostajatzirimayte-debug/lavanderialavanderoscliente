import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

class LavanderosWebApp:
    def __init__(self, root):
        self.root = root
        root.title("Lavandería Lavanderos - Sistema de Gestión")
        root.geometry("1000x800")
        
        # --- VARIABLES DE ESTADO ---
        self.user_logged_in = False
        self.user_role = "" # Ahora 'Cliente'
        self.nav_visible = True # Estado inicial del menú de hamburguesa
        
        # --- COLORES DE LAVANDERÍA ---
        self.COLOR_FONDO_PRINCIPAL = "#E1F5FE"      # Azul muy claro (Fondo principal)
        self.COLOR_AZUL_BOTON = "#1E88E5"          # Azul fuerte (Botones de acción)
        self.COLOR_HEADER = "#091A6F"              # Azul oscuro (Header/Footer)
        self.COLOR_NAV_BUTTON = "#5B92E5"          # Azul intermedio para botones de nav
        self.root.configure(bg=self.COLOR_FONDO_PRINCIPAL)

        # --- ESTILOS (ttk) ---
        self.style = ttk.Style()
        
        self.style.configure("Content.TFrame", background=self.COLOR_FONDO_PRINCIPAL) 
        self.style.configure("TLabel", background=self.COLOR_FONDO_PRINCIPAL, foreground="black", font=('Arial', 12))
        
        self.style.configure("Header.TFrame", background=self.COLOR_HEADER)
        self.style.configure("Nav.TFrame", background=self.COLOR_HEADER)
        self.style.configure("Header.TLabel", background=self.COLOR_HEADER, foreground="white", font=('Arial', 28, 'bold'))
        
        self.style.configure("Nav.TButton", 
                             background=self.COLOR_NAV_BUTTON, 
                             foreground="#003366", # Texto en Azul Marino
                             font=('Arial', 12, 'bold'),
                             padding=[20, 10, 20, 10], 
                             relief="flat")
        self.style.map("Nav.TButton", 
                       background=[('active', '#3A77C8')]) 
        
        self.style.configure("TButton", 
                             background=self.COLOR_AZUL_BOTON, 
                             foreground="white", 
                             font=('Arial', 12, 'bold'),
                             padding=10)
        self.style.map("TButton", 
                       background=[('active', '#1565C0')]) 

        # --- 1. CONTENEDOR PRINCIPAL DEL HEADER (GRID) ---
        self.header_frame = ttk.Frame(root, style="Header.TFrame")
        self.header_frame.pack(fill="x", pady=0)
        
        self.header_frame.grid_columnconfigure(0, weight=0) # Logo/Menu
        self.header_frame.grid_columnconfigure(1, weight=3) # Título
        self.header_frame.grid_columnconfigure(2, weight=1) # Búsqueda/Social
        
        # 1.1 Botón de Hamburguesa
        self.menu_button = ttk.Button(self.header_frame, text="☰ Menú", command=self.toggle_nav, style="Nav.TButton")
        self.menu_button.grid(row=0, column=0, padx=(10, 0), pady=15, sticky="nsw")
        
        # 1.2 Título principal
        ttk.Label(self.header_frame, text="LAVANDERÍA LAVANDEROS", 
                  style="Header.TLabel").grid(row=0, column=1, padx=20, pady=15, sticky="w")
        
        # 1.3 Buscador (Simulación de barra ovalada)
        search_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        search_frame.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        ttk.Label(search_frame, text="🔍", background=self.COLOR_NAV_BUTTON, foreground="white", 
                  font=('Arial', 14)).pack(side="left", padx=(10, 5), ipady=5)
        ttk.Entry(search_frame, width=15).pack(side="left", ipady=5)
        
        # 1.4 Íconos Sociales (Ahora incluye el botón de Login/Perfil)
        self.social_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.social_frame.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        
        self.login_status_label = ttk.Label(self.social_frame, text="", background=self.COLOR_HEADER, foreground="white", font=('Arial', 10, 'bold'))
        self.login_status_label.pack(side="top", pady=(0, 5))
        
        # Simulación de Íconos
        ttk.Label(self.social_frame, text="✆", background="white", foreground="black", font=('Arial', 14), width=2).pack(side="left", padx=5)
        ttk.Label(self.social_frame, text="📷", background="white", foreground="black", font=('Arial', 14), width=2).pack(side="left", padx=5)
        ttk.Label(self.social_frame, text="f", background="white", foreground="black", font=('Arial', 14), width=2).pack(side="left", padx=5)
        
        # --- 2. BARRA DE NAVEGACIÓN HORIZONTAL (Botones principales) ---
        self.nav_frame = ttk.Frame(root, style="Nav.TFrame", height=60)
        self.nav_frame.pack(fill="x")
        
        self.nav_frame.grid_columnconfigure(0, weight=1) 
        self.nav_frame.grid_columnconfigure(1, weight=0) 
        self.nav_frame.grid_columnconfigure(2, weight=1) 

        self.nav_buttons_frame = ttk.Frame(self.nav_frame, style="Nav.TFrame")
        self.nav_buttons_frame.grid(row=0, column=1, pady=5)
        
        # Creación de botones de navegación
        self.create_nav_button(self.nav_buttons_frame, "Inicio", self.show_inicio, side="left")
        self.create_nav_button(self.nav_buttons_frame, "Formulario de contacto", self.show_contacto, side="left") 
        self.create_nav_button(self.nav_buttons_frame, "Recolección a Domicilio", self.show_recoleccion, side="left")
        self.create_nav_button(self.nav_buttons_frame, "Nuestros Servicios", self.show_servicios, side="left")
        
        # --- Botones de Login/Perfil/Logout (Se actualizarán) ---
        self.update_nav_buttons()


        # --- 3. IMAGEN / LOGO (POSICIÓN AJUSTADA: Columna 0, fila 1) ---
        try:
            # ********** CAMBIO REALIZADO AQUÍ **********
            img = Image.open("Lavanderia.png") 
            img = img.resize((100, 100))
            self.imgTk = ImageTk.PhotoImage(img)
            
            # Se ha reubicado el logo en la columna 0, debajo del botón de menú
            self.logo_label = tk.Label(self.header_frame, image=self.imgTk, bg=self.COLOR_HEADER)
            self.logo_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsw")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el archivo 'Lavanderia.png'. Error: {e}")
            self.logo_label = tk.Label(self.header_frame, text="🧺 LOGO", font=('Arial', 18, 'bold'), bg=self.COLOR_HEADER, fg="white")
            self.logo_label.grid(row=1, column=0, padx=20, pady=5, sticky="nsw")


        # --- 4. CONTENIDO PRINCIPAL ---
        self.content_frame = ttk.Frame(root, padding=40, style="Content.TFrame") 
        self.content_frame.pack(expand=True, fill="both")

        # Variables de Recolección/Contacto
        self.nombre = tk.StringVar()
        self.telefono = tk.StringVar()
        self.direccion = tk.StringVar()
        self.email_contacto = tk.StringVar()
        self.asunto_contacto = tk.StringVar()
        self.mensaje_contacto = tk.StringVar()
        
        # Variables de Login
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        # Iniciar en la pantalla de Login
        self.show_login()


        # --- 5. FOOTER (AVANZADO) ---
        self.footer_frame = ttk.Frame(root, style="Header.TFrame")
        self.footer_frame.pack(side="bottom", fill="x", pady=0)
        
        self.footer_frame.grid_columnconfigure(0, weight=1) 
        self.footer_frame.grid_columnconfigure(1, weight=1) 
        
        # Columna 0: Logo y Copyright
        footer_info_frame = ttk.Frame(self.footer_frame, style="Header.TFrame")
        footer_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        ttk.Label(footer_info_frame, text="🧺", background=self.COLOR_HEADER, foreground="white", font=('Arial', 20, 'bold')).pack(side="left", padx=(0, 10))
        
        ttk.Label(footer_info_frame, text="Visitas: Inicio | Aviso de Privacidad\nCopyright © 2024 Lavandería Lavanderos.\nTodos los derechos reservados.", 
                  font=('Arial', 10), background=self.COLOR_HEADER, foreground="white", justify="left").pack(side="left")
        
        # Columna 1: Políticas y Términos
        ttk.Label(self.footer_frame, text="• Políticas de Privacidad\n• Términos y Condiciones", 
                  font=('Arial', 11, 'bold'), background=self.COLOR_HEADER, foreground="white", justify="right").grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
    # --- Funciones de Utilidad ---
    
    def create_nav_button(self, parent, text, command, side="left"):
        """Crea y empaqueta un botón de navegación horizontal."""
        btn = ttk.Button(parent, text=text, command=command, style="Nav.TButton")
        btn.pack(side=side, padx=10, pady=10) 

    def toggle_nav(self):
        """Alterna la visibilidad de la barra de navegación (menú de hamburguesa)."""
        if self.nav_visible:
            self.nav_frame.pack_forget()
            self.menu_button.config(text="☰ Menú (Oculto)")
        else:
            self.nav_frame.pack(before=self.content_frame, fill="x") # Reinsertar antes del contenido
            self.menu_button.config(text="☰ Menú")
        self.nav_visible = not self.nav_visible

    def clear_content(self):
        """Limpia todos los widgets del frame de contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_content_label(self, text, font=('Arial', 14)):
        """Crea y actualiza una etiqueta de contenido principal (para textos simples)."""
        self.clear_content()
        center_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        center_frame.pack(expand=True)

        new_label = ttk.Label(center_frame, text=text, font=font, background=self.COLOR_FONDO_PRINCIPAL, wraplength=700, justify="center")
        new_label.pack(pady=50, padx=20) 
        
    def update_nav_buttons(self):
        """Actualiza los botones de Login/Perfil/Logout."""
        for widget in self.social_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.destroy()
        
        self.login_status_label.pack_forget()
        self.login_status_label.pack(side="top", pady=(0, 5))
        
        for widget in self.social_frame.winfo_children():
            if not isinstance(widget, ttk.Label) or widget == self.login_status_label: continue
            widget.pack_forget()
            widget.pack(side="left", padx=5)

        if self.user_logged_in:
            self.login_status_label.config(text=f"Bienvenido, {self.user_role}")
            
            btn_perfil = ttk.Button(self.social_frame, text="👤 Mi Cuenta", command=self.show_perfil, style="Nav.TButton")
            btn_perfil.pack(side="left", padx=5)
            
            btn_logout = ttk.Button(self.social_frame, text="❌ Salir", command=self.logout, style="Nav.TButton")
            btn_logout.pack(side="left", padx=5)
        else:
            self.login_status_label.config(text="HABLA CON NOSOTROS")
            
            btn_login = ttk.Button(self.social_frame, text="🔑 Login", command=self.show_login, style="Nav.TButton")
            btn_login.pack(side="left", padx=5)

    # --- Funciones de Autenticación ---

    def show_login(self):
        """Muestra el formulario de inicio de sesión."""
        self.clear_content()
        
        title_label = ttk.Label(self.content_frame, 
                                 text="🔑 Iniciar Sesión (Cliente)", 
                                 font=('Arial', 18, 'bold'),
                                 background=self.COLOR_FONDO_PRINCIPAL)
        title_label.pack(pady=(50, 30))

        login_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        login_frame.pack(pady=20)

        # Usuario
        ttk.Label(login_frame, text="Usuario (Cliente):", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=0, column=0, sticky="e", padx=5, pady=10
        )
        ttk.Entry(login_frame, textvariable=self.username, width=30).grid(
            row=0, column=1, sticky="w", padx=5, pady=10
        )

        # Contraseña
        ttk.Label(login_frame, text="Contraseña:", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=1, column=0, sticky="e", padx=5, pady=10
        )
        ttk.Entry(login_frame, textvariable=self.password, show="*", width=30).grid(
            row=1, column=1, sticky="w", padx=5, pady=10
        )
        
        # Botón
        ttk.Button(login_frame, text="Ingresar", command=self.attempt_login).grid(
            row=2, column=0, columnspan=2, pady=20
        )

    def attempt_login(self):
        """Simulación de la lógica de inicio de sesión."""
        user = self.username.get()
        pwd = self.password.get()
        
        # Credenciales simuladas de Cliente
        if user == "cliente" and pwd == "1234":
            self.user_logged_in = True
            self.user_role = "Cliente" 
            self.update_nav_buttons()
            self.show_perfil() 
            messagebox.showinfo("Éxito", "Bienvenido, Cliente.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.password.set("")

    def logout(self):
        """Cierra la sesión del usuario."""
        self.user_logged_in = False
        self.user_role = ""
        self.username.set("")
        self.password.set("")
        self.update_nav_buttons()
        self.show_login()
        messagebox.showinfo("Cerrar Sesión", "Has cerrado la sesión correctamente.")

    # --- Funciones de Gestión ---

    def show_perfil(self):
        """Muestra la pantalla de Gestión de Perfil (Solo Cliente)."""
        self.clear_content()
        if not self.user_logged_in or self.user_role != "Cliente":
            self.update_content_label("Acceso Denegado. Por favor, inicie sesión como Cliente.", font=('Arial', 16, 'bold'))
            return
            
        title_label = ttk.Label(self.content_frame, 
                                 text="👤 Mi Cuenta de Cliente", 
                                 font=('Arial', 18, 'bold'),
                                 background=self.COLOR_FONDO_PRINCIPAL)
        title_label.pack(pady=(20, 30))

        perfil_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        perfil_frame.pack(pady=20)

        # Simulación de datos del perfil de Cliente
        perfil_data = {
            "Nombre": "Cliente Frecuente (Simulado)",
            "Email": "cliente.frecuente@mail.com",
            "Teléfono": "55 1234 5678",
            "Dirección Principal": "Calle Ficción #123, Col. Limpio",
            "Último Pedido": "2024-11-25 (Recolección Exitosa)"
        }
        
        r = 0
        for key, value in perfil_data.items():
            ttk.Label(perfil_frame, text=f"{key}:", font=('Arial', 12, 'bold'), background=self.COLOR_FONDO_PRINCIPAL).grid(
                row=r, column=0, sticky="w", padx=10, pady=5
            )
            ttk.Label(perfil_frame, text=value, background=self.COLOR_FONDO_PRINCIPAL).grid(
                row=r, column=1, sticky="w", padx=10, pady=5
            )
            r += 1
        
        # Botones de Acción para el Cliente
        action_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        action_frame.pack(pady=30)
        
        ttk.Button(action_frame, text="📆 Agendar Nueva Recolección", command=self.show_recoleccion).pack(side="left", padx=10)
        ttk.Button(action_frame, text="💳 Ver Historial de Pagos", command=lambda: messagebox.showinfo("Historial", "Funcionalidad no implementada: Muestra los pagos del cliente.")).pack(side="left", padx=10)

    # --- Funciones de Recolección (Mantenida por su utilidad) ---
    def agendar_recoleccion(self):
        """Simula el envío del formulario de recolección."""
        if not self.nombre.get() or not self.telefono.get() or not self.direccion.get():
            messagebox.showerror("Error", "Nombre, Teléfono y Dirección son campos obligatorios.")
            return

        messagebox.showinfo("Recolección Agendada", f"¡Recolección agendada para {self.nombre.get()} en {self.direccion.get()}! Nos pondremos en contacto al {self.telefono.get()}.")
        # Limpiar campos después de enviar
        self.nombre.set("")
        self.telefono.set("")
        self.direccion.set("")
        self.show_inicio()

    def show_recoleccion(self):
        """Muestra el formulario de solicitud de recolección."""
        self.clear_content()
        
        title_label = ttk.Label(self.content_frame, 
                                 text="📝 Solicite su Recolección a Domicilio", 
                                 font=('Arial', 18, 'bold'),
                                 background=self.COLOR_FONDO_PRINCIPAL)
        title_label.pack(pady=(20, 30))

        # --- Formulario de Recolección con Grid Centrado ---
        form_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Nombre Completo:", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=1, column=0, sticky="e", padx=(10, 5), pady=10
        )
        ttk.Entry(form_frame, textvariable=self.nombre, width=35).grid(
            row=1, column=1, sticky="w", padx=(5, 10), pady=10
        )
        ttk.Label(form_frame, text="Teléfono de Contacto:", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=2, column=0, sticky="e", padx=(10, 5), pady=10
        )
        ttk.Entry(form_frame, textvariable=self.telefono, width=35).grid(
            row=2, column=1, sticky="w", padx=(5, 10), pady=10
        )
        ttk.Label(form_frame, text="Dirección de Recolección:", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=3, column=0, sticky="e", padx=(10, 5), pady=10
        )
        ttk.Entry(form_frame, textvariable=self.direccion, width=35).grid(
            row=3, column=1, sticky="w", padx=(5, 10), pady=10
        )
        ttk.Label(form_frame, text="Peso Estimado (kg):", background=self.COLOR_FONDO_PRINCIPAL).grid(
            row=4, column=0, sticky="e", padx=(10, 5), pady=10
        )
        ttk.Entry(form_frame, width=35).grid(
            row=4, column=1, sticky="w", padx=(5, 10), pady=10
        )
        
        ttk.Button(form_frame, text="Agendar Recolección", command=self.agendar_recoleccion).grid(
            row=5, column=0, columnspan=2, pady=30
        )

    # --- Funciones de Contenido General ---

    def show_contacto(self):
        """Muestra el formulario de contacto completo."""
        self.clear_content()
        
        title_label = ttk.Label(self.content_frame, 
                                 text="✉️ Formulario de Contacto", 
                                 font=('Arial', 18, 'bold'),
                                 background=self.COLOR_FONDO_PRINCIPAL)
        title_label.pack(pady=(20, 30))

        contact_frame = ttk.Frame(self.content_frame, style="Content.TFrame", padding=20)
        contact_frame.pack(pady=20)

        # 1. Nombre
        ttk.Label(contact_frame, text="Tu Nombre:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=0, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(contact_frame, textvariable=self.nombre, width=40).grid(row=0, column=1, sticky="w", padx=5, pady=10)

        # 2. Email
        ttk.Label(contact_frame, text="Tu Email:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(contact_frame, textvariable=self.email_contacto, width=40).grid(row=1, column=1, sticky="w", padx=5, pady=10)

        # 3. Asunto
        ttk.Label(contact_frame, text="Asunto:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        ttk.Entry(contact_frame, textvariable=self.asunto_contacto, width=40).grid(row=2, column=1, sticky="w", padx=5, pady=10)

        # 4. Mensaje
        ttk.Label(contact_frame, text="Mensaje:", background=self.COLOR_FONDO_PRINCIPAL).grid(row=3, column=0, sticky="ne", padx=5, pady=10)
        mensaje_text = tk.Text(contact_frame, height=8, width=40)
        mensaje_text.grid(row=3, column=1, sticky="w", padx=5, pady=10)
        
        # Botón de Enviar
        ttk.Button(contact_frame, text="Enviar Mensaje", command=lambda: self.send_contact(mensaje_text.get("1.0", tk.END))).grid(
            row=4, column=0, columnspan=2, pady=20
        )
        
    def send_contact(self, mensaje):
        """Simula el envío del formulario de contacto."""
        if not self.nombre.get() or not self.email_contacto.get() or not self.asunto_contacto.get() or not mensaje.strip():
            messagebox.showerror("Error", "Todos los campos del formulario de contacto son obligatorios.")
            return

        messagebox.showinfo("Mensaje Enviado", f"Mensaje enviado con éxito por {self.nombre.get()}. Nos pondremos en contacto a {self.email_contacto.get()}.")
        # Limpiar campos después de enviar
        self.nombre.set("")
        self.email_contacto.set("")
        self.asunto_contacto.set("")
        self.show_inicio()

    def show_inicio(self):
        """Muestra la Historia de Éxito, Misión y Visión en un solo bloque de texto."""
        
        texto_completo_inicio = (
            "Somos Lavandería Lavanderos \n\n"
            "Hemos logrado el éxito porque nuestra prioridad es tu tiempo y la calidad "
            "en el cuidado de tu ropa. Nos especializamos en ofrecer un servicio integral a "
            "domicilio: tú agendas la recolección y la entrega a través de nuestra "
            "plataforma, y nosotros nos encargamos del resto.\n\n"
            
            "Nuestra Misión es ofrecer el mejor servicio de lavandería a domicilio, "
            "garantizando el cuidado de tu ropa con los más altos estándares de calidad.\n\n"
            
            "Nuestra Visión es ser la lavandería líder en el mercado, reconocida por "
            "la puntualidad en la recolección y entrega, y nuestro compromiso ecológico."
        )
        
        self.clear_content()
        center_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        center_frame.pack(expand=True, fill="both")
        
        # Título principal
        ttk.Label(center_frame, 
                  text="🧼 ¡Somos expertos en el cuidado de tu ropa! 🧺", 
                  font=('Arial', 18, 'bold'), 
                  background=self.COLOR_FONDO_PRINCIPAL).pack(pady=(20, 20))
        
        # Mostrar el texto completo unificado
        ttk.Label(center_frame, 
                  text=texto_completo_inicio, 
                  font=('Arial', 14), 
                  foreground="black", 
                  background=self.COLOR_FONDO_PRINCIPAL, 
                  wraplength=800, 
                  justify="center").pack(pady=30, padx=50)

    def show_plan_mensual(self):
        self.update_content_label("💎 **Nuestros Planes Mensuales**\n\nPlan Básico: 15kg/mes por $400.\nPlan Premium: 30kg/mes, incluye tintorería, por $850.\n\n¡Ahorra tiempo y dinero!", font=('Arial', 16))

    def show_sucursal(self):
        self.update_content_label("📍 **Sucursal Más Cercana**\n\nNuestra sucursal principal está en:\nAvenida Siempre Viva #123, Colonia Limpio.\n\nPróximamente abriremos más sucursales para ti.", font=('Arial', 16))

    def show_servicios(self):
        servicios_text = "✨ **Lista de Servicios**\n\n- Lavado y Secado por kilo.\n- Tintorería (trajes, vestidos).\n- Planchado exprés.\n- Lavado de edredones y blancos.\n- Servicio a domicilio (Recolección y Entrega)."
        self.update_content_label(servicios_text, font=('Arial', 16))


if __name__ == "__main__":
    root = tk.Tk()
    app = LavanderosWebApp(root)
    root.mainloop()