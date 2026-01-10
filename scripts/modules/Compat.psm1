Set-StrictMode -Version Latest

function Show-Passage {
  param(
    [Parameter(Mandatory=$false)][AllowNull()][string]$Text = $null,
    [switch]$Async
  )

  # Si viene vacio, no hace nada (UI no deberia romper por esto)
  if ([string]::IsNullOrWhiteSpace($Text)) { return }

  # Prioridad 1: Speak-Passage (AudioBridge)
  if (Get-Command Speak-Passage -ErrorAction SilentlyContinue) {
    if ($Async) { Speak-Passage -Text $Text -Async } else { Speak-Passage -Text $Text }
    return
  }

  # Prioridad 2: Speak-Text (Audio)
  if (Get-Command Speak-Text -ErrorAction SilentlyContinue) {
    if ($Async) { Speak-Text -Text $Text -Async } else { Speak-Text -Text $Text }
    return
  }

  # Si no hay motor, no hace nada
}

Export-ModuleMember -Function Show-Passage
