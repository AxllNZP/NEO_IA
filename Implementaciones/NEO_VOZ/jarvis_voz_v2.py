# jarvis_voz_v2.py - Con detección de silencio
import whisper
import pyaudio
import wave
import os
import numpy as np

print("=" * 50)
print("JARVIS - Sistema de Voz v0.2")
print("(Con detección automática de silencio)")
print("=" * 50)

# Configuración
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 2

audio = pyaudio.PyAudio()

print("\n[1] Inicializando micrófono...")
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("[2] ¡Listo! Esperando que hables...")
print("💡 Habla cuando quieras. Pararé cuando te calles.\n")

frames = []
silent_chunks = 0
max_silent_chunks = int(SILENCE_DURATION * RATE / CHUNK)
recording = False

try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        
        # Convertir audio a números para analizar volumen
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()
        
        # Si hay sonido (hablas)
        if volume > SILENCE_THRESHOLD:
            if not recording:
                print("🎤 Detectado: Grabando...")
                recording = True
            silent_chunks = 0
        else:
            # Si hay silencio
            if recording:
                silent_chunks += 1
                
        # Si llevamos 2 segundos en silencio, parar
        if recording and silent_chunks > max_silent_chunks:
            print("✓ Grabación completa (silencio detectado)")
            break
            
        # Máximo 30 segundos de grabación
        if len(frames) > int(RATE / CHUNK * 30):
            print("✓ Grabación completa (30 seg máximo)")
            break
            
except KeyboardInterrupt:
    print("\n⚠️  Grabación cancelada")

# Guardar y procesar
stream.stop_stream()
stream.close()
audio.terminate()

if len(frames) > 0:
    AUDIO_FILE = "temp_audio.wav"
    wf = wave.open(AUDIO_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print("[3] Cargando Whisper...")
    model = whisper.load_model("base")
    
    print("[4] Transcribiendo...")
    result = model.transcribe(AUDIO_FILE, language="es")
    
    print("\n" + "=" * 50)
    print("📝 DIJISTE:")
    print("=" * 50)
    print(f"\n'{result['text']}'")
    print("\n" + "=" * 50)
    
    os.remove(AUDIO_FILE)
else:
    print("⚠️  No se grabó nada")