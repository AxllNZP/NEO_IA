# neo_v1.py - NEO COMPLETO - Integración total
import whisper
import pyaudio
import wave
import numpy as np
import os
import time
import subprocess
import json
import re

print("=" * 60)
print("NEO v0.2 - Asistente Inteligente con Memoria")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN
# ==========================================

# Audio
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
# CARGAR WHISPER
# ==========================================

print("\n[1/3] Cargando Whisper...")
try:
    modelo_whisper = whisper.load_model(MODELO_WHISPER)
    print(" Whisper cargado")
except Exception as e:
    print(f" Error al cargar Whisper: {e}")
    exit(1)

print("[2/3] Verificando Ollama...")
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print(" Ollama funcionando")
    else:
        print(" Ollama no responde")
except:
    print(" Ollama no encontrado")

print("[3/3] Cargando sistema de memoria...")
try:
    import neo_memoria
    MEMORIA_DISPONIBLE = True
    print(" Sistema de memoria cargado")
except ImportError:
    MEMORIA_DISPONIBLE = False
    print("⚠️  neo_memoria.py no encontrado")

print("\n" + "=" * 60)
print(" NEO listo para usar")
print("=" * 60)


# ==========================================
# FUNCIÓN: CAPTURAR Y ANALIZAR PANTALLA
# ==========================================

