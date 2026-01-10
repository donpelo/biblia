Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Base = Split-Path -Parent $MyInvocation.MyCommand.Path

# Audio
try { Import-Module (Join-Path $Base "modules\Audio.psm1") -Force } catch {}
try { Import-Module (Join-Path $Base "modules\AudioBridge.psm1") -Force } catch {}
function SpeakIfAvailable { param([string]$Text) try { Speak-Passage -Text $Text -Async } catch {} }

$VersionsPath = Join-Path $Base "data\versions"
if (-not (Test-Path $VersionsPath)) { throw "No existe: $VersionsPath" }

function Load-Version {
  param([Parameter(Mandatory=$true)][string]$Path)
  $json = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
  $obj = $json | ConvertFrom-Json
  if (-not ($obj.PSObject.Properties.Name -contains "verses")) { throw "Sin 'verses': $Path" }

  [PSCustomObject]@{
    Metadata = if ($obj.PSObject.Properties.Name -contains "metadata") { $obj.metadata } else { $null }
    Verses   = $obj.verses
  }
}

# Cargar versiones
$bibles = @()
Get-ChildItem -LiteralPath $VersionsPath -Filter *.json -File | ForEach-Object {
  $name = $_.BaseName
  $data = Load-Version $_.FullName
  $bibles += [PSCustomObject]@{ Version = $name; Data = $data; Path = $_.FullName }
}

Write-Host "Versiones disponibles:" -ForegroundColor Cyan
for ($i=0; $i -lt $bibles.Count; $i++) {
  Write-Host ("[{0}] {1}" -f $i, $bibles[$i].Version)
}

$readIndex = [int](Read-Host "Que version quieres leer en voz alta (indice, ej 0)")
$audioOn = (Read-Host "Audio ON? (1=si, 0=no)") -eq "1"

# Libros detectados por ID numerico
$books = $bibles[0].Data.Verses | Select-Object -ExpandProperty book | Where-Object { $_ } | Select-Object -Unique

Write-Host ""
Write-Host "Libros detectados por ID:" -ForegroundColor Cyan
$books | Sort-Object {[int]$_} | ForEach-Object { Write-Host ("- {0}" -f $_) }

Write-Host ""
$book = Read-Host "Libro ID (ej 40)"
$chapter = [int](Read-Host "Capitulo (ej 3)")
$verse = [int](Read-Host "Versiculo (ej 16)")

Write-Host ""
Write-Host ("=== Comparacion {0} {1}:{2} ===" -f $book, $chapter, $verse) -ForegroundColor Cyan

$toSpeak = $null

foreach ($b in $bibles) {
  $row = $b.Data.Verses | Where-Object {
    $_.book -eq $book -and [int]$_.chapter -eq $chapter -and [int]$_.verse -eq $verse
  } | Select-Object -First 1

  if ($row -and $row.text) {
    Write-Host ("{0}: {1}" -f $b.Version, [string]$row.text) -ForegroundColor Green
    if ($b.Version -eq $bibles[$readIndex].Version) { $toSpeak = [string]$row.text }
  } else {
    Write-Host ("{0}: (no encontrado)" -f $b.Version) -ForegroundColor Yellow
  }
}

if ($audioOn -and $toSpeak) {
  SpeakIfAvailable ($bibles[$readIndex].Version + ". " + $toSpeak)
}

Write-Host ""
Write-Host "Listo." -ForegroundColor Cyan
