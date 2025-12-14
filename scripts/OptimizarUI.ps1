#requires -Version 5.1
<#
.SYNOPSIS
    OPTIMIZADOR UX/UI - VERSIÓN ASCII COMPATIBLE
    Autor: Dsanti (@donpelo)
    GitHub: https://github.com/donpelo/biblia
#>

# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================
$Global:Theme = @{
    PrimaryColor    = "Cyan"
    SecondaryColor  = "Yellow"
    SuccessColor    = "Green"
    ErrorColor      = "Red"
    WarningColor    = "Yellow"
    InfoColor       = "Gray"
    AccentColor     = "Magenta"
    
    # Tema actual
    CurrentTheme    = "dark"
}

# ============================================
# FUNCIONES DE VERIFICACIÓN (ASCII)
# ============================================
function Test-ProjectStructure {
    param([string]$ProjectPath = "C:\BibliaInteractiva")
    
    $structure = @{
        directories = @(
            "$ProjectPath",
            "$ProjectPath\scripts",
            "$ProjectPath\scripts\modules",
            "$ProjectPath\data",
            "$ProjectPath\data\metadata",
            "$ProjectPath\data\versions",
            "$ProjectPath\assets",
            "$ProjectPath\user_data",
            "$ProjectPath\logs"
        )
        
        essentialFiles = @(
            "$ProjectPath\scripts\BibliaInteractiva.ps1",
            "$ProjectPath\config.json",
            "$ProjectPath\data\metadata\books.json"
        )
    }
    
    $results = @{
        Directories = @{Missing = @(); Existing = @()}
        EssentialFiles = @{Missing = @(); Existing = @()}
        Score = 0
        TotalItems = 0
    }
    
    Write-Host "`n[VERIFICANDO ESTRUCTURA DEL PROYECTO]" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Gray
    
    # Verificar directorios
    Write-Host "`nDIRECTORIOS:" -ForegroundColor Yellow
    foreach ($dir in $structure.directories) {
        if (Test-Path $dir) {
            Write-Host "  [OK] $dir" -ForegroundColor Green
            $results.Directories.Existing += $dir
        } else {
            Write-Host "  [X] $dir" -ForegroundColor Red
            $results.Directories.Missing += $dir
        }
        $results.TotalItems++
    }
    
    # Verificar archivos esenciales
    Write-Host "`nARCHIVOS ESENCIALES:" -ForegroundColor Yellow
    foreach ($file in $structure.essentialFiles) {
        if (Test-Path $file) {
            Write-Host "  [OK] $file" -ForegroundColor Green
            $results.EssentialFiles.Existing += $file
            $results.Score += 10
        } else {
            Write-Host "  [X] $file" -ForegroundColor Red
            $results.EssentialFiles.Missing += $file
        }
        $results.TotalItems++
    }
    
    # Calcular puntuación
    $maxScore = ($structure.essentialFiles.Count * 10)
    $results.Percentage = [math]::Round(($results.Score / $maxScore) * 100, 2)
    
    Write-Host "`nRESUMEN DE VERIFICACION:" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Gray
    Write-Host "  Directorios: $($results.Directories.Existing.Count)/$($structure.directories.Count)" -ForegroundColor White
    Write-Host "  Archivos esenciales: $($results.EssentialFiles.Existing.Count)/$($structure.essentialFiles.Count)" -ForegroundColor White
    Write-Host "  Puntuacion: $($results.Score)/$maxScore ($($results.Percentage)%)" -ForegroundColor White
    
    if ($results.Percentage -lt 80) {
        Write-Host "`n[!] SE RECOMIENDA MEJORAR LA ESTRUCTURA" -ForegroundColor Yellow
    } else {
        Write-Host "`n[OK] ESTRUCTURA OPTIMA" -ForegroundColor Green
    }
    
    return $results
}

