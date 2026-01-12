@echo off
setlocal
cd /d C:\biblia

echo Running Biblia GUI (debug)...
"C:\Program Files\Python310\python.exe" biblia_gui.py
echo.
echo ExitCode=%errorlevel%
echo.
pause
endlocal
