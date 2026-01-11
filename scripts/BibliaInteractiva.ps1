$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path $ROOT)) { throw "ROOT no existe: $ROOT" }
Set-Location $ROOT

$PY  = "C:\Program Files\Python310\python.exe"
$PYW = "C:\Program Files\Python310\pythonw.exe"

if (-not (Test-Path $PY))  { throw "No existe python.exe: $PY" }
if (-not (Test-Path $PYW)) { throw "No existe pythonw.exe: $PYW" }

$GUI = Join-Path $ROOT "biblia_gui.py"
if (-not (Test-Path $GUI)) { throw "No existe biblia_gui.py en $ROOT" }

Start-Process -FilePath $PYW -WorkingDirectory $ROOT -ArgumentList @($GUI) | Out-Null
