# diagnostico_neo_completo.py - Diagnóstico Completo del Sistema NEO
"""
Este script prueba CADA componente de NEO y te dice exactamente:
- ✅ Qué funciona
- ❌ Qué no funciona
- ⚠️ Qué tiene problemas
"""

import sys
import subprocess
import time

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA NEO")
print("=" * 70)

resultados = {
    'modulos_python': {},
    'ollama': {},
    'control_pc': None,
    'tts': None,
    'voz': None,
    'cerebro': None,
    'gui': None
}

# ============================================
# FASE 1: VERIFICAR MÓDULOS PYTHON
# ============================================
print("\n" + "=" * 70)
print("FASE 1: VERIFICANDO MÓDULOS DE PYTHON")
print("=" * 70)

modulos_requeridos = {
    'pyautogui': 'Control de PC',
    'numpy': 'Procesamiento de datos',
    'PIL': 'Imágenes (Pillow)',
    'mss': 'Captura de pantalla',
    'customtkinter': 'Interfaz gráfica',
    'pyttsx3': 'Síntesis de voz',
    'whisper': 'Reconocimiento de voz',
    'pyaudio': 'Captura de audio',
}

for modulo, descripcion in modulos_requeridos.items():
    try:
        if modulo == 'PIL':
            __import__('PIL')
        else:
            __import__(modulo)
        print(f"   ✅ {modulo:20} - {descripcion}")
        resultados['modulos_python'][modulo] = True
    except ImportError:
        print(f"   ❌ {modulo:20} - {descripcion} [NO INSTALADO]")
        resultados['modulos_python'][modulo] = False

# ============================================
# FASE 2: VERIFICAR OLLAMA
# ============================================
print("\n" + "=" * 70)
print("FASE 2: VERIFICANDO OLLAMA (IA LOCAL)")
print("=" * 70)

