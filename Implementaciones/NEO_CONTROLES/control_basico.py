import pyautogui
import time
import os

print("=" * 60)
print("CONTROLES DE PC")
print("=" * 60)

# Configuración de seguridad
pyautogui.PAUSE = 0.5  # Pausa entre acciones
pyautogui.FAILSAFE = True  # Para que el mouse se coloque en la esquina superior izquierda y detenga el script

def abrir_menu_inicio():
    """Abre el menú inicio"""
    print("Abriendo menú inicio...")
    pyautogui.press('win')
    time.sleep(0.5)
    print("Menú abierto")

def buscar_programa(nombre):
    """Busca un programa en Windows"""
    print(f"Buscando: {nombre}")
    abrir_menu_inicio()
    time.sleep(0.5)
    pyautogui.write(nombre, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    print(f"{nombre} iniciado")

def abrir_chrome():
    """Abre Google Chrome"""
    buscar_programa('chrome')

def abrir_notepad():
    """Abre Notepad"""
    buscar_programa('notepad')

def abrir_calculadora():
    """Abre Calculadora"""
    buscar_programa('calc')

def escribir_texto(texto):
    """Escribe texto en la ventana activa"""
    print(f"Escribiendo: {texto}")
    time.sleep(1)  # Tiempo para cambiar de ventana
    pyautogui.write(texto, interval=0.05)
    print("Texto escrito")

def minimizar_todo():
    """Muestra el escritorio"""
    print("Minimizando todo...")
    pyautogui.hotkey('win', 'd')
    time.sleep(0.3)
    print("Escritorio visible")

def cerrar_ventana():
    """Cierra ventana actual"""
    print("Cerrando ventana...")
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.3)
    print("Ventana cerrada")

def volumen_subir(veces=1):
    """Sube el volumen"""
    print(f"Subiendo volumen (x{veces})...")
    for _ in range(veces):
        pyautogui.press('volumeup')
        time.sleep(0.1)
    print("Volumen subido")

def volumen_bajar(veces=1):
    """Baja el volumen"""
    print(f"Bajando volumen (x{veces})...")
    for _ in range(veces):
        pyautogui.press('volumedown')
        time.sleep(0.1)
    print("Volumen bajado")

def captura_pantalla():
    """Toma captura de pantalla"""
    print("Tomando captura...")
    pyautogui.hotkey('win', 'shift', 's')
    time.sleep(0.5)
    print("Herramienta de captura abierta")

def abrir_explorador():
    """Abre el Explorador de archivos"""
    print("Abriendo Explorador...")
    pyautogui.hotkey('win', 'e')
    time.sleep(0.5)
    print("Explorador abierto")

# ==========================================
# MENÚ INTERACTIVO
# ==========================================

def mostrar_menu():
    """Muestra opciones disponibles"""
    print("\n" + "=" * 60)
    print("COMANDOS DISPONIBLES")
    print("=" * 60)
    print("\nPROGRAMAS:")
    print("  1. Abrir Chrome")
    print("  2. Abrir Notepad")
    print("  3. Abrir Calculadora")
    print("  4. Abrir Explorador")
    
    print("\nACCIONES:")
    print("  5. Escribir texto")
    print("  6. Minimizar todo")
    print("  7. Cerrar ventana actual")
    
    print("\nVOLUMEN:")
    print("  8. Subir volumen")
    print("  9. Bajar volumen")
    
    print("\nOTROS:")
    print("  10. Tomar captura")
    
    print("\n  0. Salir")
    print("=" * 60)


print("\nSi algo sale mal, mueve el mouse a la esquina superior izquierda")
print("   para detener todo (FAILSAFE activado)\n")

while True:
    mostrar_menu()
    
    try:
        opcion = input("\nElige opción (0-10): ").strip()
        print()  # Línea en blanco
        
        if opcion == "1":
            abrir_chrome()
            
        elif opcion == "2":
            abrir_notepad()
            
        elif opcion == "3":
            abrir_calculadora()
            
        elif opcion == "4":
            abrir_explorador()
            
        elif opcion == "5":
            texto = input("¿Qué escribir?: ")
            print("Tienes 3 segundos para cambiar a la ventana destino...")
            time.sleep(3)
            escribir_texto(texto)
            
        elif opcion == "6":
            minimizar_todo()
            
        elif opcion == "7":
            cerrar_ventana()
            
        elif opcion == "8":
            veces = input("¿Cuántas veces? (Enter = 3): ").strip()
            veces = int(veces) if veces else 3
            volumen_subir(veces)
            
        elif opcion == "9":
            veces = input("¿Cuántas veces? (Enter = 3): ").strip()
            veces = int(veces) if veces else 3
            volumen_bajar(veces)
            
        elif opcion == "10":
            captura_pantalla()
            
        elif opcion == "0":
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción inválida")
        
        time.sleep(1)  # Pausa antes de mostrar menú otra vez
        
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido")
        break
    except Exception as e:
        print(f"Error: {e}")

print("\nPrograma terminado")
print("\nDIA 2.5.")