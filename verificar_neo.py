# verificar_neo.py - Script de Verificación del Proyecto NEO
"""
Este script verifica que todo esté listo para ejecutar NEO
"""

import sys
import subprocess

print("=" * 70)
print("🔍 VERIFICACIÓN DEL PROYECTO NEO")
print("=" * 70)

# Lista de dependencias necesarias
DEPENDENCIAS = {
    'pyautogui': 'Control del PC',
    'whisper': 'Reconocimiento de voz',
    'pyaudio': 'Captura de audio',
    'numpy': 'Procesamiento de datos',
    'pyttsx3': 'Síntesis de voz (TTS)',
    'customtkinter': 'Interfaz gráfica',
    'mss': 'Captura de pantalla',
    'PIL': 'Procesamiento de imágenes',
}

DEPENDENCIAS_OPCIONALES = {
    'ollama': 'Modelo de IA local (Llama)',
}

def verificar_python():
    """Verifica la versión de Python"""
    print("\n📌 PASO 1: Verificando Python...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("   ✅ Versión correcta (3.8+)")
        return True
    else:
        print("   ❌ Necesitas Python 3.8 o superior")
        return False

def verificar_modulo(nombre, descripcion):
    """Verifica si un módulo está instalado"""
    try:
        if nombre == 'PIL':
            __import__('PIL')
        elif nombre == 'whisper':
            __import__('whisper')
        else:
            __import__(nombre)
        print(f"   ✅ {nombre:20} - {descripcion}")
        return True
    except ImportError:
        print(f"   ❌ {nombre:20} - {descripcion} [NO INSTALADO]")
        return False

def verificar_ollama():
    """Verifica si Ollama está instalado"""
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Ollama instalado")
            return True
        else:
            print(f"   ❌ Ollama no responde correctamente")
            return False
    except FileNotFoundError:
        print(f"   ❌ Ollama no está instalado")
        return False
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Ollama no responde (timeout)")
        return False

def verificar_archivos_proyecto():
    """Verifica que los archivos del proyecto existan"""
    print("\n📌 PASO 3: Verificando archivos del proyecto...")
    
    archivos_necesarios = [
        'neo_control.py',
        'neo_cerebro.py',
        'neo_voz.py',
        'neo_voz_tts.py',
        'neo_memoria.py',
        'neo_gui_integrado.py',
    ]
    
    import os
    todos_presentes = True
    
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} [FALTA]")
            todos_presentes = False
    
    return todos_presentes

def main():
    resultados = {
        'python': False,
        'dependencias': [],
        'ollama': False,
        'archivos': False
    }
    
    # Verificar Python
    resultados['python'] = verificar_python()
    
    # Verificar dependencias
    print("\n📌 PASO 2: Verificando dependencias de Python...")
    for modulo, desc in DEPENDENCIAS.items():
        if verificar_modulo(modulo, desc):
            resultados['dependencias'].append(modulo)
    
    # Verificar Ollama
    print("\n📌 PASO 2.1: Verificando Ollama (IA local)...")
    resultados['ollama'] = verificar_ollama()
    
    # Verificar archivos
    resultados['archivos'] = verificar_archivos_proyecto()
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    
    dependencias_instaladas = len(resultados['dependencias'])
    dependencias_totales = len(DEPENDENCIAS)
    
    print(f"\n✓ Python: {'✅' if resultados['python'] else '❌'}")
    print(f"✓ Dependencias: {dependencias_instaladas}/{dependencias_totales} instaladas")
    print(f"✓ Ollama: {'✅' if resultados['ollama'] else '❌'}")
    print(f"✓ Archivos: {'✅' if resultados['archivos'] else '❌'}")
    
    # Conclusión
    print("\n" + "=" * 70)
    
    if resultados['python'] and dependencias_instaladas == dependencias_totales and resultados['archivos']:
        print("🎉 ¡TODO LISTO! Puedes ejecutar NEO")
        print("\nPara iniciar la interfaz: python neo_gui_integrado.py")
    else:
        print("⚠️  FALTAN COMPONENTES")
        print("\n📝 SIGUIENTE PASO:")
        
        if not resultados['python']:
            print("   1. Instala Python 3.8 o superior")
        
        if dependencias_instaladas < dependencias_totales:
            print("   2. Instala las dependencias faltantes:")
            faltantes = set(DEPENDENCIAS.keys()) - set(resultados['dependencias'])
            for modulo in faltantes:
                print(f"      pip install {modulo if modulo != 'PIL' else 'Pillow'}")
        
        if not resultados['ollama']:
            print("   3. Instala Ollama desde: https://ollama.ai")
        
        if not resultados['archivos']:
            print("   4. Coloca todos los archivos .py en la misma carpeta")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
