# instalador_neo_completo.py - Instalador Automático de NEO
"""
Este script instala TODAS las dependencias necesarias para NEO
de forma automática y ordenada.
"""

import subprocess
import sys
import os
import time

print("=" * 70)
print("🤖 INSTALADOR AUTOMÁTICO DE NEO")
print("=" * 70)

def ejecutar_comando(comando, descripcion, opcional=False):
    """
    Ejecuta un comando y muestra el resultado
    
    Args:
        comando: Comando a ejecutar
        descripcion: Qué hace el comando
        opcional: Si es True, no detiene si falla
    """
    print(f"\n{'[OPCIONAL]' if opcional else '[REQUERIDO]'} {descripcion}")
    print(f"Ejecutando: {comando}")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo
        )
        
        if result.returncode == 0:
            print("✅ ÉXITO")
            return True
        else:
            print(f"⚠️  ADVERTENCIA: código de salida {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            
            if not opcional:
                print("❌ Este componente es necesario")
                return False
            else:
                print("⚠️  Continuando (es opcional)...")
                return True
                
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT: El comando tardó demasiado")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("\n🎯 Este script instalará:")
    print("   • PyAutoGUI (control de PC)")
    print("   • NumPy (procesamiento de datos)")
    print("   • Pillow (imágenes)")
    print("   • MSS (captura de pantalla)")
    print("   • CustomTkinter (interfaz gráfica)")
    print("   • pyttsx3 (síntesis de voz)")
    print("   • pypiwin32 (soporte Windows)")
    print("   • OpenAI Whisper (reconocimiento de voz)")
    print("   • PyAudio (captura de audio)")
    
    print("\n⚠️  ADVERTENCIAS:")
    print("   • Necesitas conexión a internet")
    print("   • Puede tardar 10-20 minutos")
    print("   • PyAudio puede fallar (normal en Windows)")
    
    print("\n" + "=" * 70)
    respuesta = input("¿Continuar con la instalación? (si/no): ").strip().lower()
    
    if respuesta != 'si':
        print("\n❌ Instalación cancelada")
        return
    
    print("\n" + "=" * 70)
    print("COMENZANDO INSTALACIÓN...")
    print("=" * 70)
    
    # Contador de éxitos
    exitos = 0
    total = 0
    
    # FASE 1: Actualizar pip
    print("\n" + "=" * 70)
    print("FASE 1: ACTUALIZAR PIP")
    print("=" * 70)
    
    total += 1
    if ejecutar_comando(
        f"{sys.executable} -m pip install --upgrade pip",
        "Actualizando pip",
        opcional=False
    ):
        exitos += 1
    
    # FASE 2: Dependencias básicas
    print("\n" + "=" * 70)
    print("FASE 2: DEPENDENCIAS BÁSICAS")
    print("=" * 70)
    
    dependencias_basicas = [
        ("pyautogui", "Control automático de PC"),
        ("numpy", "Procesamiento de datos"),
        ("Pillow", "Procesamiento de imágenes"),
        ("mss", "Captura de pantalla"),
    ]
    
    for paquete, descripcion in dependencias_basicas:
        total += 1
        if ejecutar_comando(
            f"{sys.executable} -m pip install {paquete}",
            f"Instalando {descripcion} ({paquete})",
            opcional=False
        ):
            exitos += 1
        time.sleep(1)
    
    # FASE 3: Interfaz gráfica
    print("\n" + "=" * 70)
    print("FASE 3: INTERFAZ GRÁFICA")
    print("=" * 70)
    
    total += 1
    if ejecutar_comando(
        f"{sys.executable} -m pip install customtkinter",
        "Instalando CustomTkinter",
        opcional=False
    ):
        exitos += 1
    
    # FASE 4: Sistema de voz (TTS)
    print("\n" + "=" * 70)
    print("FASE 4: SÍNTESIS DE VOZ (TTS)")
    print("=" * 70)
    
    total += 1
    if ejecutar_comando(
        f"{sys.executable} -m pip install pyttsx3",
        "Instalando pyttsx3",
        opcional=False
    ):
        exitos += 1
    
    total += 1
    if ejecutar_comando(
        f"{sys.executable} -m pip install pypiwin32",
        "Instalando pypiwin32 (soporte Windows)",
        opcional=True  # Opcional porque puede fallar en algunos sistemas
    ):
        exitos += 1
    
    # FASE 5: Reconocimiento de voz
    print("\n" + "=" * 70)
    print("FASE 5: RECONOCIMIENTO DE VOZ")
    print("=" * 70)
    
    # PyAudio (problemático)
    print("\n⚠️  IMPORTANTE sobre PyAudio:")
    print("   • Puede fallar en Windows (es normal)")
    print("   • Si falla, necesitarás un archivo .whl precompilado")
    print("   • Ver GUIA_COMPLETA.py FASE 2, PASO 2.4")
    
    total += 1
    pyaudio_ok = ejecutar_comando(
        f"{sys.executable} -m pip install pyaudio",
        "Instalando PyAudio",
        opcional=True  # Marcar como opcional porque sabemos que puede fallar
    )
    
    if pyaudio_ok:
        exitos += 1
        print("\n🎉 ¡PyAudio se instaló! (Esto es raro pero excelente)")
    else:
        print("\n⚠️  PyAudio falló (esperado)")
        print("   Necesitarás instalarlo manualmente con .whl")
        print("   Ver: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
    
    # Whisper
    print("\n⚠️  IMPORTANTE sobre Whisper:")
    print("   • Descarga ~140MB la primera vez")
    print("   • Puede tardar varios minutos")
    
    total += 1
    if ejecutar_comando(
        f"{sys.executable} -m pip install openai-whisper",
        "Instalando OpenAI Whisper",
        opcional=False
    ):
        exitos += 1
    
    # RESUMEN FINAL
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE INSTALACIÓN")
    print("=" * 70)
    
    print(f"\n✓ Instalados correctamente: {exitos}/{total}")
    print(f"✗ Fallaron: {total - exitos}/{total}")
    
    if exitos == total:
        print("\n🎉 ¡INSTALACIÓN COMPLETA!")
        print("\n✅ SIGUIENTE PASO:")
        print("   1. Instala Ollama: https://ollama.ai")
        print("   2. Descarga modelos:")
        print("      ollama pull llama3.2:3b")
        print("      ollama pull llava:7b")
        print("   3. Ejecuta: python neo_gui_integrado.py")
    
    elif exitos >= total - 1:  # Solo PyAudio falló
        print("\n🔶 CASI COMPLETA")
        print("\n✅ La mayoría se instaló correctamente")
        print("\n⚠️  PENDIENTES:")
        if not pyaudio_ok:
            print("   • PyAudio (instala .whl manualmente)")
        
        print("\n💡 PUEDES USAR NEO EN MODO TEXTO mientras tanto")
        print("   (El modo VOZ necesita PyAudio)")
    
    else:
        print("\n❌ INSTALACIÓN INCOMPLETA")
        print(f"\n⚠️  Fallaron {total - exitos} componentes")
        print("\n📝 RECOMENDACIÓN:")
        print("   1. Verifica tu conexión a internet")
        print("   2. Ejecuta este script de nuevo")
        print("   3. Si sigue fallando, instala manualmente:")
        print("      pip install [nombre_del_paquete]")
    
    print("\n" + "=" * 70)
    print("🔍 Para verificar qué falta:")
    print("   python verificar_neo.py")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
    
    print("\n\nPresiona Enter para cerrar...")
    input()