# neo_voz.py - Sistema de reconocimiento de voz con Whisper
import whisper
import pyaudio
import wave
import numpy as np
import os
import time

print("=" * 60)
print("NEO - Sistema de Reconocimiento de Voz v1.0")
print("=" * 60)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 400
SILENCE_DURATION = 2.5
TEMP_AUDIO = "temp_audio.wav"

print("\n[1/1] Cargando Whisper...")
try:
    modelo = whisper.load_model("base")
    print("Whisper cargado correctamente")
except Exception as e:
    print(f"Error al cargar Whisper: {e}")
    exit(1)

def escuchar_audio(timeout=30, esperar_activacion=False):
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
        chunks_grabados = 0
        max
        max_chunks = int(timeout * RATE / CHUNK)
        
        if esperar_activacion:
            print("🎤 Esperando que hables...")
        
        while chunks_grabados < max_chunks:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
            except IOError:
                continue
            
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()
            
            if volume > SILENCE_THRESHOLD:
                if not recording:
                    if esperar_activacion:
                        print("Grabando...")
                    recording = True
                silent_chunks = 0
                frames.append(data)
            else:
                if recording:
                    silent_chunks += 1
                    frames.append(data)
                    
                    if silent_chunks > max_silent_chunks:
                        break
            
            chunks_grabados += 1
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        if len(frames) == 0:
            return None
        
        wf = wave.open(TEMP_AUDIO, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        duracion = len(frames) * CHUNK / RATE
        print(f"Audio capturado ({duracion:.1f}s)")
        return TEMP_AUDIO
        
    except Exception as e:
        print(f"Error en grabación: {e}")
        audio.terminate()
        return None

def transcribir_audio(archivo_audio):
    try:
        result = modelo.transcribe(archivo_audio, language="es")
        texto = result['text'].strip()
        return texto
    except Exception as e:
        print(f"Error en transcripción: {e}")
        return None

def probar_voz():
    print("\n" + "=" * 60)
    print("MODO DE PRUEBA")
    print("=" * 60)
    print("\nHabla cuando quieras. Pararé cuando te calles.\n")
    
    while True:
        print("-" * 60)
        input("\nPresiona Enter para grabar...")
        
        archivo = escuchar_audio(timeout=10, esperar_activacion=True)
        
        if not archivo:
            print(" No se grabó audio")
            continue
        
        print("Transcribiendo...")
        texto = transcribir_audio(archivo)
        
        if texto:
            print("\n" + "=" * 60)
            print("DIJISTE:")
            print("=" * 60)
            print(f"\n'{texto}'\n")
            print("=" * 60)
        else:
            print(" No se pudo transcribir")
        
        if os.path.exists(TEMP_AUDIO):
            os.remove(TEMP_AUDIO)
        
        print("\n¿Continuar? (si/no): ", end='')
        respuesta = input().strip().lower()
        
        if respuesta != 'si':
            print(" ¡Hasta luego!")
            break

if __name__ == "__main__":
    print("\nSistema de voz cargado")
    print("\nEste módulo reconoce voz en español\n")
    
    print("¿Probar el sistema? (si/no): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta == 'si':
        probar_voz()
    else:
        print("\nMódulo listo para importar")