# neo_memoria.py - Sistema de memoria para NEO
import json
import os
from datetime import datetime

ARCHIVO_MEMORIA = "neo_memoria.json"

def guardar_interaccion(comando, respuesta):
    """
    Guarda una interacción en la memoria
    
    Args:
        comando (str): Lo que dijiste
        respuesta (str): Lo que NEO respondió
    """
    # Cargar memoria existente
    memoria = cargar_memoria()
    
    # Agregar nueva interacción
    memoria.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "comando": comando,
        "respuesta": respuesta
    })
    
    # Mantener solo últimas 50 interacciones
    if len(memoria) > 50:
        memoria = memoria[-50:]
    
    # Guardar
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

def obtener_contexto():
    """
    Obtiene las últimas 3 interacciones para contexto
    
    Returns:
        str: Resumen del contexto
    """
    memoria = cargar_memoria()
    
    if not memoria:
        return ""
    
    # Últimas 3 interacciones
    recientes = memoria[-3:]
    
    contexto = "Conversación reciente:\n"
    for item in recientes:
        contexto += f"- Usuario: {item['comando']}\n"
        contexto += f"  NEO: {item['respuesta']}\n"
    
    return contexto

def limpiar_memoria():
    """Borra toda la memoria"""
    if os.path.exists(ARCHIVO_MEMORIA):
        os.remove(ARCHIVO_MEMORIA)
    print("✓ Memoria limpiada")

# Prueba
if __name__ == "__main__":
    print("Probando memoria...")
    guardar_interaccion("abre chrome", "Abriendo Chrome")
    guardar_interaccion("busca python", "Buscando Python")
    print(obtener_contexto())
    print("✓ Memoria funciona")