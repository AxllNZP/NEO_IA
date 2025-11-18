# neo_cerebro.py - Sistema de decisiones inteligente de NEO
import subprocess
import json
import re
from datetime import datetime

print("=" * 60)
print("NEO - Sistema de Decisiones v1.0")
print("=" * 60)

MODELO_CEREBRO = "llama3.2:3b"

FUNCIONES_DISPONIBLES = """
FUNCIONES QUE PUEDES EJECUTAR:

PROGRAMAS:
- abrir_chrome()
- abrir_notepad()
- abrir_calculadora()
- abrir_explorador_archivos()
- abrir_programa('nombre')
- abrir_cmd()
- abrir_configuracion()

WEB:
- buscar_en_google('query')
- abrir_url('url')
- abrir_youtube('busqueda')

VENTANAS:
- minimizar_todo()
- cerrar_ventana_actual()
- cambiar_ventana()
- maximizar_ventana()
- minimizar_ventana()
- ventana_izquierda()
- ventana_derecha()

ESCRITURA:
- escribir_texto('texto')
- copiar()
- pegar()
- guardar()
- deshacer()
- seleccionar_todo()
- presionar_enter()

ARCHIVOS:
- abrir_carpeta('nombre')
- crear_nota_rapida('texto')

MULTIMEDIA:
- volumen_subir(veces)
- volumen_bajar(veces)
- volumen_silenciar()
- tomar_captura()

SISTEMA:
- esperar(segundos)
"""

def detectar_comando_especial(comando):
    comando_lower = comando.lower()
    
    if any(palabra in comando_lower for palabra in ['qué hora', 'que hora', 'hora es']):
        hora_actual = datetime.now().strftime("%H:%M")
        return {
            "acciones": [],
            "explicacion": f"Son las {hora_actual}",
            "respuesta_directa": True
        }
    
    if comando_lower.startswith('abre '):
        programa = comando[5:].strip()
        return {
            "acciones": [
                {"funcion": "abrir_programa", "args": [programa]}
            ],
            "explicacion": f"Abriendo {programa}"
        }
    
    if comando_lower.startswith('busca '):
        query = comando[6:].strip()
        return {
            "acciones": [
                {"funcion": "buscar_en_google", "args": [query]}
            ],
            "explicacion": f"Buscando: {query}"
        }
    
    if 'cierra' in comando_lower or 'cerrar' in comando_lower:
        if 'todo' in comando_lower:
            return {
                "acciones": [
                    {"funcion": "minimizar_todo", "args": []}
                ],
                "explicacion": "Minimizando todas las ventanas"
            }
        else:
            return {
                "acciones": [
                    {"funcion": "cerrar_ventana_actual", "args": []}
                ],
                "explicacion": "Cerrando ventana actual"
            }
    
    if 'volumen' in comando_lower or 'sonido' in comando_lower:
        if 'sube' in comando_lower or 'subir' in comando_lower or 'aumenta' in comando_lower:
            numeros = re.findall(r'\d+', comando)
            veces = int(numeros[0]) if numeros else 3
            return {
                "acciones": [
                    {"funcion": "volumen_subir", "args": [veces]}
                ],
                "explicacion": f"Subiendo volumen {veces} veces"
            }
        elif 'baja' in comando_lower or 'bajar' in comando_lower or 'disminuye' in comando_lower:
            numeros = re.findall(r'\d+', comando)
            veces = int(numeros[0]) if numeros else 3
            return {
                "acciones": [
                    {"funcion": "volumen_bajar", "args": [veces]}
                ],
                "explicacion": f"Bajando volumen {veces} veces"
            }
        elif 'silencia' in comando_lower or 'mutea' in comando_lower or 'silencio' in comando_lower:
            return {
                "acciones": [
                    {"funcion": "volumen_silenciar", "args": []}
                ],
                "explicacion": "Silenciando/activando volumen"
            }
    
    return None

