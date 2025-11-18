# cerebro_ejecutor.py - Cerebro que ejecuta planes
import subprocess
import json
import re
import pyautogui
import time

print("=" * 60)
print("CEREBRO PERO QUE EJECUTA - Genera y ejecuta")
print("=" * 60)

# Configuración PyAutoGUI
pyautogui.PAUSE = 0.5

# ==========================================
# FUNCIONES DE CONTROL (Simples)
# ==========================================

def abrir_vscode():
    print("Abriendo VSCode...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('vscode', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_chrome():
    print("Abriendo Chrome...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('chrome', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_notepad():
    print("Abriendo Notepad...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('notepad', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_calculadora():
    print("Abriendo Calculadora...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('calc', interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def abrir_explorador():
    print("Abriendo Explorador...")
    pyautogui.hotkey('win', 'e')

def minimizar_todo():
    print("Minimizando todo...")
    pyautogui.hotkey('win', 'd')

def cerrar_ventana():
    print("Cerrando ventana...")
    pyautogui.hotkey('alt', 'f4')

def escribir_texto(texto):
    print(f"Escribiendo: {texto}")
    time.sleep(1)
    pyautogui.write(texto, interval=0.05)

def volumen_subir(veces):
    print(f"Subiendo volumen {veces}x...")
    for _ in range(veces):
        pyautogui.press('volumeup')
        time.sleep(0.1)

def volumen_bajar(veces):
    print(f"Bajando volumen {veces}x...")
    for _ in range(veces):
        pyautogui.press('volumedown')
        time.sleep(0.1)

def esperar(segundos):
    print(f"Esperando {segundos}s...")
    time.sleep(segundos)

# ==========================================
# FUNCIONES DEL CEREBRO
# ==========================================

FUNCIONES_DISPONIBLES = """
PROGRAMAS:
- abrir_chrome()
- abrir_notepad()
- abrir_calculadora()
- abrir_explorador()
- abrir_vscode()

ACCIONES:
- minimizar_todo()
- cerrar_ventana()
- escribir_texto('texto')

VOLUMEN:
- volumen_subir(veces)
- volumen_bajar(veces)

SISTEMA:
- esperar(segundos)
"""

def procesar_comando(comando):
    """Genera plan de acción"""
    print(f"\nAnalizando: '{comando}'")
    print("Pensando...\n")
    
    prompt = f"""Convierte este comando en JSON.

COMANDO: "{comando}"

{FUNCIONES_DISPONIBLES}

Responde SOLO con JSON en este formato:
{{
  "acciones": [{{"funcion": "nombre", "args": []}}],
  "explicacion": "texto"
}}

EJEMPLOS:

"abre chrome"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}], "explicacion": "Abriendo Chrome"}}

"minimiza todo y abre calculadora"
{{"acciones": [{{"funcion": "minimizar_todo", "args": []}}, {{"funcion": "esperar", "args": [1]}}, {{"funcion": "abrir_calculadora", "args": []}}], "explicacion": "Minimizando y abriendo calculadora"}}

"sube volumen 5 veces"
{{"acciones": [{{"funcion": "volumen_subir", "args": [5]}}], "explicacion": "Subiendo volumen 5 veces"}}

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
        
        respuesta = resultado.stdout.strip()
        plan = extraer_json(respuesta)
        
        if plan:
            print(f"Plan: {plan.get('explicacion', 'N/A')}")
            print(f"{len(plan.get('acciones', []))} acciones\n")
            return plan
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def extraer_json(texto):
    """Extrae JSON de la respuesta"""
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

def ejecutar_plan(plan):
    """Ejecuta el plan de acciones"""
    if not plan or 'acciones' not in plan:
        return False
    
    acciones = plan['acciones']
    total = len(acciones)
    
    print(f"Ejecutando {total} acciones:\n")
    
    for i, accion in enumerate(acciones, 1):
        funcion = accion.get('funcion', '')
        args = accion.get('args', [])
        
        print(f"[{i}/{total}]", end=' ')
        
        try:
            # Ejecutar la función
            if funcion == 'abrir_chrome':
                abrir_chrome()
            elif funcion == 'abrir_notepad':
                abrir_notepad()
            elif funcion == 'abrir_calculadora':
                abrir_calculadora()
            elif funcion == 'abrir_explorador':
                abrir_explorador()
            elif funcion == 'abrir_vscode':
                abrir_vscode()
            elif funcion == 'minimizar_todo':
                minimizar_todo()
            elif funcion == 'cerrar_ventana':
                cerrar_ventana()
            elif funcion == 'escribir_texto':
                escribir_texto(args[0] if args else '')
            elif funcion == 'volumen_subir':
                volumen_subir(args[0] if args else 3)
            elif funcion == 'volumen_bajar':
                volumen_bajar(args[0] if args else 3)
            elif funcion == 'esperar':
                esperar(args[0] if args else 1)
            else:
                print(f"Función desconocida: {funcion}")
                continue
            
            print("    ✓")
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    print("\nPlan ejecutado completamente")
    return True

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\nEste programa genera Y ejecuta planes")
    print("Las acciones se ejecutarán en tu PC\n")
    
    while True:
        print("-" * 60)
        comando = input("\nTu comando (o 'salir'): ").strip()
        
        if comando.lower() in ['salir', 'exit']:
            print("¡Hasta luego!")
            break
        
        if not comando:
            continue
        
        # Generar plan
        plan = procesar_comando(comando)
        
        if plan:
            # Mostrar plan
            print("\nPlan generado:")
            print(json.dumps(plan, indent=2, ensure_ascii=False))
            
            # Confirmar ejecución
            print("\n¿Ejecutar este plan? (si/no): ", end='')
            confirmar = input().strip().lower()
            
            if confirmar == 'si':
                ejecutar_plan(plan)
            else:
                print("Ejecución cancelada")
        else:
            print("No se pudo generar plan")