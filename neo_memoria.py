# neo_memoria.py - Sistema de memoria para NEO
import json
import os
from datetime import datetime

ARCHIVO_MEMORIA = "neo_memoria.json"
ARCHIVO_LOGS = "neo_logs.txt"

def guardar_comando(comando, plan, exito):
    """
    Guarda un comando ejecutado en la memoria
    
    Args:
        comando (str): Comando del usuario
        plan (dict): Plan generado
        exito (bool): Si se ejecutó correctamente
    """
    memoria = cargar_memoria()
    
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comando": comando,
        "explicacion": plan.get('explicacion', '') if plan else '',
        "num_acciones": len(plan.get('acciones', [])) if plan else 0,
        "exito": exito
    }
    
    memoria.append(entrada)
    
    # Mantener solo últimas 50
    if len(memoria) > 50:
        memoria = memoria[-50:]
    
    try:
        with open(ARCHIVO_MEMORIA, 'w', encoding='utf-8') as f:
            json.dump(memoria, f, indent=2, ensure_ascii=False)
    except:
        pass

def cargar_memoria():
    """Carga la memoria completa"""
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def obtener_contexto_memoria():
    """
    Obtiene las últimas 3 interacciones para contexto
    
    Returns:
        str: Resumen del contexto
    """
    memoria = cargar_memoria()
    
    if not memoria:
        return ""
    
    recientes = memoria[-3:]
    
    contexto = "Historial reciente:\n"
    for item in recientes:
        contexto += f"- '{item['comando']}' → {item['explicacion']}\n"
    
    return contexto

def obtener_ultimo_comando():
    """Obtiene el último comando ejecutado"""
    memoria = cargar_memoria()
    if memoria:
        return memoria[-1]
    return None

def guardar_log(mensaje, tipo="INFO"):
    """
    Guarda un mensaje en el archivo de logs
    
    Args:
        mensaje (str): Mensaje a guardar
        tipo (str): INFO, ERROR, WARNING
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] [{tipo}] {mensaje}\n"
    
    try:
        with open(ARCHIVO_LOGS, 'a', encoding='utf-8') as f:
            f.write(linea)
    except:
        pass

def limpiar_memoria():
    """Borra toda la memoria"""
    if os.path.exists(ARCHIVO_MEMORIA):
        os.remove(ARCHIVO_MEMORIA)
    print("✓ Memoria limpiada")

def limpiar_logs():
    """Borra todos los logs"""
    if os.path.exists(ARCHIVO_LOGS):
        os.remove(ARCHIVO_LOGS)
    print("✓ Logs limpiados")

def mostrar_historial(cantidad=10):
    """Muestra los últimos N comandos"""
    memoria = cargar_memoria()
    
    if not memoria:
        print("No hay historial")
        return
    
    ultimos = memoria[-cantidad:]
    
    print("\n" + "=" * 60)
    print(f"HISTORIAL (últimos {len(ultimos)} comandos)")
    print("=" * 60)
    
    for i, item in enumerate(ultimos, 1):
        icono = "✓" if item['exito'] else "✗"
        print(f"\n{i}. {icono} [{item['timestamp']}]")
        print(f"   Comando: {item['comando']}")
        print(f"   Resultado: {item['explicacion']}")
        print(f"   Acciones: {item['num_acciones']}")
    
    print("\n" + "=" * 60)


# ============================================
# CONTEXTO TEMPORAL (se pierde al cerrar NEO)
# ============================================

# Variable global que almacena el contexto
_contexto_actual = {
    'ultima_app': None,           # Última aplicación abierta
    'ultima_url': None,           # Última URL visitada
    'ultimo_archivo': None,       # Último archivo abierto
    'ultima_accion': None,        # Última acción ejecutada
    'ultima_busqueda': None,      # Última búsqueda en Google
    'volumen_cambios': 0,         # Cuántas veces cambió el volumen
    'ventanas_abiertas': [],      # Lista de ventanas abiertas
}

# ============================================
# FUNCIÓN: actualizar_contexto
# ============================================
def actualizar_contexto(tipo, valor):
    """
    Actualiza el contexto con nueva información.
    
    Args:
        tipo (str): Tipo de contexto ('app', 'url', 'archivo', 'accion')
        valor: Valor a guardar
    
    Ejemplos:
        actualizar_contexto('app', 'chrome')
        actualizar_contexto('url', 'google.com')
        actualizar_contexto('archivo', 'reporte.xlsx')
    """
    global _contexto_actual
    
    if tipo == 'app':
        _contexto_actual['ultima_app'] = valor
        # Agregar a lista de ventanas abiertas si no está
        if valor and valor not in _contexto_actual['ventanas_abiertas']:
            _contexto_actual['ventanas_abiertas'].append(valor)
    
    elif tipo == 'url':
        _contexto_actual['ultima_url'] = valor
    
    elif tipo == 'archivo':
        _contexto_actual['ultimo_archivo'] = valor
    
    elif tipo == 'accion':
        _contexto_actual['ultima_accion'] = valor
    
    elif tipo == 'busqueda':
        _contexto_actual['ultima_busqueda'] = valor
    
    elif tipo == 'volumen':
        _contexto_actual['volumen_cambios'] += 1
    
    # Guardar en log
    guardar_log(f"Contexto actualizado: {tipo} = {valor}", "CONTEXTO")

# ============================================
# FUNCIÓN: obtener_contexto
# ============================================
def obtener_contexto(tipo=None):
    """
    Obtiene información del contexto.
    
    Args:
        tipo (str): Tipo específico o None para todo
    
    Returns:
        dict o valor: Contexto completo o valor específico
    
    Ejemplos:
        obtener_contexto('app')  → 'chrome'
        obtener_contexto()       → {dict completo}
    """
    global _contexto_actual
    
    if tipo:
        return _contexto_actual.get(tipo)
    else:
        return _contexto_actual.copy()

# ============================================
# FUNCIÓN: limpiar_contexto
# ============================================
def limpiar_contexto():
    """
    Limpia el contexto (útil para empezar de cero)
    """
    global _contexto_actual
    
    _contexto_actual = {
        'ultima_app': None,
        'ultima_url': None,
        'ultimo_archivo': None,
        'ultima_accion': None,
        'ultima_busqueda': None,
        'volumen_cambios': 0,
        'ventanas_abiertas': [],
    }
    
    guardar_log("Contexto limpiado", "CONTEXTO")

# ============================================
# FUNCIÓN: generar_resumen_contexto
# ============================================
def generar_resumen_contexto():
    """
    Genera un resumen legible del contexto actual.
    
    Returns:
        str: Resumen del contexto
    """
    global _contexto_actual
    
    resumen = "CONTEXTO ACTUAL:\n"
    
    if _contexto_actual['ultima_app']:
        resumen += f"- Última app: {_contexto_actual['ultima_app']}\n"
    
    if _contexto_actual['ultima_url']:
        resumen += f"- Última URL: {_contexto_actual['ultima_url']}\n"
    
    if _contexto_actual['ultimo_archivo']:
        resumen += f"- Último archivo: {_contexto_actual['ultimo_archivo']}\n"
    
    if _contexto_actual['ultima_busqueda']:
        resumen += f"- Última búsqueda: {_contexto_actual['ultima_busqueda']}\n"
    
    if _contexto_actual['ventanas_abiertas']:
        resumen += f"- Ventanas abiertas: {', '.join(_contexto_actual['ventanas_abiertas'])}\n"
    
    if not any([
        _contexto_actual['ultima_app'],
        _contexto_actual['ultima_url'],
        _contexto_actual['ultimo_archivo'],
        _contexto_actual['ultima_busqueda']
    ]):
        resumen += "- Sin contexto previo\n"
    
    return resumen

# ============================================
# FUNCIÓN: hay_contexto_previo
# ============================================
def hay_contexto_previo():
    """
    Verifica si hay contexto guardado.
    
    Returns:
        bool: True si hay contexto, False si no
    """
    global _contexto_actual
    
    return any([
        _contexto_actual['ultima_app'],
        _contexto_actual['ultima_url'],
        _contexto_actual['ultimo_archivo'],
        _contexto_actual['ultima_busqueda']
    ])


# ============================================
# EXPLICACIÓN DE USO:
# ============================================

"""
📝 CÓMO USAR ESTAS FUNCIONES:

