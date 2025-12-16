# ==========================================
# NEO v1.0 - SISTEMA COMPLETO
# Asistente de voz inteligente con visión
# ==========================================

import whisper
import pyaudio
import wave
import numpy as np
import os
import time
from datetime import datetime

# Importar nuestros módulos
import neo_cerebro
import neo_control

print("=" * 60)
print("🤖 NEO v1.0 - Asistente Inteligente")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN
# ==========================================

# ==========================================
# CONFIGURACIÓN DE AUDIO MEJORADA
# ==========================================

# Parámetros básicos
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Detección de voz (ajustables)
SILENCE_THRESHOLD = 400        # Bajado de 500 (más sensible)
SILENCE_DURATION = 2.5         # Aumentado de 2 (espera más antes de cortar)
MIN_AUDIO_LENGTH = 0.5         # Mínimo 0.5 segundos de audio

# Grabación
MAX_RECORDING_TIME = 15        # Máximo 15 segundos de grabación
ACTIVATION_TIMEOUT = 10        # 10 segundos esperando activación

#---------------------------------------------------------------------------------------------------------------

# Palabras de activación (variaciones que Whisper puede detectar)
PALABRAS_ACTIVACION = [
    'neo', 'neó', 'nio', 'neo.', 'neo,',  # Básicas
    'oye neo', 'hey neo', 'hola neo',      # Con saludo
    'nео',  # Caracteres similares
]

# ==========================================
# Whisper
MODELO_WHISPER = "base"          # Modelo principal (rápido)
MODELO_WHISPER_PRECISO = "small" # Modelo de respaldo (más preciso)
usar_modelo_preciso = False       # Se activa si hay errores

# Archivos temporales
TEMP_AUDIO = "temp_neo_audio.wav"

# ==========================================
# CARGAR MODELOS
# ==========================================

print("\n[1/2] Cargando Whisper...")
try:
    modelo_whisper = whisper.load_model(MODELO_WHISPER)
    print("✓ Whisper cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar Whisper: {e}")
    exit(1)

print("[2/2] Verificando Ollama...")
import subprocess
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("✓ Ollama funcionando correctamente")
    else:
        print("⚠️ Ollama no responde correctamente")
except:
    print("⚠️ Ollama no encontrado")

print("\n" + "=" * 60)
print("✅ NEO listo para usar")
print("=" * 60)

# ==========================================
# FUNCIÓN: ESCUCHAR AUDIO MEJORADA
# ==========================================

