@echo off
chcp 65001 >nul
cd /d C:\biblia
powershell -NoProfile -ExecutionPolicy Bypass -File "scripts\BibliaInteractiva.ps1"
exit