1. CUANDO NEO ABRE UNA APP:
   from neo_memoria import actualizar_contexto
   actualizar_contexto('app', 'chrome')

2. CUANDO NEO BUSCA ALGO:
   actualizar_contexto('busqueda', 'python tutorial')

3. CUANDO NECESITAS EL CONTEXTO:
   from neo_memoria import obtener_contexto
   ultima_app = obtener_contexto('app')
   print(f"Última app: {ultima_app}")

4. PARA VER TODO EL CONTEXTO:
   contexto = obtener_contexto()
   print(contexto)

5. PARA LIMPIAR:
   from neo_memoria import limpiar_contexto
   limpiar_contexto()
"""


# ============================================
# PRUEBA RÁPIDA
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBA DE CONTEXTO")
    print("=" * 60)
    
    # Simular comandos
    print("\n1. Abriendo Chrome...")
    actualizar_contexto('app', 'chrome')
    
    print("\n2. Buscando Python...")
    actualizar_contexto('busqueda', 'python tutorial')
    
    print("\n3. Abriendo Notepad...")
    actualizar_contexto('app', 'notepad')
    
    # Ver contexto
    print("\n" + "=" * 60)
    print("CONTEXTO ACTUAL:")
    print("=" * 60)
    print(generar_resumen_contexto())
    
    # Consultar específico
    print("\n" + "=" * 60)
    print("CONSULTAS ESPECÍFICAS:")
    print("=" * 60)
    print(f"Última app: {obtener_contexto('app')}")
    print(f"Última búsqueda: {obtener_contexto('busqueda')}")
    print(f"Ventanas abiertas: {obtener_contexto('ventanas_abiertas')}")
    
    # Limpiar
    print("\n" + "=" * 60)
    print("LIMPIANDO CONTEXTO...")
    print("=" * 60)
    limpiar_contexto()
    print(generar_resumen_contexto())


if __name__ == "__main__":
    print("NEO - Sistema de Memoria")
    print("\nOpciones:")
    print("1. Ver historial")
    print("2. Limpiar memoria")
    print("3. Limpiar logs")
    
    opcion = input("\n¿Qué hacer? (1/2/3): ").strip()
    
    if opcion == "1":
        mostrar_historial()
    elif opcion == "2":
        limpiar_memoria()
    elif opcion == "3":
        limpiar_logs()