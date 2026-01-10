Set-StrictMode -Version Latest

# Config simple (puedes moverlo luego a tu config real)
$script:AudioEnabled = $true
$script:AudioRate = 0
$script:AudioVolume = 100

function Enable-Audio { $script:AudioEnabled = $true }
function Disable-Audio { $script:AudioEnabled = $false; try { Stop-Speech } catch {} }
function Set-AudioRate { param([int]$Rate) $script:AudioRate = $Rate }
function Set-AudioVolume { param([int]$Volume) $script:AudioVolume = $Volume }

function Speak-Passage {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [switch]$Async
  )

  if (-not $script:AudioEnabled) { return }

  # limpieza básica para que el TTS no lea basura
  $clean = ($Text -replace "\s+", " ").Trim()

  # corta cualquier lectura anterior para evitar voces encimadas
  try { Stop-Speech } catch {}

  Speak-Text -Text $clean -Rate $script:AudioRate -Volume $script:AudioVolume -Async:$Async
}

Export-ModuleMember -Function Enable-Audio, Disable-Audio, Set-AudioRate, Set-AudioVolume, Speak-Passage