def escuchar_audio(timeout=None, esperar_activacion=False):
    """
    Escucha audio del micrófono con detección inteligente de silencio
    
    MEJORAS v2:
    - Calibración automática de ruido de fondo
    - Detección más precisa de voz
    - Validación de longitud mínima
    - Mejor manejo de errores
    
    Args:
        timeout (int): Tiempo máximo de grabación (None = usar MAX_RECORDING_TIME)
        esperar_activacion (bool): Si True, espera sonido antes de grabar
    
    Returns:
        str: Ruta del archivo de audio, o None si falló
    """
    if timeout is None:
        timeout = MAX_RECORDING_TIME
    
    audio = pyaudio.PyAudio()
    
    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        # CALIBRACIÓN: Medir ruido de fondo durante 0.5 segundos
        if esperar_activacion:
            print("🎤 Calibrando micrófono...")
            calibration_frames = int(0.5 * RATE / CHUNK)
            noise_samples = []
            
            for _ in range(calibration_frames):
                data = stream.read(CHUNK)
                audio_data = np.frombuffer(data, dtype=np.int16)
                noise_samples.append(np.abs(audio_data).mean())
            
            # Calcular umbral dinámico (ruido promedio + margen)
            avg_noise = np.mean(noise_samples)
            dynamic_threshold = max(avg_noise * 2, SILENCE_THRESHOLD)
            
            print(f"📊 Ruido ambiente: {avg_noise:.0f} | Umbral: {dynamic_threshold:.0f}")
        else:
            dynamic_threshold = SILENCE_THRESHOLD
        
        frames = []
        silent_chunks = 0
        max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)
        recording = False
        chunks_grabados = 0
        max_chunks = int(timeout * RATE / CHUNK)
        
        if esperar_activacion:
            print("🎤 Listo. Esperando que hables...")
        
        # LOOP DE GRABACIÓN
        while chunks_grabados < max_chunks:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
            except IOError as e:
                print(f"⚠️ Error de audio: {e}")
                continue
            
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            
            # Detectar si hay sonido (voz)
            if volume > dynamic_threshold:
                if not recording:
                    if esperar_activacion:
                        print("🎤 Grabando...")
                    recording = True
                
                silent_chunks = 0
                frames.append(data)
            else:
                # Hay silencio
                if recording:
                    silent_chunks += 1
                    frames.append(data)
                    
                    # Si hay silencio prolongado, parar
                    if silent_chunks > max_silent_chunks:
                        break
            
            chunks_grabados += 1
        
        # LIMPIEZA
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # VALIDACIÓN: Verificar longitud mínima
        if len(frames) == 0:
            return None
        
        duracion = len(frames) * CHUNK / RATE
        
        if duracion < MIN_AUDIO_LENGTH:
            print(f"⚠️ Audio muy corto ({duracion:.1f}s), descartando...")
            return None
        
        # GUARDAR AUDIO
        wf = wave.open(TEMP_AUDIO, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"✓ Audio capturado ({duracion:.1f}s)")
        return TEMP_AUDIO
        
    except Exception as e:
        print(f"❌ Error en grabación: {e}")
        try:
            audio.terminate()
        except:
            pass
        return None

# ==========================================
# FUNCIÓN: TRANSCRIBIR AUDIO MEJORADA
# ==========================================

def transcribir_audio(archivo_audio, intentar_preciso=False):
    """
    Transcribe audio a texto con sistema de respaldo
    
    MEJORAS v2:
    - Intenta con modelo base primero (rápido)
    - Si falla o está vacío, usa modelo preciso (lento pero mejor)
    - Filtrado de ruido en texto
    
    Args:
        archivo_audio (str): Ruta del archivo
        intentar_preciso (bool): Forzar uso de modelo preciso
    
    Returns:
        str: Texto transcrito, o None si falló
    """
    global usar_modelo_preciso
    
    # Decidir qué modelo usar
    if intentar_preciso or usar_modelo_preciso:
        modelo_actual = MODELO_WHISPER_PRECISO
        print("🔍 Usando modelo preciso...")
    else:
        modelo_actual = MODELO_WHISPER
    
    try:
        # Transcribir
        result = modelo_whisper.transcribe(
            archivo_audio, 
            language="es",
            fp16=False,  # Forzar FP32 en CPU
            temperature=0.0,  # Más determinista
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6
        )
        
        texto = result['text'].strip()
        
        # FILTRADO: Remover artefactos comunes
        texto = texto.replace('[música]', '')
        texto = texto.replace('[sonido]', '')
        texto = texto.replace('...', '')
        texto = texto.strip()
        
        # VALIDACIÓN: ¿El texto está vacío o es muy corto?
        if len(texto) < 2:
            if not intentar_preciso and not usar_modelo_preciso:
                print("⚠️ Texto vacío, reintentando con modelo preciso...")
                return transcribir_audio(archivo_audio, intentar_preciso=True)
            return None
        
        # VALIDACIÓN: ¿Solo tiene puntuación o números?
        if texto.replace('.', '').replace(',', '').replace(' ', '').isdigit():
            return None
        
        return texto
        
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        
        # Si falló con base, intentar con preciso
        if not intentar_preciso and not usar_modelo_preciso:
            print("💡 Activando modelo preciso para futuros comandos...")
            usar_modelo_preciso = True
            return transcribir_audio(archivo_audio, intentar_preciso=True)
        
        return None
