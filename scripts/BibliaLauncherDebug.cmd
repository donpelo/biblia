@echo off
set ROOT=%~dp0..
cd /d "C:\biblia"
echo START %date% %time%>> "C:\biblia\logs\desktop_debug.log"
py -3.11 "C:\biblia\biblia_gui.py" >> "C:\biblia\logs\desktop_debug.log" 2>&1
echo EXITCODE=%ERRORLEVEL%>> "C:\biblia\logs\desktop_debug.log"
echo END %date% %time%>> "C:\biblia\logs\desktop_debug.log"
pause

