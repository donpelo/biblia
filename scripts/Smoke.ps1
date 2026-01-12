param(
  [string]$Py = "C:\Program Files\Python310\python.exe",
  [string]$Root = (Resolve-Path .).Path
)

$ErrorActionPreference = "Stop"
Set-Location $Root

# asegurar logs/config
New-Item -ItemType Directory -Force "$Root\logs" | Out-Null
New-Item -ItemType Directory -Force "$Root\config" | Out-Null

# asegurar config template si no existe
if (-not (Test-Path "$Root\config\default.json")) {
@"
{
  "ui_lang": "es",
  "tts_rate": "180",
  "tts_volume": "1.0",
  "tts_voice": ""
}
"@ | Set-Content "$Root\config\default.json" -Encoding UTF8
}

# smoke core + launcher (sin abrir ventanas)
& $Py -m py_compile "$Root\biblia_gui.py"
& $Py -m py_compile "$Root\core\bible_loader.py"
& $Py -m py_compile "$Root\core\bible_reader.py"
& $Py -m py_compile "$Root\core\gui_reader.py"
if ($LASTEXITCODE -ne 0) { throw "py_compile falló" }

& $Py -c "import sys; sys.path.insert(0,r'$Root'); import biblia_gui; print('OK import biblia_gui')"
if ($LASTEXITCODE -ne 0) { throw "import biblia_gui falló" }

& $Py -c "import sys; sys.path.insert(0,r'$Root'); from core.bible_loader import load_bible_version; idx, books = load_bible_version('RV1909-es'); print('OK books', len(books))"
if ($LASTEXITCODE -ne 0) { throw "load_bible_version falló" }

& $Py -c "import json; p=r'$Root\data\devocional_calendar.json'; json.load(open(p,'r',encoding='utf-8-sig')); print('OK calendar utf-8-sig')"
if ($LASTEXITCODE -ne 0) { throw "calendar parse falló" }

"OK: smoke ok" | Out-Host
