@echo off
set ROOT=%~dp0..
cd /d "C:\biblia"
py -3.11 "C:\biblia\biblia_gui.py" >> "C:\biblia\logs\desktop_run.log" 2>&1