# ==========================================
# FUNCIÓN: DETECTAR ACTIVACIÓN MEJORADA
# ==========================================

def detectar_activacion(texto):
    """
    Detecta la palabra de activación con más flexibilidad
    
    MEJORAS v2:
    - Detecta variaciones con/sin puntuación
    - Permite activación al inicio o al final
    - Maneja mejor el texto limpio
    
    Args:
        texto (str): Texto transcrito
    
    Returns:
        tuple: (activado, comando_limpio)
    """
    texto_lower = texto.lower()
    texto_limpio = texto_lower.strip('.,-;:!¡?¿ ')
    
    # Buscar cada variación de activación
    for palabra in PALABRAS_ACTIVACION:
        palabra_limpia = palabra.strip('.,-;:!¡?¿ ')
        
        # CASO 1: "NEO al inicio"
        if texto_limpio.startswith(palabra_limpia):
            comando = texto_limpio[len(palabra_limpia):].strip('.,-;:!¡?¿ ')
            return True, comando
        
        # CASO 2: "NEO al final" (menos común pero válido)
        if texto_limpio.endswith(palabra_limpia):
            comando = texto_limpio[:-len(palabra_limpia)].strip('.,-;:!¡?¿ ')
            return True, comando
        
        # CASO 3: "NEO en medio" (con espacios)
        if f' {palabra_limpia} ' in f' {texto_limpio} ':
            # Tomar solo lo que viene después de NEO
            partes = texto_limpio.split(palabra_limpia, 1)
            if len(partes) > 1:
                comando = partes[1].strip('.,-;:!¡?¿ ')
                return True, comando
    
    return False, texto

# ==========================================
# FUNCIÓN: CAPTURAR PANTALLA (OPCIONAL)
# ==========================================

def necesita_contexto_visual(comando):
    """
    Determina si el comando necesita ver la pantalla
    
    Args:
        comando (str): Comando del usuario
    
    Returns:
        bool: True si necesita contexto visual
    """
    palabras_visuales = [
        'esto', 'esta', 'eso', 'aquí', 'ahí',
        'ventana', 'pantalla', 'esto que veo',
        'lo que está abierto', 'lo que hay'
    ]
    
    comando_lower = comando.lower()
    return any(palabra in comando_lower for palabra in palabras_visuales)

