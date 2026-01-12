@echo off
setlocal enabledelayedexpansion

rem Root del proyecto (carpeta padre de scripts)
set ROOT=%~dp0..
cd /d "%ROOT%"

set PY=C:\Program Files\Python310\pythonw.exe

rem Logs
if not exist "logs" mkdir "logs"
set RUNLOG=logs\desktop_run.log
set APPLOG=logs\desktop_app.log

echo START %date% %time%>> "%RUNLOG%"

rem Ejecuta GUI sin consola, captura stderr en APPLOG
"%PY%" "%ROOT%\biblia_gui.py" 1>> "%APPLOG%" 2>>&1
set EC=%ERRORLEVEL%

echo EXITCODE=!EC!>> "%RUNLOG%"
echo END %date% %time%>> "%RUNLOG%"
exit /b !EC!
