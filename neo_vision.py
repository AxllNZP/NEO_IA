# neo_vision.py - Sistema de Visión para NEO (Ojos de la IA)
"""
Este módulo le permite a NEO "ver" y analizar tu pantalla.
Usa Llava (modelo de visión) para entender qué hay en pantalla.
"""

import mss
import mss.tools
from PIL import Image
import subprocess
import os
import base64
from io import BytesIO

print("=" * 60)
print("NEO - Sistema de Visión v1.0")
print("=" * 60)

# ==========================================
# CONFIGURACIÓN
# ==========================================

# Modelo de visión (Llava via Ollama)
MODELO_VISION = "llava:7b"

# Configuración de optimización de imagen
MAX_ANCHO = 1280          # Ancho máximo en píxeles (más pequeño = más rápido)
CALIDAD_COMPRESION = 85   # Calidad JPEG (1-100, más bajo = más rápido)

# Archivo temporal (se borra después de usar)
TEMP_CAPTURA = "temp_neo_vision.png"

# ==========================================
# Variables de estado
# ==========================================

_ultima_captura = None           # Guarda la última imagen capturada
_ultima_descripcion = None       # Guarda la última descripción
_vision_activa = False           # Si la visión está actualmente activa

# ==========================================
# FUNCIÓN 1: Capturar Pantalla
# ==========================================

def capturar_pantalla_rapida():
    """
    Captura la pantalla completa de forma muy rápida.
    
    Returns:
        PIL.Image: Objeto imagen de la pantalla
        None: Si hay error
    """
    try:
        # Crear capturador MSS (muy rápido)
        sct = mss.mss()
        
        # Capturar monitor principal (índice 1)
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        # Convertir a PIL Image para poder manipular
        img = Image.frombytes(
            'RGB',
            screenshot.size,
            screenshot.rgb
        )
        
        return img
        
    except Exception as e:
        print(f"❌ Error al capturar pantalla: {e}")
        return None


# ==========================================
# FUNCIÓN 2: Optimizar Imagen
# ==========================================

def optimizar_imagen(imagen):
    """
    Optimiza la imagen para análisis rápido con IA.
    - Reduce tamaño si es muy grande
    - Comprime sin perder mucha calidad
    
    Args:
        imagen (PIL.Image): Imagen original
        
    Returns:
        PIL.Image: Imagen optimizada
    """
    try:
        ancho_original, alto_original = imagen.size
        
        # Si la imagen es más ancha que MAX_ANCHO, redimensionar
        if ancho_original > MAX_ANCHO:
            # Calcular nuevo tamaño manteniendo proporción
            ratio = MAX_ANCHO / ancho_original
            nuevo_ancho = MAX_ANCHO
            nuevo_alto = int(alto_original * ratio)
            
            # Redimensionar (LANCZOS = mejor calidad)
            imagen = imagen.resize(
                (nuevo_ancho, nuevo_alto),
                Image.Resampling.LANCZOS
            )
            
            print(f"   📐 Optimizado: {ancho_original}x{alto_original} → {nuevo_ancho}x{nuevo_alto}")
        else:
            print(f"   📐 Tamaño original OK: {ancho_original}x{alto_original}")
        
        return imagen
        
    except Exception as e:
        print(f"❌ Error al optimizar: {e}")
        return imagen  # Devolver original si falla


# ==========================================
# FUNCIÓN 3: Convertir a Base64
# ==========================================

def imagen_a_base64(imagen):
    """
    Convierte imagen PIL a string base64.
    Ollama necesita las imágenes en formato base64.
    
    Args:
        imagen (PIL.Image): Imagen a convertir
        
    Returns:
        str: Imagen en formato base64
        None: Si hay error
    """
    try:
        # Crear buffer en memoria (sin archivo temporal)
        buffer = BytesIO()
        
        # Guardar imagen en buffer como JPEG
        imagen.save(buffer, format='JPEG', quality=CALIDAD_COMPRESION, optimize=True)
        
        # Obtener bytes
        img_bytes = buffer.getvalue()
        
        # Convertir a base64
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        return img_base64
        
    except Exception as e:
        print(f"❌ Error al convertir a base64: {e}")
        return None
# ==========================================|

# ==========================================
# FUNCIÓN 4: Analizar Imagen con Llava
# ==========================================