def obtener_contexto_pantalla():
    """
    Captura la pantalla y la analiza con LLaVA
    
    Returns:
        str: Descripción de lo que hay en pantalla, o None
    """
    print("👁️ Analizando pantalla...")
    
    try:
        import mss
        import mss.tools
        from PIL import Image
        
        # Capturar pantalla
        sct = mss.mss()
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        temp_screen = "temp_neo_screen.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=temp_screen)
        
        # Optimizar
        img = Image.open(temp_screen)
        if img.size[0] > 1280:
            ratio = 1280 / img.size[0]
            new_size = (1280, int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img.save(temp_screen, optimize=True, quality=85)
        
        # Analizar con LLaVA
        prompt = "Describe brevemente lo que ves en esta captura de pantalla en español. Menciona qué programas están abiertos y qué contenido hay visible."
        
        command = f'ollama run llava:7b "Analiza: {temp_screen}. {prompt}"'
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        # Limpiar archivo temporal
        if os.path.exists(temp_screen):
            os.remove(temp_screen)
        
        if result.stdout:
            return result.stdout.strip()
        else:
            return None
            
    except Exception as e:
        print(f"⚠️ Error al analizar pantalla: {e}")
        return None

# ==========================================
# FUNCIÓN: PROCESAR COMANDO COMPLETO
# ==========================================

def procesar_comando_completo(comando):
    """
    Procesa un comando completo: analiza, decide y ejecuta
    
    Args:
        comando (str): Comando del usuario
    
    Returns:
        bool: True si se ejecutó correctamente
    """
    print(f"\n💬 Comando recibido: '{comando}'")
    
    # Verificar si necesita contexto visual
    contexto = ""
    if necesita_contexto_visual(comando):
        contexto = obtener_contexto_pantalla()
        if contexto:
            print(f"👁️ Contexto: {contexto[:100]}...")
    
    # Procesar con el cerebro
    plan = neo_cerebro.procesar_comando(comando, contexto)
    
    if plan:
        # Ejecutar el plan
        exito = neo_cerebro.ejecutar_plan(plan)
        return exito
    else:
        print("❌ No pude entender el comando")
        return False

# ==========================================
# FUNCIÓN: LOOP PRINCIPAL
# ==========================================

def loop_principal():
    """
    Loop principal de NEO - escucha continuamente
    """
    print("\n" + "=" * 60)
    print("🎧 NEO está escuchando...")
    print("=" * 60)
    print("\n💡 Di 'NEO' seguido de tu comando")
    print("💡 Ejemplo: 'NEO, abre Chrome'")
    print("💡 Presiona Ctrl+C para salir\n")
    
    intentos_fallidos = 0
    
    while True:
        try:
            # Escuchar audio
            archivo_audio = escuchar_audio(timeout=10, esperar_activacion=True)
            
            if not archivo_audio:
                continue
            
            # Transcribir
            texto = transcribir_audio(archivo_audio)
            
            if not texto:
                continue
            
           # Mostrar lo que escuchó
            print(f"📝 Escuché: '{texto}'")
            
            # Detectar activación
            activado, comando = detectar_activacion(texto)
            
            # DEBUG: Mostrar detección
            if activado:
                if comando:
                    print(f"✓ Activación detectada | Comando: '{comando}'")
                else:
                    print(f"⚠️ Activación detectada pero sin comando")
            else:
                print(f"⚠️ No se detectó 'NEO' en el texto")
            
            if activado:
                if comando:
                    print("✓ NEO activado")
                    intentos_fallidos = 0
                    
                    # Procesar comando
                    exito = procesar_comando_completo(comando)
                    
                    if exito:
                        print("\n✅ Comando completado")
                    else:
                        print("\n⚠️ Hubo un problema al ejecutar")
                    
                    print("\n🎧 Esperando siguiente comando...\n")
                else:
                    print("💭 Dijiste 'NEO' pero no escuché un comando")
                    print("    Intenta: 'NEO, abre Chrome'\n")
            else:
                # No se detectó activación
                intentos_fallidos += 1
                if intentos_fallidos % 5 == 0:
                    print("💡 Recuerda decir 'NEO' antes de tu comando\n")
            
            # Limpiar archivo temporal
            if os.path.exists(TEMP_AUDIO):
                os.remove(TEMP_AUDIO)
                
        except KeyboardInterrupt:
            print("\n\n👋 Apagando NEO...")
            break
            
        except Exception as e:
            print(f"\n⚠️ Error inesperado: {e}")
            print("Continuando...\n")
            time.sleep(1)

# ==========================================
# FUNCIÓN: MODO DE PRUEBA SIN VOZ
# ==========================================

def modo_prueba_texto():
    """
    Modo de prueba donde escribes comandos en texto
    Útil para probar sin usar el micrófono
    """
    print("\n" + "=" * 60)
    print("📝 MODO DE PRUEBA (sin voz)")
    print("=" * 60)
    print("\n💡 Escribe comandos como si se los dijeras a NEO")
    print("💡 No necesitas escribir 'NEO', solo el comando")
    print("💡 Escribe 'salir' para terminar\n")
    
    while True:
        try:
            comando = input("💬 Tu comando: ").strip()
            
            if comando.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not comando:
                continue
            
            # Procesar comando
            exito = procesar_comando_completo(comando)
            
            if exito:
                print("\n✅ Comando completado\n")
            else:
                print("\n⚠️ Hubo un problema\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo...")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {e}\n")

# ==========================================
# FUNCIÓN: CONFIGURACIÓN INTERACTIVA
# ==========================================

def configurar_microfono():
    """
    Permite ajustar la sensibilidad del micrófono interactivamente
    """
    global SILENCE_THRESHOLD, SILENCE_DURATION
    
    print("\n" + "=" * 60)
    print("⚙️ CONFIGURACIÓN DEL MICRÓFONO")
    print("=" * 60)
    
    print(f"\n📊 Configuración actual:")
    print(f"   - Umbral de silencio: {SILENCE_THRESHOLD}")
    print(f"   - Duración de silencio: {SILENCE_DURATION}s")
    
    print("\n💡 Ajustes recomendados según tu ambiente:")
    print("\n   🔇 Lugar SILENCIOSO (oficina callada, noche):")
    print("      - Umbral: 300-400")
    print("      - Duración: 2.0s")
    
    print("\n   🔊 Lugar con RUIDO MODERADO (casa, día):")
    print("      - Umbral: 500-600")
    print("      - Duración: 2.5s")
    
    print("\n   📢 Lugar RUIDOSO (calle, música de fondo):")
    print("      - Umbral: 700-900")
    print("      - Duración: 3.0s")
    
    cambiar = input("\n¿Quieres cambiar la configuración? (si/no): ").strip().lower()
    
    if cambiar == 'si':
        try:
            nuevo_umbral = input(f"\nNuevo umbral de silencio [{SILENCE_THRESHOLD}]: ").strip()
            if nuevo_umbral:
                SILENCE_THRESHOLD = int(nuevo_umbral)
                print(f"✓ Umbral actualizado a {SILENCE_THRESHOLD}")
            
            nueva_duracion = input(f"Nueva duración de silencio [{SILENCE_DURATION}s]: ").strip()
            if nueva_duracion:
                SILENCE_DURATION = float(nueva_duracion)
                print(f"✓ Duración actualizada a {SILENCE_DURATION}s")
            
            print("\n✅ Configuración guardada")
        except ValueError:
            print("⚠️ Valores inválidos, usando configuración por defecto")
    
    print("\n" + "=" * 60)





# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MODOS DISPONIBLES")
    print("=" * 60)
    print("\n1. Modo VOZ (escucha tu micrófono)")
    print("2. Modo TEXTO (escribes los comandos)")
    print("3. Configurar micrófono")
    print("4. Salir")
    
    modo = input("\n¿Qué modo? (1/2/3/4): ").strip()
    
    if modo == "1":
        print("\n⚠️ Asegúrate de que tu micrófono esté conectado")
        
        # Opción de configurar antes
        config = input("¿Configurar micrófono primero? (si/no): ").strip().lower()
        if config == 'si':
            configurar_microfono()
        
        input("\nPresiona Enter cuando estés listo...")
        loop_principal()
        
    elif modo == "2":
        modo_prueba_texto()
        
    elif modo == "3":
        configurar_microfono()
        print("\n💡 Ahora puedes ejecutar el programa de nuevo con la nueva configuración")
        
    else:
        print("\n👋 ¡Hasta luego!")
    
    modo = input("\n¿Qué modo? (1/2/3): ").strip()
    
    if modo == "1":
        print("\n⚠️ Asegúrate de que tu micrófono esté conectado")
        input("Presiona Enter cuando estés listo...")
        loop_principal()
        
    elif modo == "2":
        modo_prueba_texto()
        
    else:
        print("\n👋 ¡Hasta luego!")
    
    # Limpiar archivos temporales
    for archivo in [TEMP_AUDIO, "temp_neo_screen.png"]:
        if os.path.exists(archivo):
            os.remove(archivo)
    
    print("\n✓ NEO apagado correctamente")