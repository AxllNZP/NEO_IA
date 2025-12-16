# neo_voz_tts.py - Sistema TTS (Text-to-Speech) para NEO
"""
Sistema de síntesis de voz para NEO usando pyttsx3.
Permite que NEO "hable" de vuelta al usuario con voz en español.

Características:
- Voz en español (busca automáticamente)
- Velocidad ajustable
- Volumen configurable
- Sistema de cola para múltiples mensajes
- Modo debug para pruebas
"""

import sys
import pyttsx3
import time
import threading
from datetime import datetime

print("=" * 60)
print("NEO - Sistema TTS v1.0")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================

# Configuración por defecto
DEFAULT_RATE = 160        # Palabras por minuto (160 es natural para español)
DEFAULT_VOLUME = 0.9      # Volumen (0.0 - 1.0)
DEFAULT_VOICE_GENDER = None  # 'male', 'female', o None para automático

# Motor TTS global (se inicializa una sola vez)
_engine = None
_engine_initialized = False
_engine_lock = threading.Lock()

# ==========================================
# CLASE: NEOVoice
# ==========================================

class NEOVoice:
    """
    Clase principal para el sistema TTS de NEO.
    Maneja la inicialización, configuración y síntesis de voz.
    """
    
    def __init__(self, rate=DEFAULT_RATE, volume=DEFAULT_VOLUME, debug=False):
        """
        Inicializa el motor TTS.
        
        Args:
            rate (int): Velocidad de habla (80-300 palabras/minuto)
            volume (float): Volumen (0.0 a 1.0)
            debug (bool): Modo debug para ver información detallada
        """
        self.debug = debug
        self.rate = rate
        self.volume = volume
        self.current_voice = None
        self.available_voices = []
        
        # Inicializar motor
        self._init_engine()
        
        # Obtener voces disponibles
        self._load_voices()
        
        # Configurar voz en español (si está disponible)
        self._setup_spanish_voice()
        
        # Aplicar configuración
        self._apply_settings()
        
        if self.debug:
            self._print_config()
    
    def _init_engine(self):
        """Inicializa el motor pyttsx3"""
        try:
            if self.debug:
                print("\n[DEBUG] Inicializando motor TTS...")
            
            self.engine = pyttsx3.init('sapi5' if sys.platform == 'win32' else None)
            
            if self.debug:
                print("[DEBUG] ✓ Motor inicializado correctamente")
                
        except Exception as e:
            print(f"❌ Error al inicializar TTS: {e}")
            self.engine = None
    
    def _is_windows(self):
        """Detecta si estamos en Windows"""
        import platform
        return platform.system() == 'Windows'
    
    def _load_voices(self):
        """Carga todas las voces disponibles en el sistema"""
        if not self.engine:
            return
        
        try:
            self.available_voices = self.engine.getProperty('voices')
            
            if self.debug:
                print(f"\n[DEBUG] {len(self.available_voices)} voces encontradas:")
                for i, voice in enumerate(self.available_voices):
                    print(f"  [{i}] {voice.name}")
                    print(f"      ID: {voice.id}")
                    print(f"      Idiomas: {voice.languages}")
                    print(f"      Género: {voice.gender}")
                    print()
                    
        except Exception as e:
            print(f"⚠️  Error al cargar voces: {e}")
            self.available_voices = []
    
    def _setup_spanish_voice(self):
        """
        Busca y configura una voz en español.
        Orden de prioridad:
        1. Voces con 'es' en languages
        2. Voces con 'spanish' en el nombre
        3. Primera voz disponible (fallback)
        """
        if not self.available_voices:
            print("⚠️  No hay voces disponibles")
            return
        
        # Buscar voz en español
        spanish_voice = None
        
        # Método 1: Buscar por código de idioma
        for voice in self.available_voices:
            if voice.languages:
                for lang in voice.languages:
                    lang_str = str(lang).lower()
                    if 'es' in lang_str or 'spanish' in lang_str:
                        spanish_voice = voice
                        break
            if spanish_voice:
                break
        
        # Método 2: Buscar por nombre
        if not spanish_voice:
            for voice in self.available_voices:
                name = voice.name.lower()
                if 'spanish' in name or 'helena' in name or 'sabina' in name:
                    spanish_voice = voice
                    break
        
        # Método 3: Usar primera voz (fallback)
        if not spanish_voice:
            spanish_voice = self.available_voices[0]
            if self.debug:
                print("⚠️  No se encontró voz en español, usando voz por defecto")
        
        # Configurar voz
        if spanish_voice:
            self.current_voice = spanish_voice
            self.engine.setProperty('voice', spanish_voice.id)
            
            if self.debug:
                print(f"\n[DEBUG] Voz seleccionada: {spanish_voice.name}")
    
    def _apply_settings(self):
        """Aplica la configuración de velocidad y volumen"""
        if not self.engine:
            return
        
        try:
            # Velocidad
            self.engine.setProperty('rate', self.rate)
            
            # Volumen
            self.engine.setProperty('volume', self.volume)
            
            if self.debug:
                print(f"\n[DEBUG] Configuración aplicada:")
                print(f"  - Velocidad: {self.rate} palabras/minuto")
                print(f"  - Volumen: {self.volume * 100}%")
                
        except Exception as e:
            print(f"⚠️  Error al aplicar configuración: {e}")
    
    def _print_config(self):
        """Imprime la configuración actual (modo debug)"""
        print("\n" + "=" * 60)
        print("CONFIGURACIÓN TTS")
        print("=" * 60)
        print(f"\nVoz actual: {self.current_voice.name if self.current_voice else 'N/A'}")
        print(f"Velocidad: {self.rate} palabras/minuto")
        print(f"Volumen: {self.volume * 100}%")
        print(f"Voces disponibles: {len(self.available_voices)}")
        print("=" * 60)
    
    # ==========================================
    # MÉTODOS PÚBLICOS
    # ==========================================
    
    def speak(self, text, wait=True):
        """
        Habla el texto proporcionado.
        
        Args:
            text (str): Texto a sintetizar
            wait (bool): Si True, espera a que termine de hablar
        
        Returns:
            bool: True si se habló correctamente, False si hubo error
        """
        if not self.engine:
            print("❌ Motor TTS no inicializado")
            return False
        
        if not text or text.strip() == "":
            return False
        
        try:
            # Limpiar texto (quitar emojis y caracteres especiales)
            text_clean = self._clean_text(text)
            
            if self.debug:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] 🔊 NEO: {text_clean}")
            
            # Hablar
            self.engine.say(text_clean)
            
            if wait:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Error al hablar: {e}")
            return False
    
    def speak_async(self, text):
        """
        Habla de forma asíncrona (no bloquea la ejecución).
        
        Args:
            text (str): Texto a sintetizar
        """
        thread = threading.Thread(target=self.speak, args=(text, True))
        thread.daemon = True
        thread.start()
    
    def _clean_text(self, text):
        """
        Limpia el texto de caracteres que pueden causar problemas.
        
        Args:
            text (str): Texto original
            
        Returns:
            str: Texto limpio
        """
        # Quitar emojis y caracteres especiales comunes
        replacements = {
            '✓': '',
            '✅': '',
            '❌': '',
            '⚠️': '',
            '🎯': '',
            '💬': '',
            '🔊': '',
            '🎤': '',
            '📝': '',
            '👁️': '',
            '🧠': '',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text.strip()
    
    def set_rate(self, rate):
        """
        Cambia la velocidad de habla.
        
        Args:
            rate (int): Nueva velocidad (80-300 palabras/minuto)
        """
        if 80 <= rate <= 300:
            self.rate = rate
            if self.engine:
                self.engine.setProperty('rate', rate)
                if self.debug:
                    print(f"[DEBUG] Velocidad cambiada a {rate} palabras/min")
        else:
            print("⚠️  Velocidad debe estar entre 80 y 300")
    
    def set_volume(self, volume):
        """
        Cambia el volumen.
        
        Args:
            volume (float): Nuevo volumen (0.0 a 1.0)
        """
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            if self.engine:
                self.engine.setProperty('volume', volume)
                if self.debug:
                    print(f"[DEBUG] Volumen cambiado a {volume * 100}%")
        else:
            print("⚠️  Volumen debe estar entre 0.0 y 1.0")
    
    def list_voices(self):
        """Lista todas las voces disponibles con detalles"""
        print("\n" + "=" * 60)
        print("VOCES DISPONIBLES EN EL SISTEMA")
        print("=" * 60)
        
        if not self.available_voices:
            print("No hay voces disponibles")
            return
        
        for i, voice in enumerate(self.available_voices):
            print(f"\n[{i}] {voice.name}")
            print(f"    ID: {voice.id}")
            print(f"    Idiomas: {voice.languages if voice.languages else 'No especificado'}")
            print(f"    Género: {voice.gender if voice.gender else 'No especificado'}")
        
        print("\n" + "=" * 60)
    
    def change_voice_by_index(self, index):
        """
        Cambia a una voz específica por su índice.
        
        Args:
            index (int): Índice de la voz (ver list_voices())
        """
        if not self.available_voices:
            print("❌ No hay voces disponibles")
            return False
        
        if 0 <= index < len(self.available_voices):
            voice = self.available_voices[index]
            self.current_voice = voice
            self.engine.setProperty('voice', voice.id)
            
            print(f"✓ Voz cambiada a: {voice.name}")
            return True
        else:
            print(f"❌ Índice inválido. Usa 0-{len(self.available_voices)-1}")
            return False
    
    def save_to_file(self, text, filename="neo_speech.mp3"):
        """
        Guarda el audio en un archivo.
        
        Args:
            text (str): Texto a sintetizar
            filename (str): Nombre del archivo de salida
        """
        if not self.engine:
            print("❌ Motor TTS no inicializado")
            return False
        
        try:
            text_clean = self._clean_text(text)
            self.engine.save_to_file(text_clean, filename)
            self.engine.runAndWait()
            
            print(f"✓ Audio guardado en: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar audio: {e}")
            return False
    
    def stop(self):
        """Detiene cualquier síntesis en curso"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

# ==========================================
# FUNCIONES GLOBALES (para compatibilidad)
# ==========================================

def inicializar_tts(rate=DEFAULT_RATE, volume=DEFAULT_VOLUME, debug=False):
    """
    Inicializa el sistema TTS global.
    
    Args:
        rate (int): Velocidad de habla
        volume (float): Volumen
        debug (bool): Modo debug
        
    Returns:
        NEOVoice: Instancia del sistema TTS
    """
    global _engine, _engine_initialized
    
    with _engine_lock:
        if not _engine_initialized:
            _engine = NEOVoice(rate=rate, volume=volume, debug=debug)
            _engine_initialized = True
            print("✓ Sistema TTS inicializado")
        
        return _engine

def neo_habla(texto, wait=True):
    """
    Función simple para que NEO hable.
    
    Args:
        texto (str): Lo que NEO dirá
        wait (bool): Si espera a terminar de hablar
    """
    global _engine
    
    if not _engine:
        _engine = inicializar_tts()
    
    _engine.speak(texto, wait=wait)

def neo_habla_async(texto):
    """NEO habla sin bloquear la ejecución"""
    global _engine
    
    if not _engine:
        _engine = inicializar_tts()
    
    _engine.speak_async(texto)

# ==========================================
# MODO DE PRUEBA
# ==========================================

def probar_tts():
    """Modo de prueba interactivo"""
    print("\n" + "=" * 60)
    print("MODO DE PRUEBA - Sistema TTS")
    print("=" * 60)
    
    # Inicializar con debug
    tts = NEOVoice(debug=True)
    
    # Pruebas básicas
    print("\n=== PRUEBA 1: Presentación ===")
    tts.speak("Hola, soy NEO, tu asistente inteligente")
    
    print("\n=== PRUEBA 2: Confirmación de comando ===")
    tts.speak("Abriendo Google Chrome")
    
    print("\n=== PRUEBA 3: Respuesta elaborada ===")
    tts.speak("He encontrado 5 resultados en tu búsqueda de Python tutorial")
    
    # Menú interactivo
    while True:
        print("\n" + "=" * 60)
        print("OPCIONES:")
        print("  1. Hacer que NEO hable")
        print("  2. Cambiar velocidad")
        print("  3. Cambiar volumen")
        print("  4. Listar voces disponibles")
        print("  5. Cambiar voz")
        print("  6. Guardar audio en archivo")
        print("  0. Salir")
        print("=" * 60)
        
        opcion = input("\n¿Qué hacer? (0-6): ").strip()
        
        if opcion == "1":
            texto = input("\n¿Qué quieres que diga NEO?: ")
            if texto:
                tts.speak(texto)
        
        elif opcion == "2":
            velocidad = input("\nVelocidad (80-300, actual: 160): ")
            try:
                tts.set_rate(int(velocidad))
                tts.speak("Probando nueva velocidad")
            except:
                print("❌ Velocidad inválida")
        
        elif opcion == "3":
            volumen = input("\nVolumen (0.0-1.0, actual: 0.9): ")
            try:
                tts.set_volume(float(volumen))
                tts.speak("Probando nuevo volumen")
            except:
                print("❌ Volumen inválido")
        
        elif opcion == "4":
            tts.list_voices()
        
        elif opcion == "5":
            tts.list_voices()
            indice = input("\n¿Qué voz usar? (número): ")
            try:
                if tts.change_voice_by_index(int(indice)):
                    tts.speak("Hola, esta es mi nueva voz")
            except:
                print("❌ Índice inválido")
        
        elif opcion == "6":
            texto = input("\n¿Qué texto guardar?: ")
            archivo = input("Nombre del archivo (Enter = neo_speech.mp3): ").strip()
            if not archivo:
                archivo = "neo_speech.mp3"
            tts.save_to_file(texto, archivo)
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            tts.speak("Hasta luego")
            break
        
        else:
            print("❌ Opción inválida")

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n✓ Módulo TTS cargado")
    print("\nModos disponibles:")
    print("  1. Modo prueba (interactivo)")
    print("  2. Solo cargar módulo")
    
    modo = input("\n¿Qué modo? (1/2): ").strip()
    
    if modo == "1":
        probar_tts()
    else:
        print("\n✓ Módulo listo para importar")
        print("\nEjemplo de uso:")
        print("  from neo_voz_tts import neo_habla")
        print("  neo_habla('Hola mundo')")