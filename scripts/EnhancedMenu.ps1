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
