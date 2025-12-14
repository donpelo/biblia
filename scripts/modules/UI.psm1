# MÓDULO DE INTERFAZ DE USUARIO - VERSION ASCII
# Autor: Dsanti (@donpelo)

function Show-Header {
    param(
        [string]$Title = "BIBLIA INTERACTIVA",
        [string]$Subtitle = "por Dsanti (@donpelo)",
        [string]$Version = "v2.0"
    )
    
    Clear-Host
    $width = 60
    
    Write-Host ("+" + ("-" * ($width - 2)) + "+") -ForegroundColor Cyan
    Write-Host ("|" + (" " * ($width - 2)) + "|") -ForegroundColor Cyan
    
    # Título centrado
    $titlePadding = [math]::Floor(($width - $Title.Length - 2) / 2)
    Write-Host ("|" + (" " * $titlePadding) + $Title + (" " * ($width - $Title.Length - $titlePadding - 2)) + "|") -ForegroundColor Cyan
    
    # Subtítulo centrado
    if ($Subtitle) {
        $subPadding = [math]::Floor(($width - $Subtitle.Length - 2) / 2)
        Write-Host ("|" + (" " * $subPadding) + $Subtitle + (" " * ($width - $Subtitle.Length - $subPadding - 2)) + "|") -ForegroundColor Yellow
    }
    
    # Versión centrada
    if ($Version) {
        $verPadding = [math]::Floor(($width - $Version.Length - 2) / 2)
        Write-Host ("|" + (" " * $verPadding) + $Version + (" " * ($width - $Version.Length - $verPadding - 2)) + "|") -ForegroundColor Gray
    }
    
    Write-Host ("|" + (" " * ($width - 2)) + "|") -ForegroundColor Cyan
    Write-Host ("+" + ("-" * ($width - 2)) + "+") -ForegroundColor Cyan
    Write-Host ""
}

function Show-Menu {
    param(
        [array]$Options,
        [string]$Title = "MENU PRINCIPAL"
    )
    
    Show-Header -Title "BIBLIA INTERACTIVA" -Subtitle $Title
    
    for ($i = 0; $i -lt $Options.Count; $i++) {
        Write-Host "  $($i+1). $($Options[$i])" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Host "  Selecciona una opcion (1-$($Options.Count)) o 0 para salir" -ForegroundColor Gray
}

function Show-Box {
    param(
        [string]$Title,
        [string]$Content,
        [string]$Color = "Cyan"
    )
    
    $width = 60
    $contentWidth = $width - 4
    
    # Dividir contenido en líneas
    $lines = @()
    $words = $Content -split " "
    $line = ""
    
    foreach ($word in $words) {
        if (($line + " " + $word).Length -le $contentWidth) {
            $line += " " + $word
        } else {
            $lines += $line.Trim()
            $line = $word
        }
    }
    if ($line) { $lines += $line.Trim() }
    
    # Mostrar caja
    Write-Host ""
    Write-Host ("+" + ("-" * ($width - 2)) + "+") -ForegroundColor $Color
    Write-Host ("|" + (" " * ($width - 2)) + "|") -ForegroundColor $Color
    
    # Título centrado
    if ($Title) {
        $titlePadding = [math]::Floor(($width - $Title.Length - 2) / 2)
        Write-Host ("|" + (" " * $titlePadding) + $Title.ToUpper() + (" " * ($width - $Title.Length - $titlePadding - 2)) + "|") -ForegroundColor $Color
        Write-Host ("|" + (" " * ($width - 2)) + "|") -ForegroundColor $Color
    }
    
    # Contenido
    foreach ($line in $lines) {
        $linePadding = 2
        Write-Host ("| " + $line + (" " * ($contentWidth - $line.Length)) + " |") -ForegroundColor $Color
    }
    
    Write-Host ("|" + (" " * ($width - 2)) + "|") -ForegroundColor $Color
    Write-Host ("+" + ("-" * ($width - 2)) + "+") -ForegroundColor $Color
    Write-Host ""
}

function Show-Progress {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Label = "Progreso",
        [int]$Width = 40
    )
    
    $percent = [math]::Round(($Current / $Total) * 100, 1)
    $filled = [math]::Round(($Current / $Total) * $Width)
    $empty = $Width - $filled
    
    $bar = "[" + ("#" * $filled) + ("." * $empty) + "]"
    
    Write-Host "`n  $Label" -ForegroundColor White
    Write-Host "  $bar $percent%" -ForegroundColor Cyan
}

function Show-Message {
    param(
        [string]$Message,
        [string]$Type = "info"
    )
    
    $colors = @{
        info = "Cyan"
        success = "Green"
        warning = "Yellow"
        error = "Red"
    }
    
    $color = $colors[$Type]
    if (-not $color) { $color = "White" }
    
    Write-Host "`n  [$($Type.ToUpper())] $Message" -ForegroundColor $color
}

Export-ModuleMember -Function Show-Header, Show-Menu, Show-Box, Show-Progress, Show-Message
