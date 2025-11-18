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