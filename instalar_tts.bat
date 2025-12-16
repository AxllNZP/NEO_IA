@echo off
:: instalar_tts.bat - Instalador automático del sistema TTS para NEO
:: Ejecutar como administrador si es posible

echo ========================================
echo NEO - Instalador del Sistema TTS
echo ========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python desde python.org
    pause
    exit /b 1
)

echo [1/3] Python detectado correctamente
echo.

:: Actualizar pip
echo [2/3] Actualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ADVERTENCIA: No se pudo actualizar pip
    echo Continuando de todas formas...
)
echo.

:: Instalar pyttsx3
echo [3/3] Instalando pyttsx3...
pip install pyttsx3
if errorlevel 1 (
    echo ERROR: No se pudo instalar pyttsx3
    pause
    exit /b 1
)
echo.

:: En Windows, también instalar pypiwin32
echo [3.1/3] Instalando pypiwin32 (solo Windows)...
pip install pypiwin32
if errorlevel 1 (
    echo ADVERTENCIA: pypiwin32 no se instalo
    echo El TTS podria no funcionar correctamente
)
echo.

echo ========================================
echo Instalacion completada exitosamente
echo ========================================
echo.
echo Ahora puedes ejecutar:
echo   python neo_voz_tts.py
echo.
echo Para probar el sistema TTS
echo.
pause