function Create-BasicUXFiles {
    param([string]$ProjectPath = "C:\BibliaInteractiva")
    
    Write-Host "`n[CREANDO ARCHIVOS DE INTERFAZ BASICA]" -ForegroundColor Magenta
    
    # 1. MÓDULO DE INTERFAZ SIMPLIFICADO (ASCII)
    $uiModule = @'
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
'@
    
    # Crear directorio de módulos si no existe
    $modulesPath = "$ProjectPath\scripts\modules"
    if (-not (Test-Path $modulesPath)) {
        New-Item -ItemType Directory -Path $modulesPath -Force | Out-Null
    }
    
    $uiModule | Out-File "$modulesPath\UI.psm1" -Encoding UTF8
    Write-Host "  [OK] modules\UI.psm1 (modulo de interfaz)" -ForegroundColor Green
    
    # 2. MENÚ MEJORADO SIMPLIFICADO
    $menuTemplate = @'
# MENÚ MEJORADO BIBLIA INTERACTIVA
# Importar módulo de interfaz
Import-Module "$PSScriptRoot\modules\UI.psm1" -Force

function Show-MainMenu {
    do {
        Show-Header -Title "BIBLIA INTERACTIVA" -Subtitle "por Dsanti (@donpelo)" -Version "v2.0"
        
        $menuOptions = @(
            "Leer Biblia",
            "Buscar Versiculos",
            "Planes de Lectura",
            "Audio Biblia (TTS)",
            "Notas y Marcadores",
            "Configuracion",
            "Salir"
        )
        
        Show-Menu -Options $menuOptions -Title "MENU PRINCIPAL"
        
        $choice = Read-Host "`n  Opcion"
        
        switch ($choice) {
            "1" { Show-BibleReader }
            "2" { Show-Search }
            "3" { Show-ReadingPlans }
            "4" { Show-TTS }
            "5" { Show-Notes }
            "6" { Show-Settings }
            "7" { 
                Show-Message -Message "¡Hasta pronto! - Dsanti" -Type "info"
                return 
            }
            default {
                Show-Message -Message "Opcion invalida. Intenta de nuevo." -Type "warning"
            }
        }
    } while ($true)
}

function Show-BibleReader {
    Show-Box -Title "LECTOR BIBLICO" -Color "Cyan" -Content "Selecciona un libro, capitulo y versiculo para comenzar tu lectura."
    
    $books = @("Genesis", "Exodo", "Levitico", "Numeros", "Deuteronomio", "Salir")
    
    do {
        Write-Host "`n  LIBROS DISPONIBLES:" -ForegroundColor Yellow
        for ($i = 0; $i -lt $books.Count; $i++) {
            Write-Host "  $($i+1). $($books[$i])" -ForegroundColor Gray
        }
        
        $choice = Read-Host "`n  Selecciona un libro (1-$($books.Count))"
        
        if ($choice -eq $books.Count.ToString()) {
            return
        }
        
        if ($choice -match "^\d+$" -and [int]$choice -ge 1 -and [int]$choice -lt $books.Count) {
            $book = $books[[int]$choice - 1]
            Show-Message -Message "Libro seleccionado: $book" -Type "success"
            
            # Simular lectura
            Write-Host "`n  --- Genesis 1:1-3 ---" -ForegroundColor Green
            Write-Host "  1. En el principio creo Dios los cielos y la tierra." -ForegroundColor White
            Write-Host "  2. Y la tierra estaba desordenada y vacia..." -ForegroundColor White
            Write-Host "  3. Y dijo Dios: Sea la luz; y fue la luz." -ForegroundColor White
            
            Read-Host "`n  Presiona Enter para continuar"
            return
        } else {
            Show-Message -Message "Seleccion invalida" -Type "error"
        }
    } while ($true)
}

function Show-Search {
    Show-Box -Title "BUSCADOR BIBLICO" -Color "Yellow" -Content "Busca palabras, frases o referencias especificas en todas las versiones disponibles."
    
    $query = Read-Host "`n  ¿Que deseas buscar?"
    
    if ($query) {
        Show-Progress -Current 1 -Total 5 -Label "Buscando: $query"
        
        Write-Host "`n  RESULTADOS ENCONTRADOS (ejemplo):" -ForegroundColor Green
        
        $results = @(
            "Genesis 1:1 - '$query' encontrada",
            "Juan 3:16 - '$query' encontrada",
            "Salmos 23:1 - '$query' encontrada"
        )
        
        foreach ($result in $results) {
            Write-Host "  * $result" -ForegroundColor Gray
        }
    }
    
    Read-Host "`n  Presiona Enter para continuar"
}

function Show-Settings {
    Show-Box -Title "CONFIGURACION" -Color "Magenta" -Content "Ajusta las preferencias de la aplicacion"
    
    $settings = @(
        "Apariencia y Tema",
        "Audio y Sonido",
        "Configuracion de Lectura",
        "Copia de Seguridad",
        "Actualizar desde GitHub",
        "Volver"
    )
    
    do {
        Write-Host "`n  OPCIONES DE CONFIGURACION:" -ForegroundColor Yellow
        for ($i = 0; $i -lt $settings.Count; $i++) {
            Write-Host "  $($i+1). $($settings[$i])" -ForegroundColor Gray
        }
        
        $choice = Read-Host "`n  Selecciona una opcion (1-$($settings.Count))"
        
        switch ($choice) {
            "1" { Show-Message -Message "Configuracion de apariencia" -Type "info" }
            "2" { Show-Message -Message "Configuracion de audio" -Type "info" }
            "3" { Show-Message -Message "Configuracion de lectura" -Type "info" }
            "4" { 
                Show-Progress -Current 75 -Total 100 -Label "Creando copia de seguridad"
                Show-Message -Message "Copia de seguridad completada" -Type "success"
            }
            "5" { 
                Show-Progress -Current 1 -Total 3 -Label "Actualizando desde GitHub"
                Show-Message -Message "Actualizacion completada" -Type "success"
            }
            "6" { return }
            default {
                Show-Message -Message "Opcion invalida" -Type "error"
            }
        }
        
        if ($choice -ne "6") {
            Read-Host "`n  Presiona Enter para continuar"
        }
    } while ($choice -ne "6")
}

# Funciones placeholder
function Show-ReadingPlans {
    Show-Message -Message "Funcion en desarrollo: Planes de Lectura" -Type "info"
    Read-Host "`n  Presiona Enter para continuar"
}

function Show-TTS {
    Show-Message -Message "Funcion en desarrollo: Audio Biblia" -Type "info"
    Read-Host "`n  Presiona Enter para continuar"
}

function Show-Notes {
    Show-Message -Message "Funcion en desarrollo: Notas y Marcadores" -Type "info"
    Read-Host "`n  Presiona Enter para continuar"
}

# Punto de entrada
if ($MyInvocation.InvocationName -ne '.') {
    Show-MainMenu
}
'@
    
    $menuTemplate | Out-File "$ProjectPath\scripts\EnhancedMenu.ps1" -Encoding UTF8
    Write-Host "  [OK] scripts\EnhancedMenu.ps1 (menu mejorado)" -ForegroundColor Green
    
    # 3. ARCHIVO DE CONFIGURACIÓN BÁSICA
    $configContent = @{
        proyecto = "Biblia Interactiva"
        version = "2.0.0"
        autor = "Dsanti (@donpelo)"
        email = "mrgelladuga@gmail.com"
        fecha_instalacion = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        ubicacion = $ProjectPath
        github = "https://github.com/donpelo/biblia"
        ui = @{
            tema = "dark"
            idioma = "es"
            mostrar_ayuda = $true
        }
    }
    
    $configContent | ConvertTo-Json | Out-File "$ProjectPath\config.json" -Encoding UTF8
    Write-Host "  [OK] config.json (configuracion)" -ForegroundColor Green
    
    # 4. DATOS DE EJEMPLO
    $booksData = @'
[
    {
        "id": "GEN",
        "name": "Genesis",
        "chapters": 50,
        "testament": "AT"
    },
    {
        "id": "EXO",
        "name": "Exodo",
        "chapters": 40,
        "testament": "AT"
    },
    {
        "id": "JHN",
        "name": "Juan",
        "chapters": 21,
        "testament": "NT"
    }
]
'@
    
    # Crear directorio de datos si no existe
    $metadataPath = "$ProjectPath\data\metadata"
    if (-not (Test-Path $metadataPath)) {
        New-Item -ItemType Directory -Path $metadataPath -Force | Out-Null
    }
    
    $booksData | Out-File "$metadataPath\books.json" -Encoding UTF8
    Write-Host "  [OK] data\metadata\books.json (datos de libros)" -ForegroundColor Green
    
    Write-Host "`n[ARCHIVOS UX/UI CREADOS EXITOSAMENTE!]" -ForegroundColor Green
}

