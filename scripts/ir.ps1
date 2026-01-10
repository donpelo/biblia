param(
    [string]$Capitulo,
    [string]$Versiculo
)

. .\scripts\_cargar.ps1

if ($biblia.chapters.$Capitulo -and $biblia.chapters.$Capitulo.$Versiculo) {
    $config.last_chapter = $Capitulo
    $config.last_verse = $Versiculo
}

$config | ConvertTo-Json -Depth 10 | Set-Content config.json -Encoding UTF8