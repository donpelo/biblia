@echo off
setlocal
cd /d C:\biblia
if not exist logs mkdir logs
echo START %date% %time% > logs\desktop_debug.log
"C:\Program Files\Python310\python.exe" -u biblia_gui.py 1>>logs\desktop_debug.log 2>>&1
echo EXITCODE=%ERRORLEVEL% >> logs\desktop_debug.log
echo END %date% %time%  >> logs\desktop_debug.log
echo.
echo === tail logs\desktop_debug.log ===
powershell -NoProfile -Command "Get-Content -Tail 80 .\logs\desktop_debug.log"
echo.
pause
endlocal
