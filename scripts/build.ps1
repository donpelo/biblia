param([string]$Root="C:\BibliaInteractiva")
$env:VIRTUAL_ENV="$Root\venv"
$env:PATH="$Root\venv\Scripts;$env:PATH"
pyinstaller --noconfirm --onefile --name BibliaInteractiva "$Root\gui\main.py"
