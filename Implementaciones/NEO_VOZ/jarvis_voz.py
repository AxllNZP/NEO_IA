# jarvis_voz.py - Sistema de reconocimiento de voz
import whisper
import pyaudio
import wave
import os

print("=" * 50)
print("JARVIS - Sistema de Voz v0.1")
print("=" * 50)

# PASO 1: Configurar micrófono
print("\n[1] Configurando micrófono...")
CHUNK = 1024              # Tamaño de cada "pedazo" de audio
FORMAT = pyaudio.paInt16  # Formato de audio (16-bit)
CHANNELS = 1              # Mono (1 canal)
RATE = 16000              # 16kHz (suficiente para voz)
RECORD_SECONDS = 10        # Duración de grabación

# PASO 2: Inicializar PyAudio
audio = pyaudio.PyAudio()

print("[2] Micrófono listo!")
print("\n⏺️  Presiona ENTER para grabar (5 segundos)...")
input()

# PASO 3: Grabar audio
print("🎤 GRABANDO... habla ahora!")

stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

frames = []  # Aquí guardaremos el audio

# Grabar durante 5 segundos
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("✓ Grabación completa!")

# PASO 4: Guardar audio en archivo temporal
stream.stop_stream()
stream.close()
audio.terminate()

AUDIO_FILE = "temp_audio.wav"
wf = wave.open(AUDIO_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("[3] Audio guardado temporalmente")

# PASO 5: Cargar Whisper y transcribir
print("[4] Cargando Whisper... (esto toma 10-15 seg)")
model = whisper.load_model("base")

print("[5] Transcribiendo tu voz...")
result = model.transcribe(AUDIO_FILE, language="es")

# PASO 6: Mostrar resultado
print("\n" + "=" * 50)
print("📝 ESTO ES LO QUE DIJISTE:")
print("=" * 50)
print(f"\n'{result['text']}'")
print("\n" + "=" * 50)

# PASO 7: Limpiar archivo temporal
os.remove(AUDIO_FILE)
print("\n✓ Proceso completado!")