def validar_plan(plan):
    if not isinstance(plan, dict):
        print(" El plan no es un diccionario")
        return False
    
    if 'acciones' not in plan:
        print(" El plan no tiene campo 'acciones'")
        return False
    
    acciones = plan['acciones']
    
    if not isinstance(acciones, list):
        print(" 'acciones' no es una lista")
        return False
    
    funciones_validas = [
        'abrir_chrome', 'abrir_notepad', 'abrir_calculadora',
        'abrir_explorador_archivos', 'abrir_programa', 'abrir_cmd',
        'abrir_configuracion',
        'buscar_en_google', 'abrir_url', 'abrir_youtube',
        'minimizar_todo', 'cerrar_ventana_actual', 'cambiar_ventana',
        'maximizar_ventana', 'minimizar_ventana',
        'ventana_izquierda', 'ventana_derecha',
        'escribir_texto', 'copiar', 'pegar', 'guardar', 'deshacer',
        'seleccionar_todo', 'presionar_enter',
        'abrir_carpeta', 'crear_nota_rapida',
        'volumen_subir', 'volumen_bajar', 'volumen_silenciar',
        'tomar_captura', 'esperar'
    ]
    
    for i, accion in enumerate(acciones):
        if 'funcion' not in accion:
            print(f" Acción {i+1} no tiene campo 'funcion'")
            return False
        
        funcion = accion['funcion']
        
        if funcion not in funciones_validas:
            print(f" Función '{funcion}' no es válida")
            return False
        
        if 'args' not in accion:
            print(f" Acción {i+1} no tiene campo 'args'")
            return False
        
        if not isinstance(accion['args'], list):
            print(f" 'args' de acción {i+1} no es una lista")
            return False
    
    return True

def extraer_json(texto):
    try:
        return json.loads(texto)
    except:
        pass
    
    match = re.search(r'\{[^}]*"acciones"[^}]*\[[^\]]*\][^}]*\}', texto, re.DOTALL)
    
    if match:
        json_str = match.group(0)
        
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        open_brackets = json_str.count('[')
        close_brackets = json_str.count(']')
        
        if open_brackets > close_brackets:
            json_str += ']' * (open_brackets - close_brackets)
        if open_braces > close_braces:
            json_str += '}' * (open_braces - close_braces)
        
        if '"explicacion"' not in json_str:
            json_str = json_str[:-1] + ', "explicacion": "Ejecutando comando"}'
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    return None

def procesar_comando(comando_voz, contexto_pantalla=""):
    print(f"\nAnalizando comando: '{comando_voz}'")
    
    plan_especial = detectar_comando_especial(comando_voz)
    if plan_especial:
        print("Comando especial detectado (respuesta rápida)")
        return plan_especial
    
    print("Comando complejo, consultando a Llama...")
    
    prompt = f"""Eres NEO, un asistente de voz inteligente para Windows.

Tu tarea: Analizar el comando del usuario y decidir qué funciones ejecutar.

COMANDO DEL USUARIO:
"{comando_voz}"
"""
    
    if contexto_pantalla:
        prompt += f"""

CONTEXTO (lo que ves en la pantalla):
{contexto_pantalla}

Usa este contexto para tomar mejores decisiones.
"""
    
    prompt += f"""
{FUNCIONES_DISPONIBLES}

IMPORTANTE: Responde SOLO con JSON en este formato exacto:
{{"acciones": [{{"funcion": "nombre", "args": []}}], "explicacion": "texto"}}

NO agregues texto antes o después del JSON.
SIEMPRE incluye el campo "explicacion".
SIEMPRE cierra todas las llaves y corchetes.

EJEMPLOS VÁLIDOS:

Comando: "abre chrome"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}], "explicacion": "Abriendo Chrome"}}

Comando: "busca python"
{{"acciones": [{{"funcion": "abrir_chrome", "args": []}}, {{"funcion": "esperar", "args": [2]}}, {{"funcion": "buscar_en_google", "args": ["python"]}}], "explicacion": "Buscando python en Google"}}

Ahora procesa: "{comando_voz}"
Responde SOLO con el JSON:"""
    
    print(" Consultando con Llama... (10-15 segundos)")
    
    try:
        result = subprocess.run(
            ["ollama", "run", MODELO_CEREBRO],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30
        )
        
        respuesta = result.stdout.strip()
        print(f"Respuesta recibida ({len(respuesta)} caracteres)")
        
        plan = extraer_json(respuesta)
        
        if plan and validar_plan(plan):
            explicacion = plan.get('explicacion', 'Sin explicación')
            num_acciones = len(plan.get('acciones', []))
            
            print("\nPlan de acción generado:")
            print(f"  {explicacion}")
            print(f"{num_acciones} acción(es) a ejecutar")
            return plan
        else:
            print(" No se pudo generar un plan válido")
            return None
            
    except subprocess.TimeoutExpired:
        print("Timeout: Llama tardó demasiado")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def ejecutar_plan(plan):
    if not plan or 'acciones' not in plan:
        print("Plan inválido")
        return False
    
    acciones = plan['acciones']
    total = len(acciones)
    
    if total == 0:
        if 'explicacion' in plan:
            print(f"\n {plan['explicacion']}")
        return True
    
    print(f"\nEjecutando {total} acción(es)...\n")
    
    try:
        import neo_control
    except ImportError:
        print("Error: neo_control.py no encontrado")
        return False
    
    for i, accion in enumerate(acciones, 1):
        funcion = accion.get('funcion', '')
        args = accion.get('args', [])
        
        print(f"[{i}/{total}] {funcion}({', '.join(map(str, args))})")
        
        if args:
            args_str = ', '.join([
                f"'{arg}'" if isinstance(arg, str) else str(arg) 
                for arg in args
            ])
            comando = f"{funcion}({args_str})"
        else:
            comando = f"{funcion}()"
        
        try:
            eval(f"neo_control.{comando}")
            print(f"  Completado\n")
        except AttributeError:
            print(f"  Error: Función '{funcion}' no existe\n")
            return False
        except Exception as e:
            print(f"  Error: {e}\n")
            return False
    
    print(" Todas las acciones completadas")
    return True

