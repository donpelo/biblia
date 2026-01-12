@echo off
setlocal enabledelayedexpansion

set ROOT=%~dp0..
cd /d "%ROOT%"

set PY=C:\Program Files\Python310\python.exe

if not exist "logs" mkdir "logs"
set APPLOG=logs\desktop_debug.log

echo START %date% %time%>> "%APPLOG%"
"%PY%" "%ROOT%\biblia_gui.py"
set EC=%ERRORLEVEL%
echo EXITCODE=!EC!>> "%APPLOG%"
echo END %date% %time%>> "%APPLOG%"

echo.
echo Log:
type "%APPLOG%"
echo.
pause
exit /b !EC!
