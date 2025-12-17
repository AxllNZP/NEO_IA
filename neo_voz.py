# neo_voz.py - Sistema de reconocimiento de voz con Whisper [CORREGIDO]
import whisper
import pyaudio
import wave
import numpy as np
import os
import time

print("=" * 60)
print("NEO - Sistema de Reconocimiento de Voz v1.0")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN
# ==========================================
CHUNK = 1024                    # Tamaño de cada fragmento de audio
FORMAT = pyaudio.paInt16       # Formato de audio (16-bit)
CHANNELS = 1                    # Mono (1 canal)
RATE = 16000                   # 16kHz (óptimo para Whisper)
SILENCE_THRESHOLD = 400        # Umbral para detectar silencio
SILENCE_DURATION = 2.5         # Segundos de silencio para terminar
TEMP_AUDIO = "temp_audio.wav"  # Archivo temporal

# ==========================================
# CARGAR WHISPER
# ==========================================
print("\n[1/1] Cargando Whisper...")
try:
    modelo = whisper.load_model("base")
    print("✓ Whisper cargado correctamente")
except Exception as e:
    print(f"❌ Error al cargar Whisper: {e}")
    exit(1)

# ==========================================
# FUNCIÓN: escuchar_audio
# ==========================================
def escuchar_audio(timeout=30, esperar_activacion=False):
    """
    Escucha audio del micrófono hasta que detecta silencio.
    
    Args:
        timeout: Tiempo máximo de grabación en segundos
        esperar_activacion: Si True, muestra mensaje de espera
        
    Returns:
        str: Ruta al archivo de audio temporal
        None: Si no se grabó nada
    """
    audio = pyaudio.PyAudio()
    
    try:
        # Abrir stream de audio
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        # Variables de control
        frames = []                                      # Lista de fragmentos de audio
        silent_chunks = 0                               # Contador de chunks silenciosos
        max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)  # ⚠️ LÍNEA CORREGIDA
        recording = False                               # Si ya empezó a grabar
        chunks_grabados = 0                            # Total de chunks procesados
        max_chunks = int(timeout * RATE / CHUNK)       # Máximo de chunks permitidos
        
        if esperar_activacion:
            print("🎤 Esperando que hables...")
        
        # Bucle de grabación
        while chunks_grabados < max_chunks:
            try:
                # Leer chunk de audio
                data = stream.read(CHUNK, exception_on_overflow=False)
            except IOError:
                continue
            
            # Convertir a numpy para analizar
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            
            # Detectar si hay sonido
            if volume > SILENCE_THRESHOLD:
                # HAY SONIDO
                if not recording:
                    if esperar_activacion:
                        print("🔴 Grabando...")
                    recording = True
                silent_chunks = 0
                frames.append(data)
            else:
                # HAY SILENCIO
                if recording:
                    silent_chunks += 1
                    frames.append(data)
                    
                    # Si hay mucho silencio, terminar
                    if silent_chunks > max_silent_chunks:
                        break
            
            chunks_grabados += 1
        
        # Cerrar stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Verificar si se grabó algo
        if len(frames) == 0:
            return None
        
        # Guardar audio en archivo WAV
        wf = wave.open(TEMP_AUDIO, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        duracion = len(frames) * CHUNK / RATE
        print(f"✓ Audio capturado ({duracion:.1f}s)")
        return TEMP_AUDIO
        
    except Exception as e:
        print(f"❌ Error en grabación: {e}")
        audio.terminate()
        return None

# ==========================================
# FUNCIÓN: transcribir_audio
# ==========================================
def transcribir_audio(archivo_audio):
    """
    Transcribe un archivo de audio a texto usando Whisper.
    
    Args:
        archivo_audio: Ruta al archivo .wav
        
    Returns:
        str: Texto transcrito
        None: Si hubo error
    """
    try:
        # Transcribir con Whisper
        result = modelo.transcribe(archivo_audio, language="es")
        texto = result['text'].strip()
        return texto
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        return None

# ==========================================
# FUNCIÓN: probar_voz
# ==========================================
def probar_voz():
    """Modo de prueba interactivo para el reconocimiento de voz"""
    print("\n" + "=" * 60)
    print("MODO DE PRUEBA")
    print("=" * 60)
    print("\nHabla cuando quieras. Pararé cuando te calles.\n")
    
    while True:
        print("-" * 60)
        input("\nPresiona Enter para grabar...")
        
        # Escuchar audio
        archivo = escuchar_audio(timeout=10, esperar_activacion=True)
        
        if not archivo:
            print("⚠️  No se grabó audio")
            continue
        
        # Transcribir
        print("⏳ Transcribiendo...")
        texto = transcribir_audio(archivo)
        
        if texto:
            print("\n" + "=" * 60)
            print("DIJISTE:")
            print("=" * 60)
            print(f"\n'{texto}'\n")
            print("=" * 60)
        else:
            print("❌ No se pudo transcribir")
        
        # Limpiar archivo temporal
        if os.path.exists(TEMP_AUDIO):
            os.remove(TEMP_AUDIO)
        
        # Preguntar si continuar
        print("\n¿Continuar? (si/no): ", end='')
        respuesta = input().strip().lower()
        
        if respuesta != 'si':
            print("👋 ¡Hasta luego!")
            break

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("\n✓ Sistema de voz cargado")
    print("\nEste módulo reconoce voz en español\n")
    
    print("¿Probar el sistema? (si/no): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta == 'si':
        probar_voz()
    else:
        print("\n✓ Módulo listo para importar")