def probar_cerebro():
    print("\n" + "=" * 60)
    print("MODO DE PRUEBA - Prueba el cerebro de NEO")
    print("=" * 60)
    
    ejemplos = [
        "abre chrome",
        "busca python tutorial en google",
        "abre notepad",
        "minimiza todo",
        "sube el volumen 5 veces",
        "qué hora es",
    ]
    
    print("\nEjemplos de comandos (escribe el comando, NO el número):")
    for i, ej in enumerate(ejemplos, 1):
        print(f"  {i}. {ej}")
    
    print("\n IMPORTANTE: Escribe el COMANDO completo, no el número")
    print("    Ejemplo: en vez de '1', escribe 'abre chrome'\n")
    
    while True:
        print("-" * 60)
        comando = input("\n Tu comando (o 'salir'): ").strip()
        
        if comando.lower() in ['salir', 'exit', 'quit', 'adios']:
            print(" ¡Hasta luego!")
            break
        
        if not comando:
            print(" Comando vacío")
            continue
        
        if comando.isdigit():
            print(" No escribas el número, escribe el comando completo")
            print(f"    Ejemplo: en vez de '{comando}', escribe '{ejemplos[int(comando)-1] if int(comando) <= len(ejemplos) else ejemplos[0]}'")
            continue
        
        plan = procesar_comando(comando)
        
        if plan:
            print("\n¿Ejecutar? (si/no/ver): ", end='')
            confirmar = input().strip().lower()
            
            if confirmar == 'ver':
                print("\nPlan completo:")
                print(json.dumps(plan, indent=2, ensure_ascii=False))
                print("\n¿Ejecutar ahora? (si/no): ", end='')
                confirmar = input().strip().lower()
            
            if confirmar == 'si':
                ejecutar_plan(plan)
            else:
                print("Cancelado")
        else:
            print(" No se pudo generar plan")

if __name__ == "__main__":
    print("\nSistema de decisiones cargado")
    print("\nEste es el 'cerebro' de NEO\n")
    
    print("Modos disponibles:")
    print("  1. Modo prueba (probar comandos)")
    print("  2. Solo cargar módulo")
    
    modo = input("\n¿Qué modo? (1/2): ").strip()
    
    if modo == "1":
        probar_cerebro()
    else:
        print("\nMódulo listo para importar")