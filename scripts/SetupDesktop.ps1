param(
  [string]$Root = (Resolve-Path .).Path,
  [string]$Py = "C:\Program Files\Python310\python.exe",
  [string]$Name = "Biblia Interactiva"
)

$ErrorActionPreference = "Stop"
Set-Location $Root

New-Item -ItemType Directory -Force "$Root\logs" | Out-Null
New-Item -ItemType Directory -Force "$Root\config" | Out-Null

# Crear .cmd para escritorio (sin depender de powershell policy)
$cmd = @"
@echo off
set ROOT=%~dp0..
cd /d "$Root"
"$Py" "$Root\biblia_gui.py" >> "$Root\logs\desktop_run.log" 2>&1
"@
$cmdPath = Join-Path $Root "scripts\BibliaLauncher.cmd"
$cmd | Set-Content $cmdPath -Encoding ASCII

# Crear acceso directo en escritorio
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desktop "$Name.lnk"

$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($lnk)
$sc.TargetPath = $cmdPath
$sc.WorkingDirectory = $Root
$sc.IconLocation = "$Root\assets\app.ico"
if (-not (Test-Path "$Root\assets\app.ico")) { $sc.IconLocation = "$Root\biblia_gui.py" }
$sc.Save()

"OK: acceso directo creado: $lnk" | Out-Host
"OK: cmd target: $cmdPath" | Out-Host