function Update-MainMenu {
    param([string]$ProjectPath = "C:\BibliaInteractiva")
    
    Write-Host "`n[ACTUALIZANDO MENU PRINCIPAL]" -ForegroundColor Yellow
    
    $mainScript = "$ProjectPath\scripts\BibliaInteractiva.ps1"
    $enhancedMenu = "$ProjectPath\scripts\EnhancedMenu.ps1"
    
    if (Test-Path $enhancedMenu) {
        # Crear copia de seguridad
        if (Test-Path $mainScript) {
            Copy-Item $mainScript "$mainScript.backup" -Force
            Write-Host "  [OK] Copia de seguridad creada" -ForegroundColor Green
        }
        
        # Reemplazar menú principal
        Copy-Item $enhancedMenu $mainScript -Force
        Write-Host "  [OK] Menu principal actualizado" -ForegroundColor Green
    } else {
        Write-Host "  [X] No se encuentra EnhancedMenu.ps1" -ForegroundColor Red
    }
}

# ============================================
# MENÚ PRINCIPAL DEL OPTIMIZADOR
# ============================================
function Show-OptimizerMenu {
    do {
        Clear-Host
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "  OPTIMIZADOR UX/UI - BIBLIA INTERACTIVA" -ForegroundColor Cyan
        Write-Host "         por Dsanti (@donpelo)" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        Write-Host "  [1] Verificar estructura del proyecto" -ForegroundColor Green
        Write-Host "  [2] Crear archivos UX/UI basicos" -ForegroundColor Green
        Write-Host "  [3] Actualizar menu principal" -ForegroundColor Green
        Write-Host "  [4] Probar interfaz mejorada" -ForegroundColor Green
        Write-Host "  [5] Salir" -ForegroundColor Red
        Write-Host ""
        
        $choice = Read-Host "  Selecciona una opcion (1-5)"
        
        switch ($choice) {
            "1" {
                Test-ProjectStructure
                Read-Host "`nPresiona Enter para continuar..."
            }
            "2" {
                Create-BasicUXFiles
                Read-Host "`nPresiona Enter para continuar..."
            }
            "3" {
                Update-MainMenu
                Read-Host "`nPresiona Enter para continuar..."
            }
            "4" {
                Write-Host "`n[PROBANDO INTERFAZ MEJORADA]" -ForegroundColor Cyan
                Set-Location "C:\BibliaInteractiva"
                
                if (Test-Path "scripts\EnhancedMenu.ps1") {
                    & "scripts\EnhancedMenu.ps1"
                } else {
                    Write-Host "  [X] No se encuentra EnhancedMenu.ps1" -ForegroundColor Red
                    Read-Host "`nPresiona Enter para continuar..."
                }
            }
            "5" {
                Write-Host "`n¡Hasta pronto! - Dsanti (@donpelo)" -ForegroundColor Cyan
                return
            }
            default {
                Write-Host "  Opcion invalida. Intenta de nuevo." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    } while ($true)
}

# ============================================
# PUNTO DE ENTRADA
# ============================================
if ($MyInvocation.InvocationName -ne '.') {
    # Verificar ubicación
    if ((Get-Location).Path -ne "C:\BibliaInteractiva") {
        Write-Host "[Cambiando a C:\BibliaInteractiva...]" -ForegroundColor Yellow
        Set-Location "C:\BibliaInteractiva"
    }
    
    # Verificar que el proyecto existe
    if (-not (Test-Path "C:\BibliaInteractiva")) {
        Write-Host "[X] No se encuentra el proyecto en C:\BibliaInteractiva" -ForegroundColor Red
        Write-Host "[!] Ejecuta primero el instalador: InstalarBiblia.ps1" -ForegroundColor Yellow
        Read-Host "`nPresiona Enter para salir"
        exit
    }
    
    # Mostrar menú optimizador
    Show-OptimizerMenu
}