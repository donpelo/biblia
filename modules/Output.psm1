Set-StrictMode -Version Latest

function Show-Passage {
  param(
    [Parameter(Mandatory=$true)]
    $Text,
    [switch]$NoAudio,
    [switch]$Async
  )

  if ($null -eq $Text) { return }

  $s = [string]$Text
  if ([string]::IsNullOrWhiteSpace($s)) { return }

  # imprime
Show-Passage $s -Async
  # habla (si está habilitado)
  if (-not $NoAudio) {
    try { Speak-Passage -Text $s -Async:$Async } catch {}
  }
}

Export-ModuleMember -Function Show-Passage

