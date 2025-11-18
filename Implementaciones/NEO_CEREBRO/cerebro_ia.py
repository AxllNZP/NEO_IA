# cerebro_ia.py - Sistema de decisiones inteligente
import subprocess
import json
import re

print("=" * 60)
print("CEREBRO DE IA - Sistema de Decisiones")
print("=" * 60)

# ==========================================
# FUNCIONES DISPONIBLES
# ==========================================

FUNCIONES_DISPONIBLES = """
Funciones que puedes usar:

PROGRAMAS:
- abrir_chrome()
- abrir_notepad()
- abrir_calculadora()
- abrir_explorador()

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

# ==========================================
# FUNCIÓN: PROCESAR COMANDO
# ==========================================

def procesar_comando(comando):
    """
    Recibe un comando en lenguaje natural y genera plan de acción
    
    Args:
        comando (str): Lo que dijo el usuario
        
    Returns:
        dict: Plan con acciones a ejecutar
    """
    print(f"\nAnalizando: '{comando}'")
    print("Pensando... (10-15 segundos)\n")
    
    # prompt para Llama
    prompt = f"""Eres un asistente IA que convierte comandos en acciones.

COMANDO DEL USUARIO:
"{comando}"

{FUNCIONES_DISPONIBLES}

Tu tarea: Generar un plan de acciones en JSON.

FORMATO EXACTO (solo JSON, nada más):
{{
  "acciones": [
    {{"funcion": "nombre_funcion", "args": []}},
    {{"funcion": "otra_funcion", "args": ["argumento"]}}
  ],
  "explicacion": "Breve descripción de lo que harás"
}}

EJEMPLOS:

Comando: "abre chrome"
{{
  "acciones": [
    {{"funcion": "abrir_chrome", "args": []}}
  ],
  "explicacion": "Abriendo Chrome"
}}

Comando: "minimiza todo y abre la calculadora"
{{
  "acciones": [
    {{"funcion": "minimizar_todo", "args": []}},
    {{"funcion": "esperar", "args": [1]}},
    {{"funcion": "abrir_calculadora", "args": []}}
  ],
  "explicacion": "Minimizando ventanas y abriendo calculadora"
}}

Comando: "sube el volumen 5 veces"
{{
  "acciones": [
    {{"funcion": "volumen_subir", "args": [5]}}
  ],
  "explicacion": "Subiendo volumen 5 veces"
}}

Ahora procesa: "{comando}"
Responde SOLO con el JSON:"""
    
    # Ejecutar Llama
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
        print(f"Respuesta recibida")
        
        # Extraer JSON
        plan = extraer_json(respuesta)
        
        if plan:
            print("\nPlan generado:")
            print(f"   {plan.get('explicacion', 'Sin explicación')}")
            print(f"   {len(plan.get('acciones', []))} acciones")
            return plan
        else:
            print("No se pudo generar plan")
            return None
            
    except subprocess.TimeoutExpired:
        print("Timeout: Llama tardó demasiado")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# ==========================================
# FUNCIÓN: EXTRAER JSON
# ==========================================

def extraer_json(texto):
    """Extrae y limpia el JSON de la respuesta"""
    try:
        # Intentar parsear directamente
        return json.loads(texto)
    except:
        pass
    
    # Buscar JSON con regex
    match = re.search(r'\{.*\}', texto, re.DOTALL)
    if match:
        json_str = match.group(0)
        
        # Reparar JSON incompleto
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        
        if open_braces > close_braces:
            json_str += '}' * (open_braces - close_braces)
        
        try:
            return json.loads(json_str)
        except:
            pass
    
    print(f"No se encontró JSON válido")
    return None

# ==========================================
# FUNCIÓN: VALIDAR PLAN
# ==========================================

def validar_plan(plan):
    """Verifica que el plan sea seguro"""
    if not plan or 'acciones' not in plan:
        return False
    
    funciones_validas = [
        'abrir_chrome', 'abrir_notepad', 'abrir_calculadora', 
        'abrir_explorador', 'minimizar_todo', 'cerrar_ventana',
        'escribir_texto', 'volumen_subir', 'volumen_bajar', 'esperar',
    ]
    
    for accion in plan['acciones']:
        if accion.get('funcion') not in funciones_validas:
            print(f"Función '{accion.get('funcion')}' no válida")
            return False
    
    return True

# ==========================================
# FUNCIÓN: MOSTRAR PLAN
# ==========================================

def mostrar_plan(plan):
    """Muestra el plan de forma legible"""
    print("\n" + "=" * 60)
    print("PLAN DE ACCIÓN")
    print("=" * 60)
    
    print(f"\nExplicación: {plan.get('explicacion', 'N/A')}")
    
    print(f"\nAcciones ({len(plan['acciones'])}):")
    for i, accion in enumerate(plan['acciones'], 1):
        funcion = accion.get('funcion', 'N/A')
        args = accion.get('args', [])
        
        if args:
            args_str = ', '.join([f"'{a}'" if isinstance(a, str) else str(a) for a in args])
            print(f"   [{i}] {funcion}({args_str})")
        else:
            print(f"   [{i}] {funcion}()")
    
    print("\n" + "=" * 60)

# ==========================================
# PROGRAMA PRINCIPAL - MODO PRUEBA
# ==========================================

if __name__ == "__main__":
    print("\nModo de prueba del cerebro")
    print("   Escribe comandos para ver qué plan genera\n")
    
    ejemplos = [
        "abre chrome",
        "minimiza todo y abre calculadora",
        "abre notepad y escribe hola mundo",
        "sube el volumen 3 veces",
    ]
    
    print("Ejemplos de comandos:")
    for i, ej in enumerate(ejemplos, 1):
        print(f"   {i}. {ej}")
    
    while True:
        print("\n" + "-" * 60)
        comando = input("\nTu comando (o 'salir'): ").strip()
        
        if comando.lower() in ['salir', 'exit']:
            print("Saliendo del modo de prueba...")
            break
        
        if not comando:
            continue
        
        # Procesar comando
        plan = procesar_comando(comando)
        
        if plan and validar_plan(plan):
            # Mostrar plan en formato legible
            mostrar_plan(plan)
            
            # Mostrar JSON completo
            print("\nJSON completo:")
            print(json.dumps(plan, indent=2, ensure_ascii=False))
        else:
            print("No se pudo generar un plan válido")