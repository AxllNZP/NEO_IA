# NEO_control.py - Sistema de Control Completo para NEO
# Versión 1.0 - Con todas las funciones

import pyautogui
import subprocess
import time
import os
from datetime import datetime

print("=" * 60)
print("NEO - Sistema de Control Completo v1.0")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD
# ==========================================

# Si mueves el mouse a la esquina superior izquierda, todo se detiene
pyautogui.FAILSAFE = True

# Pausa entre acciones (segundos)
pyautogui.PAUSE = 0.5

# ==========================================
# CONFIGURACIÓN PERSONALIZADA
# ==========================================

# TUS RUTAS PERSONALIZADAS (Edita estas según tus programas)
RUTAS_PROGRAMAS = {
    # Navegadores
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    
    # Editores
    "vscode": r"C:\Users\AXELL\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad++": r"C:\Program Files\Notepad++\notepad++.exe",
    
    # Comunicación
    "discord": r"C:\Users\AXELL\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "whatsapp": r"C:\Users\AXELL\AppData\Local\WhatsApp\WhatsApp.exe",
    "telegram": r"C:\Users\AXELL\AppData\Roaming\Telegram Desktop\Telegram.exe",
    
    # Entretenimiento
    "spotify": r"C:\Users\AXELL\AppData\Roaming\Spotify\Spotify.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    
    # Herramientas
    "obs": r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
}

