@echo off
chcp 65001 >nul
title Biblia Interactiva - por Dsanti (@donpelo)
echo.
echo ========================================
echo     BIBLIA INTERACTIVA v2.0
echo        por Dsanti (@donpelo)
echo ========================================
echo.
echo Ubicado en: C:\BibliaInteractiva
echo GitHub: https://github.com/donpelo/biblia
echo.
powershell -ExecutionPolicy Bypass -File "scripts\BibliaInteractiva.ps1"
pause