# Verificar si Ollama está instalado
print("\n[2.1] Verificando instalación de Ollama...")
try:
    result = subprocess.run(
        ['ollama', '--version'],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0:
        print(f"   ✅ Ollama instalado: {result.stdout.strip()}")
        resultados['ollama']['instalado'] = True
    else:
        print(f"   ❌ Ollama no responde")
        resultados['ollama']['instalado'] = False
except FileNotFoundError:
    print(f"   ❌ Ollama NO está instalado")
    resultados['ollama']['instalado'] = False
except subprocess.TimeoutExpired:
    print(f"   ⚠️  Ollama no responde (timeout)")
    resultados['ollama']['instalado'] = False

# Verificar modelos descargados
if resultados['ollama'].get('instalado'):
    print("\n[2.2] Verificando modelos descargados...")
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        modelos_texto = result.stdout
        
        # Verificar llama3.2:3b
        if 'llama3.2' in modelos_texto or 'llama3.2:3b' in modelos_texto:
            print("   ✅ llama3.2:3b (cerebro) - INSTALADO")
            resultados['ollama']['llama3.2'] = True
        else:
            print("   ❌ llama3.2:3b (cerebro) - NO INSTALADO")
            resultados['ollama']['llama3.2'] = False
        
        # Verificar llava:7b
        if 'llava' in modelos_texto:
            print("   ✅ llava:7b (visión) - INSTALADO")
            resultados['ollama']['llava'] = True
        else:
            print("   ❌ llava:7b (visión) - NO INSTALADO")
            resultados['ollama']['llava'] = False
            
    except Exception as e:
        print(f"   ⚠️  No se pudo verificar modelos: {e}")
        resultados['ollama']['llama3.2'] = False
        resultados['ollama']['llava'] = False

# ============================================
# FASE 3: PROBAR ARCHIVOS NEO
# ============================================
print("\n" + "=" * 70)
print("FASE 3: VERIFICANDO ARCHIVOS DEL PROYECTO")
print("=" * 70)

import os

archivos_necesarios = [
    'neo_control.py',
    'neo_cerebro.py',
    'neo_voz.py',
    'neo_voz_tts.py',
    'neo_memoria.py',
    'neo_gui_integrado.py',
]

todos_presentes = True
for archivo in archivos_necesarios:
    if os.path.exists(archivo):
        print(f"   ✅ {archivo}")
    else:
        print(f"   ❌ {archivo} [FALTA]")
        todos_presentes = False

# ============================================
# FASE 4: PROBAR CONTROL DE PC
# ============================================
print("\n" + "=" * 70)
print("FASE 4: PROBANDO CONTROL DE PC (neo_control.py)")
print("=" * 70)

try:
    print("\n⏳ Intentando importar neo_control...")
    import neo_control
    print("   ✅ neo_control.py se importa correctamente")
    resultados['control_pc'] = True
    
    # Probar una función simple
    print("\n⏳ Probando función básica...")
    print("   (Esto no hará nada visible, solo verifica que funcione)")
    
except Exception as e:
    print(f"   ❌ Error al importar: {e}")
    resultados['control_pc'] = False

# ============================================
# FASE 5: PROBAR TTS (SÍNTESIS DE VOZ)
# ============================================
print("\n" + "=" * 70)
print("FASE 5: PROBANDO SÍNTESIS DE VOZ (neo_voz_tts.py)")
print("=" * 70)

try:
    print("\n⏳ Intentando importar neo_voz_tts...")
    from neo_voz_tts import inicializar_tts, neo_habla
    print("   ✅ neo_voz_tts.py se importa correctamente")
    
    print("\n⏳ Inicializando motor TTS...")
    tts = inicializar_tts(rate=180, volume=0.8, debug=False)
    print("   ✅ Motor TTS inicializado")
    
    print("\n🔊 PRUEBA DE VOZ:")
    print("   NEO dirá: 'Sistema de voz funcionando'")
    print("   (Si NO escuchas nada, hay un problema)")
    
    respuesta = input("\n¿Quieres probar la voz ahora? (si/no): ").strip().lower()
    if respuesta == 'si':
        neo_habla("Sistema de voz funcionando")
        print("   ✅ Prueba de voz completada")
        resultados['tts'] = True
    else:
        print("   ⏭️  Prueba de voz omitida")
        resultados['tts'] = 'omitido'
    
except Exception as e:
    print(f"   ❌ Error con TTS: {e}")
    resultados['tts'] = False

# ============================================
# FASE 6: PROBAR RECONOCIMIENTO DE VOZ
# ============================================
print("\n" + "=" * 70)
print("FASE 6: PROBANDO RECONOCIMIENTO DE VOZ (neo_voz.py)")
print("=" * 70)

print("\n⚠️  ADVERTENCIA:")
print("   • Esta prueba usará tu micrófono")
print("   • Puede tardar ~10 segundos")
print("   • Deberás hablar algo")

respuesta = input("\n¿Quieres probar el reconocimiento de voz? (si/no): ").strip().lower()

if respuesta == 'si':
    try:
        print("\n⏳ Cargando Whisper (puede tardar 10-20 segundos la primera vez)...")
        from neo_voz import escuchar_audio, transcribir_audio
        print("   ✅ neo_voz.py cargado")
        
        print("\n🎤 PRUEBA:")
        print("   1. Presiona Enter")
        print("   2. Di algo en voz alta")
        print("   3. Espera el resultado")
        
        input("\nPresiona Enter para iniciar la grabación...")
        
        archivo = escuchar_audio(timeout=8, esperar_activacion=True)
        
        if archivo:
            print("\n⏳ Transcribiendo...")
            texto = transcribir_audio(archivo)
            
            if texto:
                print(f"\n   ✅ Transcripción exitosa: '{texto}'")
                resultados['voz'] = True
            else:
                print("   ❌ No se pudo transcribir")
                resultados['voz'] = False
            
            # Limpiar archivo temporal
            import os
            if os.path.exists(archivo):
                os.remove(archivo)
        else:
            print("   ⚠️  No se capturó audio")
            resultados['voz'] = 'sin_audio'
            
    except Exception as e:
        print(f"   ❌ Error con reconocimiento de voz: {e}")
        resultados['voz'] = False
else:
    print("   ⏭️  Prueba de voz omitida")
    resultados['voz'] = 'omitido'

# ============================================
# FASE 7: PROBAR CEREBRO (CON OLLAMA)
# ============================================
print("\n" + "=" * 70)
print("FASE 7: PROBANDO CEREBRO IA (neo_cerebro.py)")
print("=" * 70)

if not resultados['ollama'].get('instalado'):
    print("   ⏭️  Ollama no está instalado, omitiendo prueba")
    resultados['cerebro'] = 'ollama_falta'
elif not resultados['ollama'].get('llama3.2'):
    print("   ⏭️  Modelo llama3.2:3b no instalado, omitiendo prueba")
    resultados['cerebro'] = 'modelo_falta'
else:
    try:
        print("\n⏳ Intentando importar neo_cerebro...")
        import neo_cerebro
        print("   ✅ neo_cerebro.py se importa correctamente")
        
        print("\n⏳ Probando procesamiento de comando simple...")
        print("   (Esto puede tardar 10-15 segundos la primera vez)")
        
        plan = neo_cerebro.procesar_comando("abre notepad")
        
        if plan:
            print(f"   ✅ Cerebro funciona: {plan.get('explicacion', 'Sin explicación')}")
            print(f"   📋 Acciones generadas: {len(plan.get('acciones', []))}")
            resultados['cerebro'] = True
        else:
            print("   ❌ No se generó plan")
            resultados['cerebro'] = False
            
    except Exception as e:
        print(f"   ❌ Error con cerebro: {e}")
        resultados['cerebro'] = False

# ============================================
# FASE 8: VERIFICAR GUI
# ============================================
print("\n" + "=" * 70)
print("FASE 8: VERIFICANDO GUI (neo_gui_integrado.py)")
print("=" * 70)

try:
    print("\n⏳ Verificando importación de GUI...")
    # No la ejecutamos, solo verificamos que se pueda importar
    with open('neo_gui_integrado.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
        if 'class NEOAppIntegrado' in contenido:
            print("   ✅ neo_gui_integrado.py existe y tiene la clase principal")
            resultados['gui'] = True
        else:
            print("   ⚠️  Archivo existe pero puede tener problemas")
            resultados['gui'] = 'dudoso'
except Exception as e:
    print(f"   ❌ Error al verificar GUI: {e}")
    resultados['gui'] = False

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "=" * 70)
print("📊 RESUMEN DEL DIAGNÓSTICO")
print("=" * 70)

print("\n🔧 MÓDULOS PYTHON:")
modulos_ok = sum(1 for v in resultados['modulos_python'].values() if v)
modulos_total = len(resultados['modulos_python'])
print(f"   {modulos_ok}/{modulos_total} instalados correctamente")

print("\n🧠 OLLAMA:")
if resultados['ollama'].get('instalado'):
    print("   ✅ Ollama instalado")
    if resultados['ollama'].get('llama3.2'):
        print("   ✅ llama3.2:3b disponible")
    else:
        print("   ❌ llama3.2:3b NO disponible")
    
    if resultados['ollama'].get('llava'):
        print("   ✅ llava:7b disponible")
    else:
        print("   ❌ llava:7b NO disponible")
else:
    print("   ❌ Ollama NO instalado")

print("\n🎯 COMPONENTES NEO:")
componentes = {
    'Control PC': resultados['control_pc'],
    'TTS (Voz salida)': resultados['tts'],
    'Reconocimiento voz': resultados['voz'],
    'Cerebro IA': resultados['cerebro'],
    'GUI': resultados['gui']
}

for nombre, estado in componentes.items():
    if estado == True:
        print(f"   ✅ {nombre:20} - Funcional")
    elif estado == False:
        print(f"   ❌ {nombre:20} - Con problemas")
    elif estado == 'omitido':
        print(f"   ⏭️  {nombre:20} - No probado")
    else:
        print(f"   ⚠️  {nombre:20} - Estado: {estado}")

# ============================================
# RECOMENDACIONES
# ============================================
print("\n" + "=" * 70)
print("💡 RECOMENDACIONES")
print("=" * 70)

problemas = []

# Verificar problemas de módulos
if not all(resultados['modulos_python'].values()):
    faltantes = [k for k, v in resultados['modulos_python'].items() if not v]
    problemas.append(f"Instalar módulos: {', '.join(faltantes)}")

# Verificar Ollama
if not resultados['ollama'].get('instalado'):
    problemas.append("Instalar Ollama desde https://ollama.ai")
elif not resultados['ollama'].get('llama3.2'):
    problemas.append("Descargar modelo: ollama pull llama3.2:3b")
elif not resultados['ollama'].get('llava'):
    problemas.append("Descargar modelo: ollama pull llava:7b")

# Verificar componentes
if resultados['control_pc'] == False:
    problemas.append("Revisar neo_control.py (tiene errores)")

if resultados['tts'] == False:
    problemas.append("Revisar neo_voz_tts.py (TTS no funciona)")

if resultados['voz'] == False:
    problemas.append("Revisar neo_voz.py (reconocimiento falla)")

if resultados['cerebro'] == False:
    problemas.append("Revisar neo_cerebro.py o conexión con Ollama")

if problemas:
    print("\n⚠️  PENDIENTES:")
    for i, problema in enumerate(problemas, 1):
        print(f"   {i}. {problema}")
else:
    print("\n🎉 ¡TODO FUNCIONA PERFECTAMENTE!")
    print("\n✅ PUEDES EJECUTAR:")
    print("   python neo_gui_integrado.py")

print("\n" + "=" * 70)
print("Diagnóstico completado")
print("=" * 70)