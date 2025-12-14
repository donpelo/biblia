#requires -Version 5.1
<#
.SYNOPSIS
  Actualiza dependencias Python y descarga biblias en inglés y español en formato JSON.
#>

# Ruta base del proyecto
$Base = "C:\BibliaInteractiva"
$Versions = Join-Path $Base "data\versions"
if (-not (Test-Path $Versions)) { New-Item -ItemType Directory -Path $Versions | Out-Null }

Write-Host "=== Actualizando librerías Python ===" -ForegroundColor Cyan
pip install --upgrade -r (Join-Path $Base "requirements.txt")

Write-Host "=== Descargando biblias en español e inglés ===" -ForegroundColor Cyan

# Ejemplos de fuentes públicas (puedes cambiarlas por otras URLs de GitHub/SourceForge)
$urls = @{
  "RV1909-es.json" = "https://raw.githubusercontent.com/psdann/biblias-espanol-json/master/rv_1909.json"
  "RVA-es.json"    = "https://raw.githubusercontent.com/psdann/biblias-espanol-json/master/rv_1858.json"
  "KJV-en.json"    = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/kjv.json"
  "ASV-en.json"    = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/asv.json"
}

foreach ($file in $urls.Keys) {
  $dest = Join-Path $Versions $file
  try {
    Invoke-WebRequest -Uri $urls[$file] -OutFile $dest -UseBasicParsing
    Write-Host "✓ Descargado: $file" -ForegroundColor Green
  } catch {
    Write-Host "⚠ Error al descargar $file: $($_.Exception.Message)" -ForegroundColor Yellow
  }
}

Write-Host "`nTodo listo. Las biblias están en $Versions" -ForegroundColor Cyan
