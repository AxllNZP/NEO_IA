# 🤖 PROYECTO NEO - Asistente IA Personal tipo Jarvis

## 📌 ¿Qué es NEO?

NEO es tu asistente personal de inteligencia artificial, similar a Jarvis de Iron Man. Puede:

- 👂 **Escucharte** usando reconocimiento de voz (Whisper)
- 🗣️ **Hablarte** con síntesis de voz (pyttsx3)
- 🧠 **Entenderte** con IA local (Ollama + Llama 3.2)
- 🖐️ **Controlar tu PC** automáticamente (PyAutoGUI)
- 👁️ **Ver tu pantalla** y analizarla (Llava)
- 💾 **Recordar** todo lo que haces (sistema de memoria)

**100% GRATIS** • **100% LOCAL** • **100% CÓDIGO ABIERTO**

---

## 🚀 INICIO RÁPIDO

### Para COMENZAR AHORA (3 pasos):

```bash
# 1. Verifica qué te falta
python COMIENZA_AQUI.py

# 2. Ejecuta el verificador
python verificar_neo.py

# 3. Instala lo que falte
python instalador_neo_completo.py
```

### Para LEER TODO (paso a paso):

```bash
python GUIA_COMPLETA.py
```

---

## 📦 ARCHIVOS DEL PROYECTO

### 🔧 Archivos de Ayuda (NUEVOS):
- **COMIENZA_AQUI.py** ← **LEE ESTE PRIMERO**
- **verificar_neo.py** - Verifica qué falta instalar
- **instalador_neo_completo.py** - Instala todo automáticamente
- **GUIA_COMPLETA.py** - Guía detallada paso a paso
- **ANALISIS_PROBLEMAS.py** - Problemas encontrados y soluciones

### 🤖 Módulos Principales:
- **neo_control.py** - Control de PC (teclado/mouse)
- **neo_cerebro.py** - Toma de decisiones con IA
- **neo_voz.py** - Reconocimiento de voz
- **neo_voz_tts.py** - Síntesis de voz
- **neo_memoria.py** - Sistema de memoria
- **neo_gui_integrado.py** - Interfaz gráfica completa
- **capturar_pantalla.py** - Captura y análisis de pantalla

### 🛠️ Instaladores:
- **instalar_customtkinter.bat** - Instala interfaz gráfica
- **instalar_tts.bat** - Instala sistema de voz

### 📊 Datos:
- **neo_memoria.json** - Historial de comandos
- **neo_logs.txt** - Registro de actividad

---

## ⚙️ REQUISITOS

