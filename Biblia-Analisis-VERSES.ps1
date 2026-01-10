Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Base = Split-Path -Parent $MyInvocation.MyCommand.Path

# Audio (si existe)
try { Import-Module (Join-Path $Base "modules\Audio.psm1") -Force } catch {}
try { Import-Module (Join-Path $Base "modules\AudioBridge.psm1") -Force } catch {}

function SpeakIfAvailable {
  param([string]$Text)
  try { Speak-Passage -Text $Text -Async } catch {}
}

# VersionsPath fijo para tu caso (ya lo detectaste)
$VersionsPath = Join-Path $Base "data\versions"
if (-not (Test-Path $VersionsPath)) { throw "No existe: $VersionsPath" }

Write-Host ("Usando VersionsPath: {0}" -f $VersionsPath) -ForegroundColor Cyan

function Load-Version {
  param([Parameter(Mandatory=$true)][string]$Path)

  $json = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
  $obj = $json | ConvertFrom-Json

  if (-not ($obj.PSObject.Properties.Name -contains "verses")) {
    throw ("El archivo no tiene propiedad 'verses': {0}" -f $Path)
  }

  # Normalizar a array
  $verses = $obj.verses
  if ($null -eq $verses) { $verses = @() }

  return [PSCustomObject]@{
    Metadata = if ($obj.PSObject.Properties.Name -contains "metadata") { $obj.metadata } else { $null }
    Verses   = $verses
  }
}

# Cargar versiones
$bibles = @()
Get-ChildItem -LiteralPath $VersionsPath -Filter *.json -File | ForEach-Object {
  $name = $_.BaseName
  try {
    $data = Load-Version -Path $_.FullName
    $bibles += [PSCustomObject]@{ Version = $name; Data = $data; Path = $_.FullName }
    Write-Host ("Cargada version: {0}" -f $name) -ForegroundColor Green
  } catch {
    Write-Host ("Saltando {0}: {1}" -f $name, $_.Exception.Message) -ForegroundColor Yellow
  }
}

if ($bibles.Count -eq 0) { throw "No se pudo cargar ninguna version." }

# Sacar lista de libros reales desde verses.book
$books = $bibles[0].Data.Verses | Select-Object -ExpandProperty book -ErrorAction SilentlyContinue |
  Where-Object { $_ } | Select-Object -Unique

Write-Host ""
Write-Host "Ejemplos de libros detectados (reales):" -ForegroundColor Cyan
$books | Select-Object -First 30 | ForEach-Object { Write-Host ("- {0}" -f $_) }

Write-Host ""
$book = Read-Host "Libro (copia uno de arriba tal cual)"
$chapter = [int](Read-Host "Capitulo (ej: 3)")
$verse = [int](Read-Host "Versiculo (ej: 16)")

Write-Host ""
Write-Host ("=== Comparacion {0} {1}:{2} ===" -f $book, $chapter, $verse) -ForegroundColor Cyan

$spoken = $false

foreach ($b in $bibles) {
  $row = $b.Data.Verses | Where-Object {
    $_.book -eq $book -and [int]$_.chapter -eq $chapter -and [int]$_.verse -eq $verse
  } | Select-Object -First 1

  if ($row -and $row.text) {
    $line = ("{0}: {1}" -f $b.Version, [string]$row.text)
    Write-Host $line -ForegroundColor Green

    if (-not $spoken) {
      SpeakIfAvailable ($b.Version + ". " + [string]$row.text)
      $spoken = $true
    }
  } else {
    Write-Host ("{0}: (no encontrado)" -f $b.Version) -ForegroundColor Yellow
  }
}

Write-Host ""
Write-Host "Analisis completado." -ForegroundColor Cyan