def analizar_con_llava(imagen_base64, pregunta="Describe en español lo que ves en esta imagen"):
    """
    Analiza una imagen usando Llava (modelo de visión de Ollama).
    
    Args:
        imagen_base64 (str): Imagen en formato base64
        pregunta (str): Qué preguntarle a Llava sobre la imagen
        
    Returns:
        str: Descripción/respuesta de Llava
        None: Si hay error
    """
    try:
        print("   🧠 Analizando con Llava...")
        print(f"   ⏱️  Esto tomará 5-10 segundos...")
        
        # Construir el comando para Ollama
        # Formato: ollama run llava:7b "prompt con imagen"
        comando = [
            'ollama',
            'run',
            MODELO_VISION,
            pregunta
        ]
        
        # Crear el input con la imagen en base64
        # Llava espera el formato: imagen en stdin + prompt
        input_data = f"data:image/jpeg;base64,{imagen_base64}"
        
        # Ejecutar Ollama
        resultado = subprocess.run(
            comando,
            input=input_data,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60  # Máximo 60 segundos
        )
        
        # Verificar si funcionó
        if resultado.returncode == 0 and resultado.stdout:
            descripcion = resultado.stdout.strip()
            print("   ✅ Análisis completado")
            return descripcion
        else:
            print(f"   ❌ Llava no respondió correctamente")
            if resultado.stderr:
                print(f"   Error: {resultado.stderr[:200]}")
            return None
            
    except subprocess.TimeoutExpired:
        print("   ⏱️  Timeout: Llava tardó demasiado (>60s)")
        return None
    except FileNotFoundError:
        print("   ❌ Ollama no está instalado o no está en PATH")
        return None
    except Exception as e:
        print(f"   ❌ Error en análisis: {e}")
        return None


# ==========================================
# FUNCIÓN 5: Ver Pantalla (TODO EN UNO)
# ==========================================

def ver_pantalla(pregunta=None):
    """
    Función principal: Captura pantalla y la analiza con IA.
    Esta es la función que NEO usará para "ver".
    
    Args:
        pregunta (str): Pregunta específica sobre la pantalla
                       Si es None, hace descripción general
        
    Returns:
        dict: {
            'exito': bool,
            'descripcion': str,
            'imagen': PIL.Image (opcional),
            'error': str (si hay error)
        }
    """
    global _ultima_captura, _ultima_descripcion, _vision_activa
    
    print("\n👁️  NEO está viendo tu pantalla...")
    _vision_activa = True
    
    try:
        # PASO 1: Capturar pantalla
        print("   [1/4] Capturando pantalla...")
        imagen = capturar_pantalla_rapida()
        
        if imagen is None:
            _vision_activa = False
            return {
                'exito': False,
                'error': 'No se pudo capturar la pantalla'
            }
        
        # PASO 2: Optimizar imagen
        print("   [2/4] Optimizando imagen...")
        imagen_opt = optimizar_imagen(imagen)
        
        # PASO 3: Convertir a base64
        print("   [3/4] Convirtiendo a base64...")
        img_base64 = imagen_a_base64(imagen_opt)
        
        if img_base64 is None:
            _vision_activa = False
            return {
                'exito': False,
                'error': 'No se pudo convertir imagen'
            }
        
        # PASO 4: Analizar con Llava
        print("   [4/4] Analizando con IA...")
        
        # Si no hay pregunta específica, hacer descripción general
        if pregunta is None:
            pregunta = """Describe en español lo que ves en esta captura de pantalla.

Menciona:
1. ¿Qué aplicaciones o programas están abiertos?
2. ¿Qué contenido específico hay visible?
3. ¿Qué elementos importantes hay en pantalla?

Sé específico pero conciso."""
        
        descripcion = analizar_con_llava(img_base64, pregunta)
        
        if descripcion is None:
            _vision_activa = False
            return {
                'exito': False,
                'error': 'Llava no pudo analizar la imagen'
            }
        
        # Guardar en cache
        _ultima_captura = imagen_opt
        _ultima_descripcion = descripcion
        _vision_activa = False
        
        print("   ✅ Visión completada\n")
        
        return {
            'exito': True,
            'descripcion': descripcion,
            'imagen': imagen_opt
        }
        
    except Exception as e:
        _vision_activa = False
        print(f"   ❌ Error general: {e}\n")
        return {
            'exito': False,
            'error': str(e)
        }


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def obtener_ultima_descripcion():
    """Obtiene la última descripción de pantalla"""
    return _ultima_descripcion


def obtener_ultima_captura():
    """Obtiene la última imagen capturada"""
    return _ultima_captura


def vision_esta_activa():
    """Verifica si la visión está procesando"""
    return _vision_activa


# ==========================================
# FUNCIÓN DE PRUEBA INTERACTIVA
# ==========================================