### Software:
- **Python 3.8+** → [Descargar](https://python.org)
- **Ollama** → [Descargar](https://ollama.ai)

### Dependencias Python:
```bash
pip install pyautogui numpy Pillow mss
pip install customtkinter
pip install pyttsx3 pypiwin32
pip install openai-whisper
pip install pyaudio  # Puede necesitar .whl en Windows
```

### Modelos de IA (con Ollama):
```bash
ollama pull llama3.2:3b  # Cerebro (3GB)
ollama pull llava:7b     # Visión (4GB)
```

### Especificaciones mínimas:
- Windows 10/11
- 8GB RAM
- 10GB espacio libre
- Micrófono (para modo voz)

---

## 🔧 INSTALACIÓN

### Opción A: Automática (Recomendada)

```bash
# 1. Clona o descarga el proyecto
# 2. Abre CMD en la carpeta del proyecto
# 3. Ejecuta:

python instalador_neo_completo.py
```

### Opción B: Manual

```bash
# 1. Instala Python 3.8+
# 2. Instala dependencias:
pip install pyautogui numpy Pillow mss customtkinter pyttsx3 pypiwin32 openai-whisper

# 3. Instala Ollama y modelos:
# Descarga Ollama de https://ollama.ai
ollama pull llama3.2:3b
ollama pull llava:7b

# 4. PyAudio (problemático):
# Si falla pip install pyaudio, descarga .whl de:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

---

## 🎮 USO

### Modo Texto (más simple):

```bash
python neo_gui_integrado.py
```

1. Click en **"MODO TEXTO"**
2. Escribe un comando: `abre chrome`
3. Presiona Enter

### Modo Voz (completo):

```bash
python neo_gui_integrado.py
```

1. Click en **"MODO VOZ"**
2. Di: **"neo, abre youtube"**
3. NEO escucha, procesa y ejecuta

### Comandos de Ejemplo:

```
Básicos:
- "abre notepad"
- "abre calculadora"
- "minimiza todo"
- "qué hora es"
- "sube el volumen"

Intermedios:
- "busca python en google"
- "abre youtube"
- "cierra esta ventana"

Avanzados:
- "abre chrome y busca inteligencia artificial"
- "minimiza todo y abre notepad"
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### PyAudio no se instala
```bash
# Descarga .whl de: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Luego instala:
pip install PyAudio-0.2.11-cpXX-cpXX-win_amd64.whl
```

### Ollama no responde
```bash
# Verifica que esté corriendo:
ollama --version

# Reinicia el servicio en Windows:
# Servicios → Ollama → Reiniciar
```

### NEO no escucha
```bash
# Verifica micrófono en Windows
# Ajusta sensibilidad en neo_voz.py línea 17:
SILENCE_THRESHOLD = 400  # Prueba con 300 o 500
```

### GUI no abre
```bash
# Reinstala CustomTkinter:
pip install customtkinter --upgrade

# Verifica que tkinter funcione:
python -m tkinter
```

---

## 📚 ARQUITECTURA

```
NEO Sistema Completo
│
├── 👂 ENTRADA (Voz)
│   ├── neo_voz.py (Whisper)
│   └── Micrófono
│
├── 🧠 PROCESAMIENTO
│   ├── neo_cerebro.py (Llama 3.2)
│   └── Toma de decisiones
│
├── 🖐️ SALIDA (Acciones)
│   ├── neo_control.py (PyAutoGUI)
│   └── Control de PC
│
├── 🗣️ SALIDA (Voz)
│   ├── neo_voz_tts.py (pyttsx3)
│   └── Síntesis de voz
│
├── 👁️ VISIÓN
│   ├── capturar_pantalla.py (Llava)
│   └── Análisis de pantalla
│
├── 💾 MEMORIA
│   ├── neo_memoria.py
│   └── neo_memoria.json
│
└── 🖥️ INTERFAZ
    ├── neo_gui_integrado.py (CustomTkinter)
    └── GUI completa
```

---

## 🚀 PRÓXIMAS MEJORAS

- [ ] Memoria contextual avanzada
- [ ] Análisis continuo de pantalla
- [ ] Comandos personalizados
- [ ] Integración con APIs (Gmail, Calendar, etc.)
- [ ] Soporte multi-idioma
- [ ] Sistema de plugins
- [ ] Modo offline 100%

---

## 📖 DOCUMENTACIÓN

- **COMIENZA_AQUI.py** - Inicio rápido
- **GUIA_COMPLETA.py** - Tutorial completo
- **ANALISIS_PROBLEMAS.py** - Troubleshooting
- Cada archivo .py tiene documentación interna

---

## ⚠️ LIMITACIONES CONOCIDAS

1. **Primera ejecución lenta**: Ollama carga modelos (10-20 seg)
2. **PyAudio complicado**: Puede necesitar .whl en Windows
3. **Modelos grandes**: Necesita 10GB+ espacio
4. **Solo Windows**: Por ahora (Linux/Mac en futuro)

---

## 🤝 CONTRIBUIR

Este es tu proyecto personal de aprendizaje. Siéntete libre de:
- Modificar el código
- Agregar funcionalidades
- Experimentar con diferentes modelos
- Compartir tus mejoras

---

## 📜 LICENCIA

Código abierto para uso educativo y personal.

---

## 💬 SOPORTE

Si algo no funciona:
1. Ejecuta: `python verificar_neo.py`
2. Lee: `ANALISIS_PROBLEMAS.py`
3. Revisa la guía completa: `GUIA_COMPLETA.py`

---

## 🎯 ESTADO DEL PROYECTO

```
✅ Control de PC        - Funcional
✅ TTS (Voz salida)     - Funcional  
✅ Cerebro IA           - Funcional
✅ Memoria              - Funcional
✅ GUI                  - Funcional
⚠️  Reconocimiento voz  - Depende de PyAudio
⚠️  Visión pantalla     - Depende de Ollama
```

---

**Creado con ❤️ para aprender y dominar la IA**

🤖 NEO - Tu asistente personal, 100% tuyo, 100% gratis