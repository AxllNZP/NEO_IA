@echo off
:: instalar_customtkinter.bat - Instalador de CustomTkinter para NEO GUI

echo ================================================
echo NEO - Instalador de CustomTkinter
echo ================================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Descargalo de: python.org
    pause
    exit /b 1
)

echo [1/3] Python detectado correctamente
echo.

:: Actualizar pip
echo [2/3] Actualizando pip...
python -m pip install --upgrade pip
echo.

:: Instalar CustomTkinter
echo [3/3] Instalando CustomTkinter...
pip install customtkinter
if errorlevel 1 (
    echo ERROR: No se pudo instalar CustomTkinter
    pause
    exit /b 1
)
echo.

:: Instalar dependencias adicionales (darkdetect se instala automáticamente)
echo [3.1/3] Verificando dependencias...
pip install pillow
echo.

echo ================================================
echo Instalacion completada exitosamente
echo ================================================
echo.
echo CustomTkinter instalado correctamente
echo Ahora puedes ejecutar: python neo_gui.py
echo.
pause