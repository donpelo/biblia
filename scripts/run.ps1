param([string]$Root="C:\BibliaInteractiva")
$env:VIRTUAL_ENV="$Root\venv"
$env:PATH="$Root\venv\Scripts;$env:PATH"
python "$Root\gui\main.py"
