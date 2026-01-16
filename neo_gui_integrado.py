# neo_gui_integrado.py - GUI Integrada con Sistema NEO Completo
"""
NEO GUI v0.2 - Totalmente Integrado
Conecta la interfaz gráfica con todo el sistema NEO:
- Reconocimiento de voz (Whisper)
- Cerebro IA (Llama)
- Control PC (PyAutoGUI)
- TTS (pyttsx3)
- Memoria

INSTRUCCIONES:
1. Asegúrate de tener todos los módulos NEO en la misma carpeta
2. Ejecuta: python neo_gui_integrado.py
"""

import customtkinter as ctk
import threading
import time
from datetime import datetime
import queue
import os
import sys

# Importar módulos de NEO
try:
    from neo_voz_tts import inicializar_tts, neo_habla
    TTS_DISPONIBLE = True
except ImportError:
    print("⚠️ neo_voz_tts.py no encontrado - TTS desactivado")
    TTS_DISPONIBLE = False

try:
    import neo_cerebro
    CEREBRO_DISPONIBLE = True
except ImportError:
    print("⚠️ neo_cerebro.py no encontrado - Modo simplificado")
    CEREBRO_DISPONIBLE = False

try:
    import neo_memoria
    MEMORIA_DISPONIBLE = True
except ImportError:
    print("⚠️ neo_memoria.py no encontrado - Sin memoria")
    MEMORIA_DISPONIBLE = False

# Para modo voz
try:
    import whisper
    import pyaudio
    import wave
    import numpy as np
    VOZ_DISPONIBLE = True
except ImportError:
    print("⚠️ Módulos de voz no disponibles - Solo modo texto")
    VOZ_DISPONIBLE = False

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

print("=" * 60)
print("NEO GUI v0.2 - COMPLETO E INTEGRADO")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN DE VOZ (si está disponible)
# ==========================================

if VOZ_DISPONIBLE:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    SILENCE_THRESHOLD = 400
    SILENCE_DURATION = 2.5
    TEMP_AUDIO = "temp_neo_gui_audio.wav"
    
    PALABRAS_ACTIVACION = ['neo', 'neó', 'nio']
    
    # Cargar Whisper
    print("\n[*] Cargando Whisper...")
    try:
        modelo_whisper = whisper.load_model("base")
        print("✓ Whisper cargado")
    except:
        VOZ_DISPONIBLE = False
        print("❌ Error al cargar Whisper")

# Inicializar TTS
if TTS_DISPONIBLE:
    print("[*] Inicializando TTS...")
    try:
        tts_engine = inicializar_tts(rate=160, volume=0.9, debug=False)
        print("✓ TTS listo")
    except:
        TTS_DISPONIBLE = False
        print("⚠️ TTS no disponible")

# ==========================================
# CLASE PRINCIPAL - NEO GUI INTEGRADO
# ==========================================

