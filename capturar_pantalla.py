# capturar_pantalla.py - Sistema de captura y análisis de pantalla
import mss
import mss.tools
from PIL import Image
import subprocess
import os
import time

print("=" * 60)
print("Sistema de Captura y Análisis de Pantalla")
print("=" * 60)

def capturar_pantalla():
    print("\n[1/3] Capturando pantalla...")
    
    sct = mss.mss()
    monitor = sct.monitors[1]
    screenshot = sct.grab(monitor)
    
    archivo = "captura_pantalla.png"
    mss.tools.to_png(screenshot.rgb, screenshot.size, output=archivo)
    
    print(f"Captura guardada: {archivo}")
    return archivo

def optimizar_imagen(archivo):
    print("[2/3] Optimizando imagen...")
    
    img = Image.open(archivo)
    print(f"  Tamaño original: {img.size[0]}x{img.size[1]} px")
    
    if img.size[0] > 1280:
        ratio = 1280 / img.size[0]
        nuevo_ancho = 1280
        nuevo_alto = int(img.size[1] * ratio)
        
        img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        img.save(archivo, optimize=True, quality=85)
        
        print(f"  Tamaño optimizado: {nuevo_ancho}x{nuevo_alto} px")
    else:
        print(f"  Tamaño ya es bueno, no se optimizó")
    
    print("Imagen lista")
    return archivo

def describir_pantalla(archivo):
    print("[3/3] Analizando con IA...")
    print("  (Esto tomará 20-30 segundos)\n")
    
    prompt = """Describe en español lo que ves en esta captura de pantalla.

Menciona:
1. ¿Qué aplicaciones o programas están abiertos?
2. ¿Qué contenido específico hay visible?
3. ¿Qué está haciendo el usuario probablemente?

Sé específico pero conciso."""
    
    comando = f'ollama run llava:7b "Analiza esta imagen: {archivo}. {prompt}"'
    
    try:
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
    print("\nCambia a la ventana que quieres analizar")
    print("   y vuelve aquí en 3 segundos...\n")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    archivo = capturar_pantalla()
    archivo = optimizar_imagen(archivo)
    descripcion = describir_pantalla(archivo)
    
    print("\n" + "=" * 60)
    print("DESCRIPCIÓN DE TU PANTALLA:")
    print("=" * 60)
    print(f"\n{descripcion}\n")
    print("=" * 60)
    
    print("\n¿Quieres analizar otra pantalla? (si/no): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta == 'si':
        print("\n" + "=" * 60)
        main()
    else:
        print("\n¡Hasta luego!")
        
        if os.path.exists(archivo):
            os.remove(archivo)

if __name__ == "__main__":
    main()