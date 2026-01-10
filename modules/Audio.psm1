Set-StrictMode -Version Latest

Add-Type -AssemblyName System.Speech

$script:tts = New-Object System.Speech.Synthesis.SpeechSynthesizer
$script:tts.Rate = 0
$script:tts.Volume = 100

function Get-TTSVoices {
  $script:tts.GetInstalledVoices() | ForEach-Object {
    $_.VoiceInfo | Select-Object Name, Culture, Gender, Age
  }
}

function Set-TTSVoice {
  param([Parameter(Mandatory=$true)][string]$Name)
  $script:tts.SelectVoice($Name)
}

function Speak-Text {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [int]$Rate = 0,
    [int]$Volume = 100,
    [switch]$Async
  )

  $script:tts.Rate   = [Math]::Max(-10,[Math]::Min(10,$Rate))
  $script:tts.Volume = [Math]::Max(0,[Math]::Min(100,$Volume))

  if ($Async) { [void]$script:tts.SpeakAsync($Text) } else { $script:tts.Speak($Text) }
}

function Stop-Speech {
  $script:tts.SpeakAsyncCancelAll()
}

Export-ModuleMember -Function Get-TTSVoices, Set-TTSVoice, Speak-Text, Stop-Speech
