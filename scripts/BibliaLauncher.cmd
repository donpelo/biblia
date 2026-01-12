@echo off
setlocal
cd /d C:\biblia

if not exist logs mkdir logs

set TS=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo [%date% %time%] START desktop launcher > logs\desktop_run.log
"C:\Program Files\Python310\pythonw.exe" biblia_gui.py 1>>logs\desktop_run.log 2>>&1
echo [%date% %time%] EXITCODE=%errorlevel% >> logs\desktop_run.log
endlocal
