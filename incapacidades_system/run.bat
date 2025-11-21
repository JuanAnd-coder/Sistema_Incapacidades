@echo off
echo ========================================
echo Sistema de Gestión de Incapacidades
echo ========================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Ejecutar aplicación
echo Iniciando servidor Flask...
echo.
echo La aplicación estará disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
echo.
python app.py

pause