def probar_vision():
    """
    Modo de prueba para el sistema de visión.
    Te permite probar si NEO puede ver tu pantalla.
    """
    print("\n" + "=" * 60)
    print("MODO DE PRUEBA - Sistema de Visión de NEO")
    print("=" * 60)
    print("\n📋 INSTRUCCIONES:")
    print("   1. Abre alguna aplicación o ventana")
    print("   2. Presiona Enter aquí")
    print("   3. NEO analizará tu pantalla")
    print("   4. Te dirá qué ve\n")
    
    while True:
        print("-" * 60)
        
        # Menú de opciones
        print("\n¿Qué quieres hacer?")
        print("  1. Ver pantalla (descripción general)")
        print("  2. Hacer pregunta específica sobre pantalla")
        print("  3. Ver última descripción")
        print("  0. Salir")
        
        opcion = input("\nElige (0-3): ").strip()
        
        if opcion == "1":
            # Descripción general
            print("\n" + "=" * 60)
            input("Prepara tu pantalla y presiona Enter...")
            
            resultado = ver_pantalla()
            
            if resultado['exito']:
                print("\n" + "=" * 60)
                print("👁️  LO QUE NEO VE:")
                print("=" * 60)
                print(f"\n{resultado['descripcion']}\n")
                print("=" * 60)
            else:
                print(f"\n❌ Error: {resultado.get('error', 'Desconocido')}")
        
        elif opcion == "2":
            # Pregunta específica
            pregunta = input("\n¿Qué quieres preguntarle a NEO sobre tu pantalla?: ").strip()
            
            if not pregunta:
                print("⚠️  No escribiste ninguna pregunta")
                continue
            
            print("\n" + "=" * 60)
            input("Prepara tu pantalla y presiona Enter...")
            
            resultado = ver_pantalla(pregunta)
            
            if resultado['exito']:
                print("\n" + "=" * 60)
                print("👁️  RESPUESTA DE NEO:")
                print("=" * 60)
                print(f"\n{resultado['descripcion']}\n")
                print("=" * 60)
            else:
                print(f"\n❌ Error: {resultado.get('error', 'Desconocido')}")
        
        elif opcion == "3":
            # Ver última descripción
            ultima = obtener_ultima_descripcion()
            
            if ultima:
                print("\n" + "=" * 60)
                print("📝 ÚLTIMA DESCRIPCIÓN:")
                print("=" * 60)
                print(f"\n{ultima}\n")
                print("=" * 60)
            else:
                print("\n⚠️  No hay descripción previa")
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida")


# ==========================================
# VERIFICAR OLLAMA Y LLAVA
# ==========================================

def verificar_llava():
    """
    Verifica si Ollama y Llava están instalados y funcionando.
    """
    print("\n🔍 Verificando sistema de visión...")
    
    # Verificar Ollama
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("   ✅ Ollama instalado")
        else:
            print("   ❌ Ollama no responde")
            return False
    except FileNotFoundError:
        print("   ❌ Ollama NO está instalado")
        print("   📥 Descárgalo de: https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("   ⚠️  Ollama no responde (timeout)")
        return False
    
    # Verificar modelo Llava
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if 'llava' in result.stdout.lower():
            print("   ✅ Modelo Llava instalado")
            return True
        else:
            print("   ❌ Modelo Llava NO instalado")
            print("   📥 Instala con: ollama pull llava:7b")
            return False
            
    except Exception as e:
        print(f"   ❌ Error al verificar Llava: {e}")
        return False


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":
    print("\n✓ Sistema de Visión cargado")
    print("\nEste módulo le da 'ojos' a NEO\n")
    
    # Verificar que todo esté instalado
    if not verificar_llava():
        print("\n⚠️  El sistema de visión NO está completo")
        print("\nPara usar la visión de NEO necesitas:")
        print("  1. Ollama instalado (https://ollama.ai)")
        print("  2. Modelo Llava: ollama pull llava:7b")
        print("\n" + "=" * 60)
        input("\nPresiona Enter para salir...")
        exit(1)
    
    print("\n✅ Todo listo para usar visión")
    
    # Preguntar si quiere probar
    print("\n¿Quieres probar el sistema de visión? (si/no): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta == 'si':
        probar_vision()
    else:
        print("\n✓ Módulo listo para importar")
        print("\nEjemplo de uso:")
        print("  from neo_vision import ver_pantalla")
        print("  resultado = ver_pantalla()")
        print("  print(resultado['descripcion'])")