class NEOAppIntegrado(ctk.CTk):
    """Aplicación NEO con integración completa"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("NEO")
        self.geometry("850x750")
        self.minsize(750, 650)
        
        self.center_window()
        
        # Variables de estado
        self.modo_activo = None
        self.neo_running = False
        self.log_queue = queue.Queue()
        
        # Threads
        self.voz_thread = None
        
        # Crear interfaz
        self.create_widgets()
        
        # Actualizar log
        self.update_log()
        
        # Mensaje inicial
        self.add_log("Sistema", "NEO GUI Integrado iniciado", "success")
        
        # Reportar módulos disponibles
        self.reportar_modulos()
        
        # Saludo inicial
        if TTS_DISPONIBLE:
            self.after(1000, lambda: neo_habla("Hola, soy Neo. Interfaz gráfica lista"))
    
    def center_window(self):
        """Centrar ventana"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def reportar_modulos(self):
        """Reporta qué módulos están disponibles"""
        modulos = {
            "Reconocimiento de Voz": VOZ_DISPONIBLE,
            "Sistema TTS": TTS_DISPONIBLE,
            "Cerebro IA": CEREBRO_DISPONIBLE,
            "Memoria": MEMORIA_DISPONIBLE
        }
        
        for nombre, disponible in modulos.items():
            estado = "✅ Activo" if disponible else "❌ Desactivado"
            self.add_log("Módulo", f"{nombre}: {estado}", "info")
    
    # ==========================================
    # CREAR INTERFAZ (igual que antes)
    # ==========================================
    
    def create_widgets(self):
        """Crea la interfaz"""
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # HEADER
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Implementacion NEO V0.2",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        self.status_label = ctk.CTkLabel(
            header_frame,
            text=" Inactivo",
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # PANEL DE MODOS
        modes_frame = ctk.CTkFrame(self, corner_radius=10)
        modes_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        modes_title = ctk.CTkLabel(
            modes_frame,
            text="Selecciona un Modo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        modes_title.pack(pady=(15, 10))
        
        buttons_frame = ctk.CTkFrame(modes_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 15), padx=20, fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Botón VOZ
        voz_text = "🎤 MODO VOZ" if VOZ_DISPONIBLE else "🎤 VOZ (No disponible)"
        self.btn_modo_voz = ctk.CTkButton(
            buttons_frame,
            text=voz_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=60,
            command=self.toggle_modo_voz,
            fg_color="#00D26A" if VOZ_DISPONIBLE else "#666666",
            hover_color="#00A652" if VOZ_DISPONIBLE else "#555555",
            state="normal" if VOZ_DISPONIBLE else "disabled"
        )
        self.btn_modo_voz.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        # Botón TEXTO
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
        
        # INPUT DE TEXTO (oculto inicialmente)
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        
        input_title = ctk.CTkLabel(
            self.input_frame,
            text="Escribe tu comando:",
            font=ctk.CTkFont(size=14)
        )
        input_title.pack(pady=(15, 5), padx=20, anchor="w")
        
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
        
        # LOG
        log_frame = ctk.CTkFrame(self, corner_radius=10)
        log_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        log_title = ctk.CTkLabel(
            log_frame,
            text="📋 Actividad en Tiempo Real",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_title.grid(row=0, column=0, pady=(15, 5), padx=20, sticky="w")
        
        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.log_textbox.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")
        
        # CONFIGURACIÓN TTS
        if TTS_DISPONIBLE:
            config_frame = ctk.CTkFrame(self, corner_radius=10)
            config_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            
            config_title = ctk.CTkLabel(
                config_frame,
                text="⚙️ Configuración de Voz (TTS)",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            config_title.pack(pady=(15, 10), padx=20, anchor="w")
            
            controls_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
            controls_frame.pack(pady=(0, 15), padx=20, fill="x")
            controls_frame.grid_columnconfigure(1, weight=1)
            
            # Velocidad
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
            
            # Volumen
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
        
        # FOOTER
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")
        footer_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        btn_limpiar = ctk.CTkButton(
            footer_frame,
            text="🗑️ Limpiar Log",
            command=self.limpiar_log,
            height=35
        )
        btn_limpiar.grid(row=0, column=0, padx=5, sticky="ew")
        
        btn_detener = ctk.CTkButton(
            footer_frame,
            text="⏹️ Detener Todo",
            command=self.detener_todo,
            height=35,
            fg_color="#D13438",
            hover_color="#A02327"
        )
        btn_detener.grid(row=0, column=1, padx=5, sticky="ew")
        
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
    # CONTROL DE MODOS
    # ==========================================
    
    def toggle_modo_voz(self):
        """Toggle modo voz"""
        if not VOZ_DISPONIBLE:
            return
        
        if self.modo_activo == "voz":
            self.desactivar_modo_voz()
        else:
            self.activar_modo_voz()
    
    def activar_modo_voz(self):
        """Activa modo voz"""
        if self.modo_activo == "texto":
            self.desactivar_modo_texto()
        
        self.modo_activo = "voz"
        self.neo_running = True
        
        self.btn_modo_voz.configure(
            text="⏸️ DETENER VOZ",
            fg_color="#D13438",
            hover_color="#A02327"
        )
        
        self.status_label.configure(text="🟢 Modo Voz Activo")
        self.add_log("Sistema", "Modo VOZ activado", "success")
        
        if TTS_DISPONIBLE:
            neo_habla("Modo voz activado", wait=False)
        
        self.input_frame.grid_remove()
        
        # Iniciar thread
        self.voz_thread = threading.Thread(target=self.run_modo_voz, daemon=True)
        self.voz_thread.start()
    
    def desactivar_modo_voz(self):
        """Desactiva modo voz"""
        self.modo_activo = None
        self.neo_running = False
        
        self.btn_modo_voz.configure(
            text="🎤 MODO VOZ",
            fg_color="#00D26A",
            hover_color="#00A652"
        )
        
        self.status_label.configure(text="⚫ Inactivo")
        self.add_log("Sistema", "Modo VOZ desactivado", "info")
    
    def toggle_modo_texto(self):
        """Toggle modo texto"""
        if self.modo_activo == "texto":
            self.desactivar_modo_texto()
        else:
            self.activar_modo_texto()
    
    def activar_modo_texto(self):
        """Activa modo texto"""
        if self.modo_activo == "voz":
            self.desactivar_modo_voz()
        
        self.modo_activo = "texto"
        
        self.btn_modo_texto.configure(
            text="⏸️ DETENER TEXTO",
            fg_color="#D13438",
            hover_color="#A02327"
        )
        
        self.status_label.configure(text="🔵 Modo Texto Activo")
        self.add_log("Sistema", "Modo TEXTO activado", "success")
        
        if TTS_DISPONIBLE:
            neo_habla("Modo texto activado", wait=False)
        
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry_comando.focus()
    
    def desactivar_modo_texto(self):
        """Desactiva modo texto"""
        self.modo_activo = None
        
        self.btn_modo_texto.configure(
            text="📝 MODO TEXTO",
            fg_color="#0078D4",
            hover_color="#005A9E"
        )
        
        self.status_label.configure(text="⚫ Inactivo")
        self.add_log("Sistema", "Modo TEXTO desactivado", "info")
        
        self.input_frame.grid_remove()
    
    def enviar_comando_texto(self):
        """Envía comando desde modo texto"""
        comando = self.entry_comando.get().strip()
        
        if not comando:
            return
        
        self.entry_comando.delete(0, "end")
        self.add_log("Usuario", comando, "command")
        
        thread = threading.Thread(
            target=self.procesar_comando,
            args=(comando,),
            daemon=True
        )
        thread.start()
    
    # ==========================================
    # WORKERS - INTEGRACIÓN REAL
    # ==========================================
    
    def run_modo_voz(self):
        """Thread de modo voz - INTEGRACIÓN REAL"""
        self.add_log("Sistema", "Iniciando reconocimiento de voz", "info")
        
        while self.neo_running and self.modo_activo == "voz":
            try:
                # Escuchar audio
                self.add_log("Sistema", "🎤 Escuchando...", "info")
                archivo = self.escuchar_audio()
                
                if not archivo:
                    continue
                
                # Transcribir
                texto = self.transcribir_audio(archivo)
                
                if not texto:
                    continue
                
                self.add_log("Whisper", f"'{texto}'", "info")
                
                # Detectar activación
                activado, comando = self.detectar_activacion(texto)
                
                if activado and comando:
                    self.add_log("Usuario", comando, "command")
                    self.procesar_comando(comando)
                
                # Limpiar
                if os.path.exists(archivo):
                    os.remove(archivo)
                    
            except Exception as e:
                self.add_log("Error", str(e), "error")
                time.sleep(1)
    
    def escuchar_audio(self):
        """Escucha audio del micrófono"""
        audio = pyaudio.PyAudio()
        
        try:
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            frames = []
            silent_chunks = 0
            max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)
            recording = False
            
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.abs(audio_data).mean()
                
                if volume > SILENCE_THRESHOLD:
                    if not recording:
                        recording = True
                    silent_chunks = 0
                    frames.append(data)
                else:
                    if recording:
                        silent_chunks += 1
                        frames.append(data)
                        
                        if silent_chunks > max_silent_chunks:
                            break
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            if len(frames) == 0:
                return None
            
            # Guardar
            wf = wave.open(TEMP_AUDIO, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return TEMP_AUDIO
            
        except Exception as e:
            audio.terminate()
            return None
    
    def transcribir_audio(self, archivo):
        """Transcribe audio con Whisper"""
        try:
            result = modelo_whisper.transcribe(archivo, language="es")
            return result['text'].strip()
        except:
            return None
    
    def detectar_activacion(self, texto):
        """Detecta palabra de activación"""
        texto_lower = texto.lower()
        
        for palabra in PALABRAS_ACTIVACION:
            if palabra in texto_lower:
                comando = texto_lower.replace(palabra, '').strip()
                return True, comando
        
        return False, texto
    
    def procesar_comando(self, comando):
        """Procesa comando - INTEGRACIÓN REAL"""
        self.add_log("NEO", "Procesando...", "processing")
        
        try:
            # Usar cerebro real si está disponible
            if CEREBRO_DISPONIBLE:
                plan = neo_cerebro.procesar_comando(comando)
                
                if plan:
                    explicacion = plan.get('explicacion', 'Ejecutando')
                    self.add_log("NEO", explicacion, "success")
                    
                    # TTS
                    if TTS_DISPONIBLE:
                        velocidad = int(self.slider_velocidad.get())
                        volumen = self.slider_volumen.get()

                        tts_engine.rate = velocidad
                        tts_engine.volume = volumen

                        neo_habla(explicacion, wait=False)

                    
                    # Ejecutar
                    exito = neo_cerebro.ejecutar_plan(plan)
                    
                    if exito:
                        self.add_log("Sistema", "✓ Comando completado", "success")
                        if TTS_DISPONIBLE:
                            neo_habla("Listo", wait=False)
                        
                        # Guardar en memoria
                        if MEMORIA_DISPONIBLE:
                            neo_memoria.guardar_comando(comando, plan, exito)
                    else:
                        self.add_log("Error", "Fallo en ejecución", "error")
                else:
                    self.add_log("Error", "No se generó plan", "error")
            else:
                # Modo simplificado sin cerebro
                self.add_log("NEO", f"Ejecutaría: {comando}", "info")
                if TTS_DISPONIBLE:
                    neo_habla(f"Ejecutando {comando}", wait=False)
                
        except Exception as e:
            self.add_log("Error", str(e), "error")
    
    # ==========================================
    # UTILIDADES
    # ==========================================
    
    def detener_todo(self):
        """Detiene todo"""
        if self.modo_activo == "voz":
            self.desactivar_modo_voz()
        elif self.modo_activo == "texto":
            self.desactivar_modo_texto()
        
        self.add_log("Sistema", "Todo detenido", "warning")
    
    def limpiar_log(self):
        """Limpia log"""
        self.log_textbox.delete("1.0", "end")
        self.add_log("Sistema", "Log limpiado", "info")
    
    def salir_app(self):
        """Cierra app"""
        self.add_log("Sistema", "Cerrando NEO...", "info")
        
        if TTS_DISPONIBLE:
            neo_habla("Hasta luego", wait=True)
        
        time.sleep(0.5)
        self.neo_running = False
        self.destroy()
    
    def add_log(self, fuente, mensaje, tipo="info"):
        """Agrega al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        emoji_map = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "command": "💬",
            "processing": "⚙️"
        }
        emoji = emoji_map.get(tipo, "•")
        
        log_entry = f"[{timestamp}] {emoji} {fuente}: {mensaje}\n"
        self.log_queue.put(log_entry)
    
    def update_log(self):
        """Actualiza log"""
        try:
            while True:
                log_entry = self.log_queue.get_nowait()
                self.log_textbox.insert("end", log_entry)
                self.log_textbox.see("end")
        except queue.Empty:
            pass
        
        self.after(100, self.update_log)
    
    def update_velocidad_label(self, value):
        """Actualiza label velocidad"""
        self.label_velocidad.configure(text=f"{int(value)} ppm")
    
    def update_volumen_label(self, value):
        """Actualiza label volumen"""
        self.label_volumen.configure(text=f"{int(value * 100)}%")

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    print("\n✓ Iniciando NEO GUI Integrado...")
    
    try:
        app = NEOAppIntegrado()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n⚠️ Aplicación interrumpida")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✓ NEO GUI cerrado")