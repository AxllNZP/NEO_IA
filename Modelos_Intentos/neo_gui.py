# neo_gui.py - Interfaz Gráfica Moderna para NEO
"""
NEO GUI v2.0
Interfaz visual completa usando CustomTkinter
Permite controlar NEO sin usar la terminal

Características:
- Modo VOZ y Modo TEXTO
- Controles visuales
- Log de actividad en tiempo real
- Configuración de TTS
- Diseño moderno y responsivo
"""

import customtkinter as ctk
import threading
import time
from datetime import datetime
import queue
import os

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("dark")  # Modos: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "dark-blue", "green"

print("=" * 60)
print("NEO GUI v2.0 - Interfaz Gráfica")
print("=" * 60)

# ==========================================
# CLASE PRINCIPAL - NEO GUI
# ==========================================

class NEOApp(ctk.CTk):
    """Ventana principal de NEO"""
    
    def __init__(self):
        super().__init__()
        
        # ==========================================
        # CONFIGURACIÓN DE VENTANA
        # ==========================================
        
        self.title("NEO - Asistente Inteligente v2.0")
        self.geometry("800x700")
        self.minsize(700, 600)
        
        # Centrar ventana
        self.center_window()
        
        # ==========================================
        # VARIABLES DE ESTADO
        # ==========================================
        
        self.modo_activo = None  # "voz", "texto", o None
        self.neo_running = False
        self.log_queue = queue.Queue()
        
        # Variables para workers (threads)
        self.voz_thread = None
        self.texto_thread = None
        
        # ==========================================
        # CREAR INTERFAZ
        # ==========================================
        
        self.create_widgets()
        
        # Iniciar actualización del log
        self.update_log()
        
        # Log inicial
        self.add_log("Sistema", "NEO GUI iniciado correctamente", "info")
        
    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    # ==========================================
    # CREAR WIDGETS
    # ==========================================
    
    def create_widgets(self):
        """Crea todos los elementos de la interfaz"""
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # ==========================================
        # HEADER
        # ==========================================
        
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 NEO",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Estado
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="⚫ Inactivo",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # ==========================================
        # PANEL DE MODOS
        # ==========================================
        
        modes_frame = ctk.CTkFrame(self, corner_radius=10)
        modes_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Título del panel
        modes_title = ctk.CTkLabel(
            modes_frame,
            text="Selecciona un Modo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        modes_title.pack(pady=(15, 10))
        
        # Frame interno para botones
        buttons_frame = ctk.CTkFrame(modes_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 15), padx=20, fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Botón MODO VOZ
        self.btn_modo_voz = ctk.CTkButton(
            buttons_frame,
            text="🎤 MODO VOZ",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            command=self.toggle_modo_voz,
            fg_color="#00D26A",
            hover_color="#00A652"
        )
        self.btn_modo_voz.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Botón MODO TEXTO
        self.btn_modo_texto = ctk.CTkButton(
            buttons_frame,
            text="📝 MODO TEXTO",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            command=self.toggle_modo_texto,
            fg_color="#0078D4",
            hover_color="#005A9E"
        )
        self.btn_modo_texto.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        # ==========================================
        # ÁREA DE INPUT (MODO TEXTO)
        # ==========================================
        
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        # Oculto inicialmente, se muestra al activar modo texto
        
        input_title = ctk.CTkLabel(
            self.input_frame,
            text="Escribe tu comando:",
            font=ctk.CTkFont(size=14)
        )
        input_title.pack(pady=(15, 5), padx=20, anchor="w")
        
        # Entry + Botón en un frame horizontal
        input_container = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        input_container.pack(pady=(0, 15), padx=20, fill="x")
        
        self.entry_comando = ctk.CTkEntry(
            input_container,
            placeholder_text="Ejemplo: abre chrome",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_comando.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_comando.bind("<Return>", lambda e: self.enviar_comando_texto())
        
        self.btn_enviar = ctk.CTkButton(
            input_container,
            text="Enviar",
            width=100,
            height=40,
            command=self.enviar_comando_texto
        )
        self.btn_enviar.pack(side="left")
        
        # ==========================================
        # LOG DE ACTIVIDAD
        # ==========================================
        
        log_frame = ctk.CTkFrame(self, corner_radius=10)
        log_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        # Título del log
        log_title = ctk.CTkLabel(
            log_frame,
            text="📋 Actividad",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_title.grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")
        
        # TextBox para log
        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.log_textbox.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        
        # ==========================================
        # PANEL DE CONFIGURACIÓN
        # ==========================================
        
        config_frame = ctk.CTkFrame(self, corner_radius=10)
        config_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        config_title = ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuración de Voz",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        config_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # Grid para controles
        controls_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        controls_frame.pack(pady=(0, 15), padx=20, fill="x")
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Velocidad TTS
        ctk.CTkLabel(
            controls_frame,
            text="Velocidad:",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.slider_velocidad = ctk.CTkSlider(
            controls_frame,
            from_=80,
            to=300,
            number_of_steps=22,
            command=self.update_velocidad_label
        )
        self.slider_velocidad.set(160)
        self.slider_velocidad.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.label_velocidad = ctk.CTkLabel(
            controls_frame,
            text="160 ppm",
            font=ctk.CTkFont(size=12),
            width=80
        )
        self.label_velocidad.grid(row=0, column=2, padx=(10, 0), pady=5)
        
        # Volumen TTS
        ctk.CTkLabel(
            controls_frame,
            text="Volumen:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.slider_volumen = ctk.CTkSlider(
            controls_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=10,
            command=self.update_volumen_label
        )
        self.slider_volumen.set(0.9)
        self.slider_volumen.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.label_volumen = ctk.CTkLabel(
            controls_frame,
            text="90%",
            font=ctk.CTkFont(size=12),
            width=80
        )
        self.label_volumen.grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # ==========================================
        # FOOTER - BOTONES DE ACCIÓN
        # ==========================================
        
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")
        footer_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Botón Limpiar Log
        btn_limpiar = ctk.CTkButton(
            footer_frame,
            text="🗑️ Limpiar Log",
            command=self.limpiar_log,
            height=35
        )
        btn_limpiar.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Botón Detener Todo
        btn_detener = ctk.CTkButton(
            footer_frame,
            text="⏹️ Detener Todo",
            command=self.detener_todo,
            height=35,
            fg_color="#D13438",
            hover_color="#A02327"
        )
        btn_detener.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Botón Salir
        btn_salir = ctk.CTkButton(
            footer_frame,
            text="❌ Salir",
            command=self.salir_app,
            height=35,
            fg_color="#666666",
            hover_color="#4D4D4D"
        )
        btn_salir.grid(row=0, column=2, padx=5, sticky="ew")
    
    # ==========================================
    # MÉTODOS DE CONTROL
    # ==========================================
    
    def toggle_modo_voz(self):
        """Activa/desactiva modo voz"""
        if self.modo_activo == "voz":
            # Desactivar
            self.desactivar_modo_voz()
        else:
            # Activar
            self.activar_modo_voz()
    
    def activar_modo_voz(self):
        """Activa el modo voz"""
        # Desactivar modo texto si está activo
        if self.modo_activo == "texto":
            self.desactivar_modo_texto()
        
        self.modo_activo = "voz"
        self.neo_running = True
        
        # Cambiar apariencia del botón
        self.btn_modo_voz.configure(
            text="⏸️ DETENER VOZ",
            fg_color="#D13438",
            hover_color="#A02327"
        )
        
        # Actualizar estado
        self.status_label.configure(text="🟢 Modo Voz Activo")
        self.add_log("Sistema", "Modo VOZ activado", "success")
        
        # Ocultar input de texto si está visible
        self.input_frame.grid_remove()
        
        # Iniciar thread de voz
        self.voz_thread = threading.Thread(target=self.run_modo_voz, daemon=True)
        self.voz_thread.start()
    
    def desactivar_modo_voz(self):
        """Desactiva el modo voz"""
        self.modo_activo = None
        self.neo_running = False
        
        # Restaurar botón
        self.btn_modo_voz.configure(
            text="🎤 MODO VOZ",
            fg_color="#00D26A",
            hover_color="#00A652"
        )
        
        # Actualizar estado
        self.status_label.configure(text="⚫ Inactivo")
        self.add_log("Sistema", "Modo VOZ desactivado", "info")
    
    def toggle_modo_texto(self):
        """Activa/desactiva modo texto"""
        if self.modo_activo == "texto":
            # Desactivar
            self.desactivar_modo_texto()
        else:
            # Activar
            self.activar_modo_texto()
    
    def activar_modo_texto(self):
        """Activa el modo texto"""
        # Desactivar modo voz si está activo
        if self.modo_activo == "voz":
            self.desactivar_modo_voz()
        
        self.modo_activo = "texto"
        
        # Cambiar apariencia del botón
        self.btn_modo_texto.configure(
            text="⏸️ DETENER TEXTO",
            fg_color="#D13438",
            hover_color="#A02327"
        )
        
        # Actualizar estado
        self.status_label.configure(text="🔵 Modo Texto Activo")
        self.add_log("Sistema", "Modo TEXTO activado", "success")
        
        # Mostrar input de texto
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew", after=self.children['!ctkframe2'])
        
        # Focus en entrada
        self.entry_comando.focus()
    
    def desactivar_modo_texto(self):
        """Desactiva el modo texto"""
        self.modo_activo = None
        
        # Restaurar botón
        self.btn_modo_texto.configure(
            text="📝 MODO TEXTO",
            fg_color="#0078D4",
            hover_color="#005A9E"
        )
        
        # Actualizar estado
        self.status_label.configure(text="⚫ Inactivo")
        self.add_log("Sistema", "Modo TEXTO desactivado", "info")
        
        # Ocultar input
        self.input_frame.grid_remove()
    
    def enviar_comando_texto(self):
        """Procesa comando del modo texto"""
        comando = self.entry_comando.get().strip()
        
        if not comando:
            return
        
        # Limpiar entrada
        self.entry_comando.delete(0, "end")
        
        # Log del comando
        self.add_log("Usuario", comando, "command")
        
        # Procesar comando en thread separado
        thread = threading.Thread(
            target=self.procesar_comando,
            args=(comando,),
            daemon=True
        )
        thread.start()
    
    def detener_todo(self):
        """Detiene todos los modos activos"""
        if self.modo_activo == "voz":
            self.desactivar_modo_voz()
        elif self.modo_activo == "texto":
            self.desactivar_modo_texto()
        
        self.add_log("Sistema", "Todos los modos detenidos", "warning")
    
    def limpiar_log(self):
        """Limpia el log de actividad"""
        self.log_textbox.delete("1.0", "end")
        self.add_log("Sistema", "Log limpiado", "info")
    
    def salir_app(self):
        """Cierra la aplicación"""
        self.add_log("Sistema", "Cerrando NEO...", "info")
        time.sleep(0.5)
        self.neo_running = False
        self.destroy()
    
    # ==========================================
    # WORKERS (Threads)
    # ==========================================
    
    def run_modo_voz(self):
        """Thread que ejecuta el modo voz"""
        self.add_log("Sistema", "Iniciando reconocimiento de voz...", "info")
        
        # Intentar importar módulos de voz
        try:
            # Aquí iría la integración con tu sistema de voz
            # Por ahora es un placeholder
            
            while self.neo_running and self.modo_activo == "voz":
                self.add_log("Sistema", "Esperando comando de voz...", "info")
                time.sleep(3)
                
                # Simulación (reemplazar con tu código real)
                if self.neo_running:
                    self.add_log("Sistema", "Escuchando...", "info")
                    time.sleep(2)
        
        except ImportError as e:
            self.add_log("Error", f"Módulos de voz no disponibles: {e}", "error")
            self.after(100, self.desactivar_modo_voz)
    
    def procesar_comando(self, comando):
        """Procesa un comando (voz o texto)"""
        self.add_log("NEO", f"Procesando: {comando}", "processing")
        
        try:
            # Aquí iría la integración con tu neo_cerebro.py
            # Por ahora es un placeholder
            
            time.sleep(1)  # Simular procesamiento
            
            # Respuesta simulada
            respuesta = f"Ejecutando: {comando}"
            self.add_log("NEO", respuesta, "success")
            
            # Simular TTS
            velocidad = int(self.slider_velocidad.get())
            volumen = int(self.slider_volumen.get() * 100)
            self.add_log("TTS", f"Hablando (vel: {velocidad}, vol: {volumen}%)", "info")
            
        except Exception as e:
            self.add_log("Error", str(e), "error")
    
    # ==========================================
    # UTILIDADES
    # ==========================================
    
    def add_log(self, fuente, mensaje, tipo="info"):
        """Agrega mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Elegir emoji según tipo
        emoji_map = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "command": "💬",
            "processing": "⚙️"
        }
        emoji = emoji_map.get(tipo, "•")
        
        # Formatear mensaje
        log_entry = f"[{timestamp}] {emoji} {fuente}: {mensaje}\n"
        
        # Agregar a cola
        self.log_queue.put(log_entry)
    
    def update_log(self):
        """Actualiza el log desde la cola (thread-safe)"""
        try:
            while True:
                log_entry = self.log_queue.get_nowait()
                self.log_textbox.insert("end", log_entry)
                self.log_textbox.see("end")
        except queue.Empty:
            pass
        
        # Repetir cada 100ms
        self.after(100, self.update_log)
    
    def update_velocidad_label(self, value):
        """Actualiza label de velocidad"""
        self.label_velocidad.configure(text=f"{int(value)} ppm")
    
    def update_volumen_label(self, value):
        """Actualiza label de volumen"""
        self.label_volumen.configure(text=f"{int(value * 100)}%")

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n✓ Iniciando NEO GUI...")
    
    try:
        app = NEOApp()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n⚠️ Aplicación interrumpida")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✓ NEO GUI cerrado")