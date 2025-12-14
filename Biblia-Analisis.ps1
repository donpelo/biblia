#requires -Version 5.1
<#
.SYNOPSIS
  Revisión y análisis de datos sobre las biblias en JSON (español e inglés).
.DESCRIPTION
  Detecta versiones en data\versions, analiza estadísticas, permite búsquedas y comparaciones.
#>

param(
  [string]$Base = "C:\BibliaInteractiva"
)

$ErrorActionPreference = "Stop"

function Load-Bible {
  param([string]$Path)
  try {
    $json = Get-Content $Path -Raw | ConvertFrom-Json
    return $json
  } catch {
    Write-Host "⚠ Error cargando $Path: $($_.Exception.Message)" -ForegroundColor Yellow
    return $null
  }
}

function Get-BibleStats {
  param($Bible,[string]$VersionName)
  $books = $Bible.PSObject.Properties.Name
  $chapters = 0; $verses = 0
  foreach ($book in $books) {
    $chapDict = $Bible.$book
    foreach ($ch in $chapDict.PSObject.Properties.Name) {
      $chapters++
      $verses += $chapDict.$ch.PSObject.Properties.Count
    }
  }
  [PSCustomObject]@{
    Version = $VersionName
    Libros = $books.Count
    Capitulos = $chapters
    Versiculos = $verses
  }
}

function Search-Keyword {
  param($Bible,[string]$Keyword,[string]$VersionName)
  $results = @()
  foreach ($book in $Bible.PSObject.Properties.Name) {
    foreach ($ch in $Bible.$book.PSObject.Properties.Name) {
      foreach ($v in $Bible.$book.$ch.PSObject.Properties.Name) {
        $text = $Bible.$book.$ch.$v
        if ($text -match $Keyword) {
          $results += "$VersionName | $book $ch:$v - $text"
        }
      }
    }
  }
  return $results
}

function Compare-Verses {
  param([string]$Book,[string]$Chapter,[string]$Verse,$Bibles)
  Write-Host "=== Comparación $Book $Chapter:$Verse ===" -ForegroundColor Cyan
  foreach ($entry in $Bibles) {
    $ver = $entry.Version
    $bible = $entry.Data
    try {
      $text = $bible.$Book.$Chapter.$Verse
      Write-Host "$ver: $text" -ForegroundColor Green
    } catch {
      Write-Host "$ver: (no encontrado)" -ForegroundColor Yellow
    }
  }
}

# --- MAIN ---
$VersionsPath = Join-Path $Base "data\versions"
if (-not (Test-Path $VersionsPath)) { Write-Host "No existe $VersionsPath" -ForegroundColor Red; exit }

Write-Host "=== Actualizando librerías Python ===" -ForegroundColor Cyan
pip install --upgrade -r (Join-Path $Base "requirements.txt")

Write-Host "=== Detectando versiones en $VersionsPath ===" -ForegroundColor Cyan
$bibles = @()
Get-ChildItem $VersionsPath -Filter *.json | ForEach-Object {
  $verName = $_.BaseName
  $data = Load-Bible $_.FullName
  if ($data) {
    $bibles += [PSCustomObject]@{Version=$verName;Data=$data}
    Write-Host "✓ Cargada versión: $verName" -ForegroundColor Green
  }
}

Write-Host "`n=== Estadísticas por versión ===" -ForegroundColor Cyan
foreach ($b in $bibles) {
  $stats = Get-BibleStats $b.Data $b.Version
  $stats | Format-Table -AutoSize
}

Write-Host "`n=== Búsqueda de palabra clave ===" -ForegroundColor Cyan
$keyword = Read-Host "Introduce palabra clave (ej: Dios, love)"
foreach ($b in $bibles) {
  $results = Search-Keyword $b.Data $keyword $b.Version
  Write-Host "`nVersión $($b.Version): $($results.Count) coincidencias" -ForegroundColor Yellow
  $results | Select-Object -First 5 | ForEach-Object { Write-Host $_ }
}

Write-Host "`n=== Comparación de versículo ===" -ForegroundColor Cyan
$book = Read-Host "Libro (ej: Juan)"
$chapter = Read-Host "Capítulo (ej: 3)"
$verse = Read-Host "Versículo (ej: 16)"
Compare-Verses $book $chapter $verse $bibles

Write-Host "`nAnálisis completado." -ForegroundColor Cyan