# CARPETAS FRECUENTES (Edita según tus carpetas)
CARPETAS_RAPIDAS = {
    "escritorio": os.path.join(os.path.expanduser("~"), "Desktop"),
    "descargas": os.path.join(os.path.expanduser("~"), "Downloads"),
    "documentos": os.path.join(os.path.expanduser("~"), "Documents"),
    "imagenes": os.path.join(os.path.expanduser("~"), "Pictures"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
    "musica": os.path.join(os.path.expanduser("~"), "Music"),
}

# ==========================================
# FUNCIONES BÁSICAS - MENÚ INICIO Y BÚSQUEDA
# ==========================================

def abrir_menu_inicio():
    """Abre el menú inicio de Windows"""
    print("🪟 Abriendo menú inicio...")
    pyautogui.press('win')
    time.sleep(0.5)

def buscar_y_abrir(programa):
    """
    Busca un programa en el menú inicio y lo abre
    
    Args:
        programa (str): Nombre del programa a buscar
    
    Ejemplo:
        buscar_y_abrir('chrome')
        buscar_y_abrir('notepad')
    """
    print(f"🔍 Buscando: {programa}")
    abrir_menu_inicio()
    time.sleep(0.5)
    pyautogui.write(programa, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    print(f"✓ {programa} iniciado")

# ==========================================
# FUNCIONES - PROGRAMAS ESPECÍFICOS
# ==========================================

def abrir_chrome():
    """Abre Google Chrome"""
    print("🌐 Abriendo Chrome...")
    if os.path.exists(RUTAS_PROGRAMAS.get("chrome", "")):
        subprocess.Popen(RUTAS_PROGRAMAS["chrome"])
        print("✓ Chrome abierto")
    else:
        buscar_y_abrir('chrome')

def abrir_notepad():
    """Abre el Bloc de notas"""
    print("📝 Abriendo Notepad...")
    buscar_y_abrir('notepad')

def abrir_calculadora():
    """Abre la Calculadora"""
    print("🔢 Abriendo Calculadora...")
    buscar_y_abrir('calc')

def abrir_explorador_archivos():
    """Abre el Explorador de archivos"""
    print("📁 Abriendo Explorador...")
    pyautogui.hotkey('win', 'e')
    time.sleep(0.5)
    print("✓ Explorador abierto")

def abrir_configuracion():
    """Abre la Configuración de Windows"""
    print("⚙️ Abriendo Configuración...")
    pyautogui.hotkey('win', 'i')
    time.sleep(0.5)
    print("✓ Configuración abierta")

def abrir_cmd():
    """Abre el símbolo del sistema (CMD)"""
    print("💻 Abriendo CMD...")
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write('cmd', interval=0.05)
    pyautogui.press('enter')
    print("✓ CMD abierto")

def abrir_powershell():
    """Abre PowerShell"""
    print("💻 Abriendo PowerShell...")
    pyautogui.hotkey('win', 'x')
    time.sleep(0.3)
    pyautogui.press('i')
    print("✓ PowerShell abierto")

def abrir_administrador_tareas():
    """Abre el Administrador de tareas"""
    print("📊 Abriendo Administrador de tareas...")
    pyautogui.hotkey('ctrl', 'shift', 'esc')
    print("✓ Administrador de tareas abierto")

# ==========================================
# FUNCIONES - PROGRAMAS PERSONALIZADOS
# ==========================================

def abrir_programa(nombre):
    """
    Abre un programa de la lista personalizada
    
    Args:
        nombre (str): Nombre clave del programa
    
    Ejemplo:
        abrir_programa('discord')
        abrir_programa('spotify')
    """
    nombre_lower = nombre.lower()
    
    if nombre_lower in RUTAS_PROGRAMAS:
        ruta = RUTAS_PROGRAMAS[nombre_lower]
        print(f"🚀 Abriendo {nombre}...")
        
        try:
            if os.path.exists(ruta.split()[0]):  # Verifica la ruta base
                subprocess.Popen(ruta, shell=True)
                print(f"✓ {nombre} abierto")
            else:
                print(f"⚠️  Ruta no encontrada. Buscando por nombre...")
                buscar_y_abrir(nombre)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Intentando búsqueda alternativa...")
            buscar_y_abrir(nombre)
    else:
        print(f"⚠️  {nombre} no está en la lista. Buscando...")
        buscar_y_abrir(nombre)

# ==========================================
# FUNCIONES - NAVEGACIÓN WEB
# ==========================================

def buscar_en_google(query):
    """
    Abre Chrome y busca en Google
    
    Args:
        query (str): Término de búsqueda
    
    Ejemplo:
        buscar_en_google('Python tutorial')
        buscar_en_google('clima Lima')
    """
    print(f"🔍 Buscando en Google: {query}")
    abrir_chrome()
    time.sleep(2)
    pyautogui.write(query, interval=0.05)
    pyautogui.press('enter')
    print("✓ Búsqueda completada")

def abrir_url(url):
    """
    Abre una URL específica en Chrome
    
    Args:
        url (str): URL a abrir
    
    Ejemplo:
        abrir_url('youtube.com')
        abrir_url('github.com')
    """
    print(f"🌐 Abriendo: {url}")
    
    # Asegurar que tenga https://
    if not url.startswith('http'):
        url = 'https://' + url
    
    abrir_chrome()
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')  # Seleccionar barra de direcciones
    time.sleep(0.3)
    pyautogui.write(url, interval=0.05)
    pyautogui.press('enter')
    print(f"✓ {url} abierto")

def abrir_youtube(busqueda=""):
    """
    Abre YouTube, opcionalmente con búsqueda
    
    Args:
        busqueda (str, opcional): Término a buscar en YouTube
    
    Ejemplo:
        abrir_youtube()  # Solo abre YouTube
        abrir_youtube('Python tutorial')  # Busca en YouTube
    """
    if busqueda:
        print(f"📺 Buscando en YouTube: {busqueda}")
        url = f"youtube.com/results?search_query={busqueda.replace(' ', '+')}"
    else:
        print("📺 Abriendo YouTube...")
        url = "youtube.com"
    
    abrir_url(url)

# ==========================================
# FUNCIONES - CONTROL DE VENTANAS
# ==========================================

def minimizar_todo():
    """Minimiza todas las ventanas (muestra escritorio)"""
    print("🖥️ Minimizando todo...")
    pyautogui.hotkey('win', 'd')
    time.sleep(0.3)
    print("✓ Escritorio visible")

def cerrar_ventana_actual():
    """Cierra la ventana activa"""
    print("❌ Cerrando ventana actual...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.3)
    print("✓ Ventana cerrada")

def cambiar_ventana():
    """Cambia a la siguiente ventana abierta (Alt+Tab)"""
    print("🔄 Cambiando de ventana...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)

def maximizar_ventana():
    """Maximiza la ventana actual"""
    print("⬆️ Maximizando ventana...")
    pyautogui.hotkey('win', 'up')
    time.sleep(0.3)
    print("✓ Ventana maximizada")

def minimizar_ventana():
    """Minimiza la ventana actual"""
    print("⬇️ Minimizando ventana...")
    pyautogui.hotkey('win', 'down')
    time.sleep(0.3)
    print("✓ Ventana minimizada")

def ventana_izquierda():
    """Ancla la ventana a la izquierda de la pantalla"""
    print("⬅️ Ventana a la izquierda...")
    pyautogui.hotkey('win', 'left')
    time.sleep(0.3)

def ventana_derecha():
    """Ancla la ventana a la derecha de la pantalla"""
    print("➡️ Ventana a la derecha...")
    pyautogui.hotkey('win', 'right')
    time.sleep(0.3)

# ==========================================
# FUNCIONES - TECLADO Y ESCRITURA
# ==========================================

def escribir_texto(texto):
    """
    Escribe texto en la ventana activa
    
    Args:
        texto (str): El texto a escribir
    
    Ejemplo:
        escribir_texto('Hola mundo')
    """
    print(f"⌨️ Escribiendo: {texto[:50]}{'...' if len(texto) > 50 else ''}")
    time.sleep(0.5)
    pyautogui.write(texto, interval=0.05)
    print("✓ Texto escrito")

def presionar_enter():
    """Presiona Enter"""
    pyautogui.press('enter')

def copiar():
    """Ejecuta Ctrl+C (copiar)"""
    print("📋 Copiando...")
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    print("✓ Copiado")

def pegar():
    """Ejecuta Ctrl+V (pegar)"""
    print("📋 Pegando...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    print("✓ Pegado")

def deshacer():
    """Ejecuta Ctrl+Z (deshacer)"""
    print("↩️ Deshaciendo...")
    pyautogui.hotkey('ctrl', 'z')
    time.sleep(0.2)

def guardar():
    """Ejecuta Ctrl+S (guardar)"""
    print("💾 Guardando...")
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.2)
    print("✓ Guardado")

def seleccionar_todo():
    """Ejecuta Ctrl+A (seleccionar todo)"""
    print("📝 Seleccionando todo...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)

# ==========================================
# FUNCIONES - ARCHIVOS Y CARPETAS
# ==========================================

def abrir_archivo(ruta_archivo):

    print(f"📄 Abriendo: {os.path.basename(ruta_archivo)}")
    
    try:
        if os.path.exists(ruta_archivo):
            os.startfile(ruta_archivo)
            print("✓ Archivo abierto")
        else:
            print(f"❌ Archivo no encontrado: {ruta_archivo}")
    except Exception as e:
        print(f"❌ Error: {e}")

def abrir_carpeta(nombre_carpeta):
    """
    Abre una carpeta de la lista rápida
    
    Args:
        nombre_carpeta (str): Nombre clave de la carpeta
    
    Ejemplo:
        abrir_carpeta('escritorio')
        abrir_carpeta('descargas')
    """
    nombre_lower = nombre_carpeta.lower()
    
    if nombre_lower in CARPETAS_RAPIDAS:
        ruta = CARPETAS_RAPIDAS[nombre_lower]
        print(f"📁 Abriendo: {nombre_carpeta}")
        
        try:
            if os.path.exists(ruta):
                os.startfile(ruta)
                print(f"✓ {nombre_carpeta} abierta")
            else:
                print(f"❌ Carpeta no encontrada: {ruta}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"⚠️  {nombre_carpeta} no está en carpetas rápidas")

def crear_archivo_texto(nombre, contenido=""):
    """
    Crea un archivo de texto en el escritorio
    
    Args:
        nombre (str): Nombre del archivo (sin extensión)
        contenido (str): Contenido del archivo
    
    Ejemplo:
        crear_archivo_texto('nota', 'Este es el contenido')
    """
    print(f"📝 Creando archivo: {nombre}.txt")
    
    desktop = CARPETAS_RAPIDAS["escritorio"]
    filepath = os.path.join(desktop, f"{nombre}.txt")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"✓ Archivo creado: {nombre}.txt")
        return filepath
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def crear_nota_rapida(texto):
    """
    Crea una nota rápida con timestamp en el escritorio
    
    Args:
        texto (str): Contenido de la nota
    
    Ejemplo:
        crear_nota_rapida('Recordar comprar leche')
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"nota_{timestamp}"
    filepath = crear_archivo_texto(nombre, texto)
    
    if filepath:
        abrir_archivo(filepath)

# ==========================================
# FUNCIONES - MULTIMEDIA Y SISTEMA
# ==========================================

def volumen_subir(veces=1):
    """
    Sube el volumen
    
    Args:
        veces (int): Número de veces a subir
    
    Ejemplo:
        volumen_subir()      # Sube 1 vez
        volumen_subir(5)     # Sube 5 veces
    """
    print(f"🔊 Subiendo volumen ({veces}x)...")
    for _ in range(veces):
        pyautogui.press('volumeup')
        time.sleep(0.1)
    print("✓ Volumen subido")

def volumen_bajar(veces=1):
    """
    Baja el volumen
    
    Args:
        veces (int): Número de veces a bajar
    
    Ejemplo:
        volumen_bajar()      # Baja 1 vez
        volumen_bajar(5)     # Baja 5 veces
    """
    print(f"🔉 Bajando volumen ({veces}x)...")
    for _ in range(veces):
        pyautogui.press('volumedown')
        time.sleep(0.1)
    print("✓ Volumen bajado")

def volumen_silenciar():
    """Silencia o activa el volumen"""
    print("🔇 Alternando silencio...")
    pyautogui.press('volumemute')
    time.sleep(0.2)
    print("✓ Silencio alternado")

def tomar_captura():
    """Abre la herramienta de captura de Windows"""
    print("📸 Abriendo herramienta de captura...")
    pyautogui.hotkey('win', 'shift', 's')
    time.sleep(0.5)
    print("✓ Herramienta lista (selecciona área)")

def bloquear_pc():
    """Bloquea la PC"""
    print("🔒 Bloqueando PC...")
    pyautogui.hotkey('win', 'l')
    print("✓ PC bloqueada")

def apagar_monitor():
    """Apaga el monitor (pantalla en negro)"""
    print("🖥️ Apagando monitor...")
    # Esto simula presionar el botón de apagado de monitor
    # No apaga la PC, solo la pantalla
    import ctypes
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

# ==========================================
# FUNCIONES - UTILIDADES
# ==========================================

def esperar(segundos):
    """
    Espera un número de segundos
    
    Args:
        segundos (int/float): Tiempo a esperar
    
    Ejemplo:
        esperar(3)    # Espera 3 segundos
        esperar(0.5)  # Espera medio segundo
    """
    print(f"⏳ Esperando {segundos} segundos...")
    time.sleep(segundos)
    print("✓ Espera completada")

def obtener_posicion_mouse():
    """Obtiene y muestra la posición actual del mouse"""
    x, y = pyautogui.position()
    print(f"🖱️ Posición del mouse: X={x}, Y={y}")
    return x, y

def mover_mouse(x, y, duracion=1):
    """
    Mueve el mouse a una posición específica
    
    Args:
        x (int): Coordenada X
        y (int): Coordenada Y
        duracion (float): Tiempo del movimiento en segundos
    
    Ejemplo:
        mover_mouse(960, 540)  # Centro de pantalla 1920x1080
    """
    print(f"🖱️ Moviendo mouse a ({x}, {y})...")
    pyautogui.moveTo(x, y, duration=duracion)
    print("✓ Mouse movido")

def click_en(x, y):
    """
    Hace click en coordenadas específicas
    
    Args:
        x (int): Coordenada X
        y (int): Coordenada Y
    
    Ejemplo:
        click_en(100, 200)
    """
    print(f"🖱️ Click en ({x}, {y})...")
    pyautogui.click(x, y)
    time.sleep(0.2)
    print("✓ Click realizado")

# ==========================================
# MENÚ INTERACTIVO
# ==========================================

def mostrar_menu():
    """Muestra el menú de comandos disponibles"""
    print("\n" + "=" * 60)
    print("COMANDOS DISPONIBLES")
    print("=" * 60)
    
    print("\n📱 PROGRAMAS:")
    print("  1.  Abrir Chrome")
    print("  2.  Abrir Notepad")
    print("  3.  Abrir Calculadora")
    print("  4.  Abrir Explorador de archivos")
    print("  5.  Abrir programa personalizado")
    
    print("\n🌐 WEB:")
    print("  6.  Buscar en Google")
    print("  7.  Abrir URL")
    print("  8.  Abrir YouTube")
    
    print("\n🪟 VENTANAS:")
    print("  9.  Minimizar todo")
    print("  10. Cerrar ventana actual")
    print("  11. Cambiar ventana")
    print("  12. Maximizar ventana")
    
    print("\n⌨️ ESCRITURA:")
    print("  13. Escribir texto")
    print("  14. Crear nota rápida")
    print("  15. Copiar")
    print("  16. Pegar")
    
    print("\n📁 ARCHIVOS:")
    print("  17. Abrir carpeta rápida")
    print("  18. Abrir archivo")
    
    print("\n🔊 MULTIMEDIA:")
    print("  19. Subir volumen")
    print("  20. Bajar volumen")
    print("  21. Silenciar")
    print("  22. Tomar captura")
    
    print("\n🔧 SISTEMA:")
    print("  23. Bloquear PC")
    print("  24. Administrador de tareas")
    print("  25. Obtener posición del mouse")
    
    print("\n  0.  Salir")
    print("=" * 60)




# ==========================================
# FUNCIONES PERSONALIZADAS 
# ==========================================

def abrir_hollow_knight():
    """
    Prepara la PC para jugar Hollow Knight
    
    Pasos:
    1. Minimiza todas las ventanas
    2. Ajusta volumen para gaming
    3. Inicia el juego desde Steam
    
    Ejemplo:
        abrir_hollow_knight()
    """
    print("🎮 Preparando Hollow Knight...")
    
    # Paso 1: Limpiar espacio
    print("\n  [1/3] Limpiando pantalla...")
    minimizar_todo()
    esperar(1)
    
    # Paso 2: Configurar audio
    print("  [2/3] Configurando audio...")
    volumen_silenciar()
    esperar(0.5)
    volumen_subir(8)
    esperar(0.5)
    
    # Paso 3: Iniciar juego
    print("  [3/3] Iniciando Hollow Knight...")
    
    buscar_y_abrir('hollow knight')
    
    # Alternativa si lo anterior no funciona:
    # buscar_y_abrir('hollow knight')
    
    esperar(2)
    
    print("\n✅ Hollow Knight iniciando")
    print("🎮 ¡Disfruta explorando Hallownest!")

# Alias corto
def abrir_hk():
    """Alias corto para abrir Hollow Knight"""
    abrir_hollow_knight()

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n✓ Sistema cargado correctamente")
    print("💡 Tip: Mueve el mouse a la esquina superior izquierda para detener cualquier acción")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n🎯 Elige una opción (0-25): ").strip()
            print()  # Línea en blanco
            
            if opcion == "1":
                abrir_chrome()
                
            elif opcion == "2":
                abrir_notepad()
                
            elif opcion == "3":
                abrir_calculadora()
                
            elif opcion == "4":
                abrir_explorador_archivos()
                
            elif opcion == "5":
                programa = input("¿Qué programa? (discord/spotify/vscode/etc): ")
                abrir_programa(programa)
                
            elif opcion == "6":
                query = input("¿Qué buscar?: ")
                buscar_en_google(query)
                
            elif opcion == "7":
                url = input("URL (sin https://): ")
                abrir_url(url)
                
            elif opcion == "8":
                busqueda = input("¿Buscar algo? (Enter para solo abrir): ")
                abrir_youtube(busqueda)
                
            elif opcion == "9":
                minimizar_todo()
                
            elif opcion == "10":
                cerrar_ventana_actual()
                
            elif opcion == "11":
                cambiar_ventana()
                
            elif opcion == "12":
                maximizar_ventana()
                
            elif opcion == "13":
                texto = input("Texto a escribir: ")
                print("⏳ Tienes 3 segundos para cambiar a la ventana destino...")
                time.sleep(3)
                escribir_texto(texto)
                
            elif opcion == "14":
                contenido = input("Contenido de la nota: ")
                crear_nota_rapida(contenido)
                
            elif opcion == "15":
                copiar()
                
            elif opcion == "16":
                pegar()
                
            elif opcion == "17":
                print("\nCarpetas disponibles:")
                for nombre in CARPETAS_RAPIDAS.keys():
                    print(f"  - {nombre}")
                carpeta = input("\n¿Cuál abrir?: ")
                abrir_carpeta(carpeta)
                
            elif opcion == "18":
                ruta = input("Ruta completa del archivo: ")
                abrir_archivo(ruta)
                
            elif opcion == "19":
                veces = input("¿Cuántas veces subir? (Enter = 1): ")
                veces = int(veces) if veces else 1
                volumen_subir(veces)
                
            elif opcion == "20":
                veces = input("¿Cuántas veces bajar? (Enter = 1): ")
                veces = int(veces) if veces else 1
                volumen_bajar(veces)
                
            elif opcion == "21":
                volumen_silenciar()
                
            elif opcion == "22":
                tomar_captura()
                
            elif opcion == "23":
                confirm = input("⚠️  ¿Seguro que quieres bloquear? (si/no): ")
                if confirm.lower() == "si":
                    bloquear_pc()
                    break  # Salir porque la PC se bloqueará
                
            elif opcion == "24":
                abrir_administrador_tareas()
                
            elif opcion == "25":
                obtener_posicion_mouse()
                
            elif opcion == "0":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("⚠️  Opción no válida")
            
            # Pequeña pausa antes de mostrar el menú de nuevo
            time.sleep(1.5)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrumpido")
            print("👋 ¡Hasta luego!")
            break
            
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("💡 Continuando...")
            time.sleep(1)

print("\n✓ Programa terminado")