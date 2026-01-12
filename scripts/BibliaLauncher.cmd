@echo off
setlocal
cd /d C:\biblia
if not exist logs mkdir logs
echo START %date% %time% > logs\desktop_run.log
"C:\Program Files\Python310\pythonw.exe" biblia_gui.py 1>>logs\desktop_run.log 2>>&1
echo EXITCODE=%ERRORLEVEL% >> logs\desktop_run.log
echo END %date% %time%  >> logs\desktop_run.log
endlocal
