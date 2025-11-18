# neo_voz.py - Sistema de voz para NEO
import pyttsx3

# Configuración global
engine = None

def inicializar_voz():
    """Inicializa el motor de voz una sola vez"""
    global engine
    
    if engine is None:
        engine = pyttsx3.init()
        
        # Configurar velocidad (150 = normal, 200 = rápido)
        engine.setProperty('rate', 160)
        
        # Configurar volumen (0.0 a 1.0)
        engine.setProperty('volume', 0.9)
        
        # Intentar usar voz en español (si está disponible)
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
    
    return engine

def neo_hablar(texto, esperar=True):
    """
    NEO habla el texto dado
    
    Args:
        texto (str): Lo que NEO dirá
        esperar (bool): Si True, espera a que termine de hablar
    
    Ejemplo:
        neo_hablar("Hola, soy NEO")
    """
    engine = inicializar_voz()
    
    # Limpiar texto (quitar emojis que causan problemas)
    texto_limpio = texto.replace('✓', '').replace('✅', '').replace('🎯', '')
    
    engine.say(texto_limpio)
    
    if esperar:
        engine.runAndWait()

def neo_hablar_async(texto):
    """NEO habla sin bloquear (continúa ejecutando código)"""
    neo_hablar(texto, esperar=False)

# Prueba rápida
if __name__ == "__main__":
    print("Probando voz de NEO...")
    neo_hablar("Hola, soy NEO. Aqui para servirte")
    print("✓ Prueba completada")