def capturar_y_analizar_pantalla():
    """Captura pantalla y la analiza con LLaVA"""
    print("\n Analizando pantalla...")
    
    try:
        import mss
        import mss.tools
        from PIL import Image
        
        print("\n Cambia a la ventana para tomar la captura")
        print("   Tomando en 3 segundos\n")
    
        for i in range(3, 0, -1):
            print(f"   {i}...")
            time.sleep(1)

        # Capturar
        sct = mss.mss()
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        temp_screen = "temp_pantalla_neo.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=temp_screen)
        
        # Optimizar imagen
        img = Image.open(temp_screen)
        if img.size[0] > 1280:
            ratio = 1280 / img.size[0]
            nuevo_size = (1280, int(img.size[1] * ratio))
            img = img.resize(nuevo_size, Image.Resampling.LANCZOS)
            img.save(temp_screen, optimize=True, quality=85)
        
        print(" Captura realizada")
        
        # Analizar con LLaVA - SINTAXIS CORREGIDA
        print(" Procesando con LLaVA (esto puede tomar 20-30 segundos)...")
        
        prompt = "Describe brevemente en español lo que ves en esta pantalla. Menciona qué aplicaciones están abiertas y qué contenido hay visible."
        
        # CORRECCIÓN: Usar la sintaxis correcta de Ollama para imágenes
        comando = [
            "ollama", "run", "llava:7b",
            prompt
        ]
        
        resultado = subprocess.run(
            comando,
            input=temp_screen,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        # Limpiar archivo temporal
        if os.path.exists(temp_screen):
            try:
                os.remove(temp_screen)
            except:
                pass
        
        if resultado.stdout and resultado.stdout.strip():
            descripcion = resultado.stdout.strip()
            
            # Limpiar respuesta de posibles errores o texto extra
            lineas = descripcion.split('\n')
            descripcion_limpia = []
            
            for linea in lineas:
                linea = linea.strip()
                # Filtrar líneas de error o vacías
                if linea and not linea.startswith('Error') and not linea.startswith('pulling'):
                    descripcion_limpia.append(linea)
            
            descripcion_final = ' '.join(descripcion_limpia)
            
            if descripcion_final:
                print(f" Análisis completado")
                print(f" Descripción: {descripcion_final}")
                return descripcion_final
            else:
                print(" LLaVA no generó respuesta válida")
                return None
        else:
            print(" LLaVA no generó respuesta")
            if resultado.stderr:
                print(f"   Error: {resultado.stderr[:200]}")
            return None
            
    except subprocess.TimeoutExpired:
        print(" Tiempo de espera agotado al analizar pantalla")
        if os.path.exists(temp_screen):
            try:
                os.remove(temp_screen)
            except:
                pass
        return None
    except Exception as e:
        print(f" Error al analizar pantalla: {e}")
        if os.path.exists(temp_screen):
            try:
                os.remove(temp_screen)
            except:
                pass
        return None

# ==========================================
# FUNCIONES DE CONTROL (básicas integradas)
# ==========================================

import pyautogui
pyautogui.PAUSE = 0.5

def abre(nombre):
    """Abre un programa por nombre"""
    print(f"   Abriendo {nombre}...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write(nombre, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_programa(nombre):
    """Abre un programa por nombre"""
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
    print(f"\n Analizando: '{comando}'")

    # Guardar en log
    if MEMORIA_DISPONIBLE:
        neo_memoria.guardar_log(f"Procesando comando: {comando}")

    # Detectar si necesita ver la pantalla
    palabras_visuales = ['esto', 'esta', 'eso', 'aquí', 'ahí', 'pantalla', 
                         'ventana', 'lo que ves', 'lo que hay', 'qué hay']
    
    necesita_vision = any(palabra in comando.lower() for palabra in palabras_visuales)
    
    contexto_pantalla = ""
    if necesita_vision:
        print(" Detecté que necesitas que vea la pantalla")
        contexto_pantalla = capturar_y_analizar_pantalla()
        
        if contexto_pantalla:
            print(f" Contexto visual obtenido")
    
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
    
    # COMANDOS DE MEMORIA (NUEVOS)
    if MEMORIA_DISPONIBLE:
        if 'repite' in comando_lower or 'hazlo de nuevo' in comando_lower:
            ultimo = neo_memoria.obtener_ultimo_comando()
            if ultimo and ultimo['exito']:
                print(f"💭 Repitiendo: '{ultimo['comando']}'")
                return procesar_comando(ultimo['comando'])
            else:
                return {
                    "acciones": [],
                    "explicacion": "No hay comando anterior para repetir",
                    "respuesta_directa": True
                }
        
        if 'qué hice' in comando_lower or 'historial' in comando_lower:
            neo_memoria.mostrar_historial(5)
            return {
                "acciones": [],
                "explicacion": "Mostrando historial",
                "respuesta_directa": True
            }
    

    
    # Si no es comando rápido, usar Llama
    print(" Consultando IA...")
    
    prompt = f"""Convierte este comando a JSON.

COMANDO: "{comando}"
"""
    
    # Agregar contexto de memoria
    if MEMORIA_DISPONIBLE:
        contexto_memoria = neo_memoria.obtener_contexto_memoria()
        if contexto_memoria:
            prompt += f"""

                        {contexto_memoria}
                        Usa este historial si es relevante para el comando actual.
                       """

    # Agregar contexto visual si existe
    if contexto_pantalla:
        prompt += f"""

CONTEXTO VISUAL (lo que ves en la pantalla):
{contexto_pantalla}

Usa esta información para tomar mejores decisiones.
"""
        
    prompt += f"""

{FUNCIONES_DISPONIBLES}

Formato JSON (solo JSON, nada más):
{{"acciones": [{{"funcion": "nombre", "args": []}}], "explicacion": "texto"}}

Ejemplos:
"abre Chrome"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}], "explicacion": "Abriendo el navegador Chrome."}}

"Quiero abrir Word"
{{"acciones": [{{"funcion": "abrir_programa", "args": ["word"]}}], "explicacion": "Ejecutando la apertura del programa Word."}}

"Sube el volumen un poco"
{{"acciones": [{{"funcion": "volumen_subir", "args": [2]}}], "explicacion": "Incrementando ligeramente el volumen del sistema."}}

"Busca el clima de mañana y luego minimiza"
{{"acciones": [{{"funcion": "buscar_en_google", "args": ["el clima de mañana"]}},{{"funcion": "esperar", "args": [3]}}, {{"funcion": "minimizar_todo", "args": []}}], "explicacion": "Buscaré el clima en Google y luego minimizaré todas las ventanas."}}

"Cierra esto"
{{"acciones": [{{"funcion": "cerrar_ventana", "args": []}}], "explicacion": "Cerrando la ventana o aplicación activa."}}

"Espera 5 segundos y abre la calculadora"
{{"acciones": [{{"funcion": "esperar", "args": [5]}}, {{"funcion": "abrir_calculadora", "args": []}}], "explicacion": "Esperando 5 segundos antes de abrir la calculadora."}}

"Abre mi explorador de archivos"
{{"acciones": [{{"funcion": "abrir_explorador", "args": []}}], "explicacion": "Abriendo el Explorador de Archivos."}}

"Abre el bloc de notas y escribe hola mundo"
{{"acciones": [{{"funcion": "abrir_notepad", "args": []}}, {{"funcion": "esperar", "args": [1]}}, {{"funcion": "escribir_texto", "args": ["Hola Mundo"]}}], "explicacion": "Abriendo el Bloc de Notas y escribiendo el mensaje 'Hola Mundo'."}}

"Baja el volumen un poco, espera 2 segundos y abre la calculadora"
{{"acciones": [{{"funcion": "volumen_bajar", "args": [3]}}, {{"funcion": "esperar", "args": [2]}}, {{"funcion": "abrir_calculadora", "args": []}}], "explicacion": "Bajando el volumen, esperando 2 segundos y abriendo la Calculadora."}}

"Quiero buscar un video gracioso en Chrome"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}, {{"funcion": "esperar", "args": [2]}}, {{"funcion": "buscar_en_google", "args": ["video gracioso"]}}], "explicacion": "Abriendo Chrome y buscando 'video gracioso'."}}

"Minimiza todo, luego abre Firefox"
{{"acciones": [{{"funcion": "minimizar_todo", "args": []}}, {{"funcion": "abrir_programa", "args": ["firefox"]}}], "explicacion": "Minimizando todas las ventanas y abriendo Firefox."}}

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
            print(f" Plan: {plan.get('explicacion', 'Sin explicación')}")
            return plan
        else:
            print(" No se pudo extraer plan válido")
        
    except Exception as e:
        print(f" Error en IA: {e}")
    
    return None

def ejecutar_plan(plan):
    """Ejecuta el plan de acciones"""
    if not plan or 'acciones' not in plan:
        return False
    
    acciones = plan['acciones']
    total = len(acciones)
    
    print(f"\n Ejecutando {total} acción(es):\n")
    
    for i, accion in enumerate(acciones, 1):
        funcion = accion.get('funcion', '')
        args = accion.get('args', [])
        
        print(f"[{i}/{total}]", end=' ')
        
        try:
            if funcion == 'abrir_chrome':
                abrir_chrome()
            elif funcion == 'abre':
                abre(args[0] if args else '')
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
                print(f" Función desconocida: {funcion}")
                continue
            
            print("  ")
            time.sleep(0.3)
            
        except Exception as e:
            print(f"   Error: {e}")
            return False
    
    print("\n Completado")
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
                    print(" Grabando...")
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
        print(f" Error en grabación: {e}")
        audio.terminate()
        return None

def transcribir_audio(archivo):
    """Transcribe audio a texto"""
    try:
        result = modelo_whisper.transcribe(archivo, language="es")
        return result['text'].strip()
    except Exception as e:
        print(f" Error en transcripción: {e}")
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
    print(" MODO TEXTO - Sin voz (para pruebas)")
    print("=" * 60)
    print("\nEscribe comandos directamente")
    print("   No necesitas decir 'NEO', solo el comando\n")
    
    while True:
        try:
            comando = input("\n Tu comando (o 'salir'): ").strip()
            
            if comando.lower() in ['salir', 'exit']:
                print(" ¡Hasta luego!")
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
                    print("\nComando completado")
                    if MEMORIA_DISPONIBLE:
                        neo_memoria.guardar_log(f"Comando exitoso: {comando}")
                else:
                    print("\nHubo un problema")
                    if MEMORIA_DISPONIBLE:
                        neo_memoria.guardar_log(f"Error al ejecutar: {comando}", "ERROR")
            else:
                print("No se pudo procesar el comando")
                if MEMORIA_DISPONIBLE:
                    neo_memoria.guardar_log(f"No se generó plan para: {comando}", "WARNING")
                
        except KeyboardInterrupt:
            print("\n\n Saliendo...")
            break
        except Exception as e:
            print(f" Error: {e}")

# ==========================================
# MODO VOZ (loop principal)
# ==========================================

def modo_voz():
    """Loop principal con voz"""
    print("\n" + "=" * 60)
    print(" NEO ESCUCHANDO - Modo Voz")
    print("=" * 60)
    print("\nDi 'NEO' seguido de tu comando")
    print("Ejemplo: 'NEO, abre Chrome'")
    print("Presiona Ctrl+C para salir\n")
    
    while True:
        try:
            print(" Esperando que hables...")
            
            # Escuchar
            archivo = escuchar_audio()
            
            if not archivo:
                continue
            
            # Transcribir
            texto = transcribir_audio(archivo)
            
            if not texto:
                continue
            
            print(f" Escuché: '{texto}'")
            
            # Detectar activación
            activado, comando = detectar_activacion(texto)
            
            if activado:
                if comando:
                    print(" NEO activado\n")
                    
                    # Procesar y ejecutar
                    plan = procesar_comando(comando)
                    
                    if plan:
                        exito = ejecutar_plan(plan)
                        
                        # Guardar en memoria
                        if MEMORIA_DISPONIBLE:
                            neo_memoria.guardar_comando(comando, plan, exito)
                    else:
                        print("No entendí el comando")
                        if MEMORIA_DISPONIBLE:
                            neo_memoria.guardar_log(f"Comando no entendido: {comando}", "WARNING")
                else:
                    print(" Dijiste 'NEO' pero sin comando")
            else:
                print(" No detecté 'NEO'\n")
            
            # Limpiar
            if os.path.exists(TEMP_AUDIO):
                os.remove(TEMP_AUDIO)
                
        except KeyboardInterrupt:
            print("\n\n Apagando NEO...")
            break
        except Exception as e:
            print(f" Error: {e}")
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
    print("3. Salir")
    
    modo = input("\n¿Qué modo? (1/2/3): ").strip()
    
    if modo == "1":
        print("\n Asegúrate de que tu micrófono funcione")
        input("Presiona Enter cuando estés listo...")
        modo_voz()
        
    elif modo == "2":
        modo_texto()
        
    else:
        print("\n ¡Hasta luego!")
    
    # Limpiar archivos temporales
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)
    
    print("\n NEO apagado correctamente")