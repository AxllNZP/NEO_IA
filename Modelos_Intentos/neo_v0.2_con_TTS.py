# neo_v0.2_con_TTS.py - NEO COMPLETO con Sistema de Voz (TTS)
"""
NEO v0.2 Mejorado - Ahora con capacidad de hablar
Cambios:
- ✅ Integración de pyttsx3 para respuestas por voz
- ✅ NEO confirma cada acción hablando
- ✅ Respuestas más naturales
"""

import whisper
import pyaudio
import wave
import numpy as np
import os
import time
import subprocess
import json
import re

# NUEVO: Importar sistema TTS
from neo_voz_tts import inicializar_tts, neo_habla

print("=" * 60)
print("NEO v0.2 - Asistente Inteligente con VOZ")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN
# ==========================================

# Audio (Micrófono)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 400
SILENCE_DURATION = 2.5
MIN_AUDIO_LENGTH = 0.5

# Archivos temporales
TEMP_AUDIO = "temp_neo_audio.wav"

# Palabras de activación
PALABRAS_ACTIVACION = ['neo', 'neó', 'nio']

# Modelo Whisper
MODELO_WHISPER = "base"

# ==========================================
# INICIALIZACIÓN
# ==========================================

print("\n[1/4] Cargando Whisper...")
try:
    modelo_whisper = whisper.load_model(MODELO_WHISPER)
    print("✓ Whisper cargado")
except Exception as e:
    print(f"❌ Error al cargar Whisper: {e}")
    exit(1)

print("[2/4] Verificando Ollama...")
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("✓ Ollama funcionando")
    else:
        print("⚠️ Ollama no responde")
except:
    print("⚠️ Ollama no encontrado")

print("[3/4] Cargando sistema de memoria...")
try:
    import neo_memoria
    MEMORIA_DISPONIBLE = True
    print("✓ Sistema de memoria cargado")
except ImportError:
    MEMORIA_DISPONIBLE = False
    print("⚠️ neo_memoria.py no encontrado")

# NUEVO: Inicializar TTS
print("[4/4] Inicializando sistema TTS...")
try:
    tts = inicializar_tts(rate=140, volume=0.9, debug=False)
    print("✓ Sistema TTS listo")
    
    # Saludo inicial
    neo_habla("Hola, soy Neo. Estoy listo para ayudarte")
except Exception as e:
    print(f"⚠️ TTS no disponible: {e}")
    tts = None

print("\n" + "=" * 60)
print("✅ NEO listo para usar")
print("=" * 60)

# ==========================================
# FUNCIONES DE CONTROL (PyAutoGUI)
# ==========================================

import pyautogui
pyautogui.PAUSE = 0.5

