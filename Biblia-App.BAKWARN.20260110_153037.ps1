Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Base = Split-Path -Parent $MyInvocation.MyCommand.Path

try { Import-Module (Join-Path $Base "modules\Audio.psm1") -Force } catch {}
try { Import-Module (Join-Path $Base "modules\AudioBridge.psm1") -Force } catch {}
try { Import-Module (Join-Path $Base "modules\BookMap.psm1") -Force } catch {}

function SpeakIfAvailable {
  param([string]$Text)
  try { Speak-Passage -Text $Text -Async } catch {}
}

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
  try {
    $data = Load-Version $_.FullName
    $bibles += [PSCustomObject]@{ Version = $name; Data = $data; Path = $_.FullName }
  } catch {}
}

if (@($bibles).Count -eq 0) { throw "No se pudo cargar ninguna version." }
# RV1858-es ONLY (porque es la que suena)
$bibles = @($bibles | Where-Object { $_.Version -eq "RV1858-es" })
if (@($bibles).Count -eq 0) { throw "No se encontro RV1858-es en data\versions" }


Write-Host "Versiones disponibles:" -ForegroundColor Cyan
for ($i=0; $i -lt @($bibles).Count; $i++) { Write-Host ("[{0}] {1}" -f $i, $bibles[$i].Version) }

$readIndex = 0  # default
$audioOn = $true  # default

# Libros reales por ID
$books = $bibles[0].Data.Verses | Select-Object -ExpandProperty book | Where-Object { $_ } | Select-Object -Unique
$books = $books | Sort-Object {[int]$_}

Write-Host ""
Write-Host "Libros detectados:" -ForegroundColor Cyan
foreach ($id in ($books | Select-Object -First 40)) {
  $name = Resolve-BookName $id
  Write-Host ("{0} = {1}" -f $id, $name)
}

while ($true) {
  Write-Host ""
  $cmd = Read-Host "Comando: v=ver versiculo, a=toggle audio, s=stop, q=salir"
  if ($cmd -eq "q") { break }
  if ($cmd -eq "a") { $audioOn = -not $audioOn; Write-Host ("Audio: {0}" -f $(if($audioOn){"ON"}else{"OFF"})) -ForegroundColor Yellow; continue }
  if ($cmd -eq "s") { try { Stop-Speech } catch {}; continue }

  if ($cmd -ne "v") { continue }

  $book = Read-Host "Libro ID (ej 40)"
  $chapter = [int](Read-Host "Capitulo (ej 3)")
  $verse = [int](Read-Host "Versiculo (ej 16)")

  $bookName = Resolve-BookName $book
  Write-Host ""
  Write-Host ("=== {0} ({1}) {2}:{3} ===" -f $bookName, $book, $chapter, $verse) -ForegroundColor Cyan

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
    SpeakIfAvailable ($bibles[$readIndex].Version + ". " + $bookName + ". " + $chapter + ":" + $verse + ". " + $toSpeak)
  }
}

Write-Host "Listo." -ForegroundColor Cyan
