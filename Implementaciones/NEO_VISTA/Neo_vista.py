# capturar_pantalla.py - Captura y describe tu pantalla
import mss
import mss.tools
from PIL import Image
import subprocess
import os
import time

print("=" * 60)
print("📸 SISTEMA DE CAPTURA Y DESCRIPCIÓN DE PANTALLA")
print("=" * 60)

def capturar_pantalla():
    """Captura la pantalla actual"""
    print("\n[1/3] Capturando pantalla...")
    
    # Capturar
    sct = mss.mss()
    monitor = sct.monitors[1]  # Pantalla principal
    screenshot = sct.grab(monitor)
    
    # Guardar
    archivo = "mi_pantalla.png"
    mss.tools.to_png(screenshot.rgb, screenshot.size, output=archivo)
    
    print(f"✓ Captura guardada: {archivo}")
    return archivo

def optimizar_imagen(archivo):
    """Hace la imagen más pequeña para procesar más rápido"""
    print("[2/3] Optimizando imagen...")
    
    img = Image.open(archivo)
    print(f"  Tamaño original: {img.size[0]}x{img.size[1]} px")
    
    # Reducir a 1280px de ancho máximo
    if img.size[0] > 1280:
        ratio = 1280 / img.size[0]
        nuevo_ancho = 1280
        nuevo_alto = int(img.size[1] * ratio)
        
        img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        img.save(archivo, optimize=True, quality=85)
        
        print(f"  Tamaño optimizado: {nuevo_ancho}x{nuevo_alto} px")
    else:
        print(f"  Tamaño ya es bueno, no se optimizó")
    
    print("✓ Imagen lista")
    return archivo

def describir_pantalla(archivo):
    """Usa LLaVA para describir la imagen"""
    print("[3/3] Analizando con IA...")
    print("  (Esto tomará 20-30 segundos)\n")
    
    # Prompt para LLaVA
    prompt = """Analiza esta captura de pantalla en español con MUCHO DETALLE.

Estructura tu respuesta así:

APLICACIONES ABIERTAS:
[Lista las aplicaciones/ventanas visibles]

CONTENIDO ESPECÍFICO:
[Describe qué texto, imágenes o elementos ves]

ACTIVIDAD DEL USUARIO:
[Qué está haciendo probablemente]

OBSERVACIONES:
[Cualquier detalle relevante]

Sé muy específico. Si ves código, menciona el lenguaje. Si ves un navegador, di qué sitios. Si ves texto, menciona de qué trata."""
    
    # Comando completo
    comando = f'ollama run llava:7b "Analiza esta imagen: {archivo}. {prompt}"'
    
    try:
        # Ejecutar Ollama
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        
        if resultado.stdout:
            descripcion = resultado.stdout.strip()
            return descripcion
        else:
            return "No se pudo obtener descripción"
            
    except subprocess.TimeoutExpired:
        return "Timeout: La IA tardó demasiado"
    except Exception as e:
        return f"Error: {e}"

def main():
    """Función principal"""
    
    print("\n💡 Cambia a la ventana que quieres analizar")
    print("   y vuelve aquí en 3 segundos...\n")
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Proceso completo
    archivo = capturar_pantalla()
    archivo = optimizar_imagen(archivo)
    descripcion = describir_pantalla(archivo)
    
    # Mostrar resultado
    print("\n" + "=" * 60)
    print("👁️  DESCRIPCIÓN DE TU PANTALLA:")
    print("=" * 60)
    print(f"\n{descripcion}\n")
    print("=" * 60)
    
    # Preguntar si quiere otro
    print("\n¿Quieres analizar otra vez tu pantalla? (si/no): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta == 'si':
        print("\n" + "=" * 60)
        main()
    else:
        print("\n👋 SE ACABO")
        
        # Limpiar archivo
        if os.path.exists(archivo):
            os.remove(archivo)

# Ejecutar
if __name__ == "__main__":
    main()