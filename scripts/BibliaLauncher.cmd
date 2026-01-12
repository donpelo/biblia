@echo off
set ROOT=%~dp0..
cd /d "C:\biblia"
"C:\Program Files\Python310\python.exe" "C:\biblia\biblia_gui.py" >> "C:\biblia\logs\desktop_run.log" 2>&1
