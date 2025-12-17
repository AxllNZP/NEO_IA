# neo_control.py - Sistema de control de PC para NEO
import pyautogui
import subprocess
import time
import os
from datetime import datetime
from neo_memoria import actualizar_contexto

print("=" * 60)
print("NEO - Sistema de Control v1.0")
print("=" * 60)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def abrir_menu_inicio():
    print("Abriendo menú inicio...")
    pyautogui.press('win')
    time.sleep(0.5)

def buscar_y_abrir(programa):
    print(f" Buscando: {programa}")
    abrir_menu_inicio()
    time.sleep(0.5)
    pyautogui.write(programa, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    print(f"{programa} iniciado")

def abrir_chrome():
    buscar_y_abrir('chrome')
    actualizar_contexto('app', 'chrome')
    actualizar_contexto('accion', 'abrir_programa')

def abrir_notepad():
    buscar_y_abrir('notepad')
    actualizar_contexto('app', 'notepad')
    actualizar_contexto('accion', 'abrir_programa')

def abrir_calculadora():
    buscar_y_abrir('calc')
    actualizar_contexto('app', 'calculadora')
    actualizar_contexto('accion', 'abrir_programa')

def abrir_explorador_archivos():
    print("📁 Abriendo Explorador...")
    pyautogui.hotkey('win', 'e')
    time.sleep(0.5)
    print("Explorador abierto")

def abrir_configuracion():
    print(" Abriendo Configuración...")
    pyautogui.hotkey('win', 'i')
    time.sleep(0.5)
    print("Configuración abierta")

def abrir_cmd():
    print(" Abriendo CMD...")
    buscar_y_abrir('cmd')

def abrir_programa(nombre):
    print(f"Abriendo {nombre}...")
    buscar_y_abrir(nombre)
    actualizar_contexto('app', nombre)
    actualizar_contexto('accion', 'abrir_programa')

def buscar_en_google(query):
    print(f" Buscando en Google: {query}")
    abrir_chrome()
    time.sleep(2)
    pyautogui.write(query, interval=0.05)
    pyautogui.press('enter')
    print("Búsqueda completada")

    actualizar_contexto('busqueda', query)
    actualizar_contexto('url', f'google.com/search?q={query}')
    actualizar_contexto('accion', 'buscar_web')

def abrir_url(url):
    print(f" Abriendo: {url}")
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    abrir_chrome()
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)
    pyautogui.write(url, interval=0.05)
    pyautogui.press('enter')
    print(f"{url} abierto")
    actualizar_contexto('url', url)
    actualizar_contexto('accion', 'abrir_url')

def abrir_youtube(busqueda=""):
    if busqueda:
        print(f" Buscando en YouTube: {busqueda}")
        url = f"youtube.com/results?search_query={busqueda.replace(' ', '+')}"
    else:
        print(" Abriendo YouTube...")
        url = "youtube.com"
    
    abrir_url(url)

def minimizar_todo():
    print("  Minimizando todo...")
    pyautogui.hotkey('win', 'd')
    time.sleep(0.3)
    print("Escritorio visible")

def cerrar_ventana_actual():
    print("Cerrando ventana actual...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.3)
    print("Ventana cerrada")


def cambiar_ventana():
    print(" Cambiando de ventana...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)

def maximizar_ventana():
    print(" Maximizando ventana...")
    pyautogui.hotkey('win', 'up')
    time.sleep(0.3)
    print("Ventana maximizada")

def minimizar_ventana():
    print("Minimizando ventana...")
    pyautogui.hotkey('win', 'down')
    time.sleep(0.3)
    print("Ventana minimizada")

def ventana_izquierda():
    print("Ventana a la izquierda...")
    pyautogui.hotkey('win', 'left')
    time.sleep(0.3)

def ventana_derecha():
    print("Ventana a la derecha...")
    pyautogui.hotkey('win', 'right')
    time.sleep(0.3)

def escribir_texto(texto):
    print(f"Escribiendo: {texto[:50]}{'...' if len(texto) > 50 else ''}")
    time.sleep(0.5)
    pyautogui.write(texto, interval=0.05)
    print("Texto escrito")

def presionar_enter():
    pyautogui.press('enter')

def copiar():
    print("Copiando...")
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    print("Copiado")

def pegar():
    print("Pegando...")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    print("Pegado")

def deshacer():
    print("Deshaciendo...")
    pyautogui.hotkey('ctrl', 'z')
    time.sleep(0.2)

def guardar():
    print("Guardando...")
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.2)
    print("Guardado")

def seleccionar_todo():
    print("Seleccionando todo...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)

def abrir_carpeta(nombre_carpeta):
    carpetas = {
        "escritorio": os.path.join(os.path.expanduser("~"), "Desktop"),
        "descargas": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documentos": os.path.join(os.path.expanduser("~"), "Documents"),
        "imagenes": os.path.join(os.path.expanduser("~"), "Pictures"),
        "videos": os.path.join(os.path.expanduser("~"), "Videos"),
        "musica": os.path.join(os.path.expanduser("~"), "Music"),
    }
    
    nombre_lower = nombre_carpeta.lower()
    
    if nombre_lower in carpetas:
        ruta = carpetas[nombre_lower]
        print(f"Abriendo: {nombre_carpeta}")
        
        try:
            if os.path.exists(ruta):
                os.startfile(ruta)
                print(f"{nombre_carpeta} abierta")
            else:
                print(f"Carpeta no encontrada: {ruta}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f" {nombre_carpeta} no está en carpetas rápidas")

def crear_nota_rapida(texto):
    print(f"Creando nota rápida...")
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"nota_{timestamp}"
    filepath = os.path.join(desktop, f"{nombre}.txt")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(texto)
        print(f"Nota creada: {nombre}.txt")
        os.startfile(filepath)
        actualizar_contexto('archivo', filepath)
        actualizar_contexto('accion', 'crear_archivo')
    except Exception as e:
        print(f"Error: {e}")

def volumen_subir(veces=1):
    print(f" Subiendo volumen ({veces}x)...")
    for _ in range(veces):
        pyautogui.press('volumeup')
        time.sleep(0.1)
    print("Volumen subido")
    actualizar_contexto('volumen', veces)
    actualizar_contexto('accion', 'volumen_subir')

def volumen_bajar(veces=1):
    print(f"Bajando volumen ({veces}x)...")
    for _ in range(veces):
        pyautogui.press('volumedown')
        time.sleep(0.1)
    print("Volumen bajado")
    actualizar_contexto('volumen', -veces)
    actualizar_contexto('accion', 'volumen_bajar')

def volumen_silenciar():
    print("Alternando silencio...")
    pyautogui.press('volumemute')
    time.sleep(0.2)
    print("Silencio alternado")

def tomar_captura():
    print("Abriendo herramienta de captura...")
    pyautogui.hotkey('win', 'shift', 's')
    time.sleep(0.5)
    print("Herramienta lista (selecciona área)")

def esperar(segundos):
    if segundos >= 1:
        print(f"Esperando {segundos}s...")
    time.sleep(segundos)

if __name__ == "__main__":
    print("\nSistema de control cargado")
    print("\nEste módulo contiene todas las funciones de control de PC")
    print("Impórta lo desde otro script: from neo_control import *\n")