def abrir_programa(nombre):
    print(f"   Abriendo {nombre}...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write(nombre, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_chrome():
    abrir_programa('chrome')

def abrir_notepad():
    abrir_programa('notepad')

def abrir_calculadora():
    abrir_programa('calc')

def abrir_explorador():
    print("   Abriendo Explorador...")
    pyautogui.hotkey('win', 'e')

def minimizar_todo():
    print("   Minimizando todo...")
    pyautogui.hotkey('win', 'd')

def cerrar_ventana():
    print("   Cerrando ventana...")
    pyautogui.hotkey('alt', 'f4')

def volumen_subir(veces=3):
    print(f"   Subiendo volumen {veces}x...")
    for _ in range(veces):
        pyautogui.press('volumeup')
        time.sleep(0.1)

def volumen_bajar(veces=3):
    print(f"   Bajando volumen {veces}x...")
    for _ in range(veces):
        pyautogui.press('volumedown')
        time.sleep(0.1)

def esperar(segundos):
    print(f"   Esperando {segundos}s...")
    time.sleep(segundos)

def buscar_en_google(query):
    print(f"   Buscando en Google: {query}")
    abrir_chrome()
    time.sleep(2)
    pyautogui.write(query, interval=0.05)
    pyautogui.press('enter')

def escribir_texto(texto):
    print(f"   Escribiendo texto: {texto}")
    pyautogui.write(texto, interval=0.05)

# ==========================================
# CEREBRO - PROCESAR COMANDOS
# ==========================================

FUNCIONES_DISPONIBLES = """
PROGRAMAS:
- abrir_chrome()
- abrir_notepad()
- abrir_calculadora()
- abrir_explorador()
- abrir_programa('nombre')

ACCIONES:
- minimizar_todo()
- cerrar_ventana()
- buscar_en_google('query')

VOLUMEN:
- volumen_subir(veces)
- volumen_bajar(veces)

SISTEMA:
- esperar(segundos)

ESCRITURA:
- escribir_texto('texto')
"""

def extraer_json(texto):
    """Extrae JSON de respuesta"""
    try:
        return json.loads(texto)
    except:
        pass
    
    match = re.search(r'\{.*\}', texto, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except:
            pass
    return None

def procesar_comando(comando):
    """Procesa comando con Llama y genera plan"""
    print(f"\n🧠 Analizando: '{comando}'")

    # NUEVO: Notificar por voz que está procesando
    if tts:
        neo_habla("Procesando", wait=False)

    # Guardar en log
    if MEMORIA_DISPONIBLE:
        neo_memoria.guardar_log(f"Procesando comando: {comando}")
    
    # Comandos rápidos (sin IA)
    comando_lower = comando.lower()
    
    if comando_lower.startswith('abre '):
        programa = comando[5:].strip()
        return {
            "acciones": [{"funcion": "abrir_programa", "args": [programa]}],
            "explicacion": f"Abriendo {programa}"
        }
    
    if comando_lower.startswith('busca '):
        query = comando[6:].strip()
        return {
            "acciones": [
                {"funcion": "abrir_chrome", "args": []},
                {"funcion": "esperar", "args": [2]},
                {"funcion": "buscar_en_google", "args": [query]}
            ],
            "explicacion": f"Buscando {query}"
        }
    
    if 'minimiza' in comando_lower:
        return {
            "acciones": [{"funcion": "minimizar_todo", "args": []}],
            "explicacion": "Minimizando ventanas"
        }
    
    # COMANDOS DE MEMORIA
    if MEMORIA_DISPONIBLE:
        if 'repite' in comando_lower or 'hazlo de nuevo' in comando_lower:
            ultimo = neo_memoria.obtener_ultimo_comando()
            if ultimo and ultimo['exito']:
                print(f"💭 Repitiendo: '{ultimo['comando']}'")
                # NUEVO: Confirmar por voz
                if tts:
                    neo_habla("Repitiendo último comando")
                return procesar_comando(ultimo['comando'])
            else:
                return {
                    "acciones": [],
                    "explicacion": "No hay comando anterior para repetir",
                    "respuesta_directa": True
                }
    
    # Si no es comando rápido, usar Llama
    print("💭 Consultando IA...")
    
    prompt = f"""Convierte este comando a JSON.

COMANDO: "{comando}"

{FUNCIONES_DISPONIBLES}

Formato JSON (solo JSON, nada más):
{{"acciones": [{{"funcion": "nombre", "args": []}}], "explicacion": "texto"}}

Ejemplos:
"abre Chrome"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}], "explicacion": "Abriendo Chrome"}}

"abre notepad y escribe hola"
{{"acciones": [{{"funcion": "abrir_notepad", "args": []}}, {{"funcion": "esperar", "args": [1]}}, {{"funcion": "escribir_texto", "args": ["hola"]}}], "explicacion": "Abriendo notepad y escribiendo hola"}}

Procesa: "{comando}"
JSON:"""
    
    try:
        resultado = subprocess.run(
            ["ollama", "run", "llama3.2:3b"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        
        plan = extraer_json(resultado.stdout.strip())
        
        if plan:
            print(f"✓ Plan: {plan.get('explicacion', 'Sin explicación')}")
            return plan
        else:
            print("⚠️ No se pudo extraer plan válido")
        
    except Exception as e:
        print(f"❌ Error en IA: {e}")
    
    return None

def ejecutar_plan(plan):
    """Ejecuta el plan de acciones"""
    if not plan or 'acciones' not in plan:
        return False
    
    acciones = plan['acciones']
    total = len(acciones)
    
    # NUEVO: Anunciar qué hará NEO
    explicacion = plan.get('explicacion', '')
    if explicacion and tts:
        neo_habla(explicacion, wait=False)
    
    print(f"\n🚀 Ejecutando {total} acción(es):\n")
    
    for i, accion in enumerate(acciones, 1):
        funcion = accion.get('funcion', '')
        args = accion.get('args', [])
        
        print(f"[{i}/{total}]", end=' ')
        
        try:
            if funcion == 'abrir_chrome':
                abrir_chrome()
            elif funcion == 'abrir_notepad':
                abrir_notepad()
            elif funcion == 'escribir_texto':
                escribir_texto(args[0] if args else '')
            elif funcion == 'abrir_calculadora':
                abrir_calculadora()
            elif funcion == 'abrir_explorador':
                abrir_explorador()
            elif funcion == 'abrir_programa':
                abrir_programa(args[0] if args else '')
            elif funcion == 'minimizar_todo':
                minimizar_todo()
            elif funcion == 'cerrar_ventana':
                cerrar_ventana()
            elif funcion == 'buscar_en_google':
                buscar_en_google(args[0] if args else '')
            elif funcion == 'volumen_subir':
                volumen_subir(args[0] if args else 3)
            elif funcion == 'volumen_bajar':
                volumen_bajar(args[0] if args else 3)
            elif funcion == 'esperar':
                esperar(args[0] if args else 1)
            else:
                print(f"⚠️ Función desconocida: {funcion}")
                continue
            
            print("  ✓")
            time.sleep(0.3)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    print("\n✅ Completado")
    
    # NUEVO: Confirmar finalización por voz
    if tts:
        neo_habla("Listo", wait=False)
    
    return True

# ==========================================
# VOZ - ESCUCHAR
# ==========================================

def escuchar_audio():
    """Escucha y graba audio del micrófono"""
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
                    print("🎤 Grabando...")
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
        
        # Guardar audio
        wf = wave.open(TEMP_AUDIO, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return TEMP_AUDIO
        
    except Exception as e:
        print(f"❌ Error en grabación: {e}")
        audio.terminate()
        return None

def transcribir_audio(archivo):
    """Transcribe audio a texto"""
    try:
        result = modelo_whisper.transcribe(archivo, language="es")
        return result['text'].strip()
    except Exception as e:
        print(f"❌ Error en transcripción: {e}")
        return None

def detectar_activacion(texto):
    """Detecta si dijo 'NEO'"""
    texto_lower = texto.lower()
    
    for palabra in PALABRAS_ACTIVACION:
        if palabra in texto_lower:
            comando = texto_lower.replace(palabra, '').strip()
            return True, comando
    
    return False, texto

# ==========================================
# MODO TEXTO (para probar sin voz)
# ==========================================

def modo_texto():
    """Modo de prueba sin micrófono"""
    print("\n" + "=" * 60)
    print("📝 MODO TEXTO - Sin voz (para pruebas)")
    print("=" * 60)
    print("\nEscribe comandos directamente")
    print("   No necesitas decir 'NEO', solo el comando\n")
    
    while True:
        try:
            comando = input("\n💬 Tu comando (o 'salir'): ").strip()
            
            if comando.lower() in ['salir', 'exit']:
                print("👋 ¡Hasta luego!")
                # NUEVO: Despedida por voz
                if tts:
                    neo_habla("Hasta luego")
                break
            
            if not comando:
                continue
            
            # Procesar y ejecutar
            plan = procesar_comando(comando)
            
            if plan:
                exito = ejecutar_plan(plan)
                
                # Guardar en memoria
                if MEMORIA_DISPONIBLE:
                    neo_memoria.guardar_comando(comando, plan, exito)
                
                if exito:
                    print("\n✅ Comando completado")
                    if MEMORIA_DISPONIBLE:
                        neo_memoria.guardar_log(f"Comando exitoso: {comando}")
                else:
                    print("\n⚠️ Hubo un problema")
                    if MEMORIA_DISPONIBLE:
                        neo_memoria.guardar_log(f"Error al ejecutar: {comando}", "ERROR")
            else:
                print("⚠️ No se pudo procesar el comando")
                if MEMORIA_DISPONIBLE:
                    neo_memoria.guardar_log(f"No se generó plan para: {comando}", "WARNING")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo...")
            if tts:
                neo_habla("Adiós")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# ==========================================
# MODO VOZ (loop principal)
# ==========================================

def modo_voz():
    """Loop principal con voz"""
    print("\n" + "=" * 60)
    print("🎧 NEO ESCUCHANDO - Modo Voz")
    print("=" * 60)
    print("\nDi 'NEO' seguido de tu comando")
    print("Ejemplo: 'NEO, abre Chrome'")
    print("Presiona Ctrl+C para salir\n")
    
    while True:
        try:
            print("🎤 Esperando que hables...")
            
            # Escuchar
            archivo = escuchar_audio()
            
            if not archivo:
                continue
            
            # Transcribir
            texto = transcribir_audio(archivo)
            
            if not texto:
                continue
            
            print(f"📝 Escuché: '{texto}'")
            
            # Detectar activación
            activado, comando = detectar_activacion(texto)
            
            if activado:
                if comando:
                    print("✅ NEO activado\n")
                    
                    # Procesar y ejecutar
                    plan = procesar_comando(comando)
                    
                    if plan:
                        exito = ejecutar_plan(plan)
                        
                        # Guardar en memoria
                        if MEMORIA_DISPONIBLE:
                            neo_memoria.guardar_comando(comando, plan, exito)
                    else:
                        print("⚠️ No entendí el comando")
                        # NUEVO: Avisar por voz
                        if tts:
                            neo_habla("No entendí el comando")
                        
                        if MEMORIA_DISPONIBLE:
                            neo_memoria.guardar_log(f"Comando no entendido: {comando}", "WARNING")
                else:
                    print("⚠️ Dijiste 'NEO' pero sin comando")
                    # NUEVO: Pedir que repita
                    if tts:
                        neo_habla("No escuché tu comando, por favor repite")
            else:
                print("⚠️ No detecté 'NEO'\n")
            
            # Limpiar
            if os.path.exists(TEMP_AUDIO):
                os.remove(TEMP_AUDIO)
                
        except KeyboardInterrupt:
            print("\n\n👋 Apagando NEO...")
            if tts:
                neo_habla("Apagando sistema, hasta luego")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(1)

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  MODOS DISPONIBLES")
    print("=" * 60)
    print("\n1. Modo VOZ (usa micrófono)")
    print("2. Modo TEXTO (escribes comandos)")
    print("3. Probar TTS (solo voz de salida)")
    print("4. Salir")
    
    modo = input("\n¿Qué modo? (1/2/3/4): ").strip()
    
    if modo == "1":
        print("\n⚠️ Asegúrate de que tu micrófono funcione")
        input("Presiona Enter cuando estés listo...")
        modo_voz()
        
    elif modo == "2":
        modo_texto()
    
    elif modo == "3":
        if tts:
            print("\n=== PRUEBA DE TTS ===")
            neo_habla("Hola, soy Neo, tu asistente inteligente")
            time.sleep(1)
            neo_habla("Puedo abrir programas, buscar en internet y controlar tu computadora")
            time.sleep(1)
            neo_habla("¿En qué puedo ayudarte hoy?")
        else:
            print("❌ TTS no disponible")
        
    else:
        print("\n👋 ¡Hasta luego!")
    
    # Limpiar archivos temporales
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)
    
    print("\n✓ NEO apagado correctamente")