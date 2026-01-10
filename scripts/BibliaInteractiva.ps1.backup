# BIBLIA INTERACTIVA - Script Principal
# Autor: Dsanti (@donpelo)
# Ubicado en: C:\BibliaInteractiva

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║         BIBLIA INTERACTIVA v2.0                ║" -ForegroundColor Cyan
    Write-Host "  ║           por Dsanti (@donpelo)                ║" -ForegroundColor Cyan
    Write-Host "  ║    Instalado en: C:\BibliaInteractiva          ║" -ForegroundColor Cyan
    Write-Host "  ╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-MainMenu {
    do {
        Show-Banner
        Write-Host "  📖 MENÚ PRINCIPAL" -ForegroundColor Yellow
        Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  1. 📚 Leer Biblia" -ForegroundColor Green
        Write-Host "  2. 🔍 Buscar versículos" -ForegroundColor Green
        Write-Host "  3. 📝 Notas personales" -ForegroundColor Green
        Write-Host "  4. ⚙️  Configuración" -ForegroundColor Green
        Write-Host "  5. 🚪 Salir" -ForegroundColor Red
        Write-Host ""
        
        $choice = Read-Host "  Selecciona una opción [1-5]"
        
        switch ($choice) {
            "1" {
                Show-BibleReader
            }
            "2" {
                Show-Search
            }
            "3" {
                Show-Notes
            }
            "4" {
                Show-Config
            }
            "5" {
                Write-Host "`n  ¡Hasta pronto! - Dsanti (@donpelo)" -ForegroundColor Cyan
                return
            }
            default {
                Write-Host "  Opción inválida. Intenta de nuevo." -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    } while ($true)
}

function Show-BibleReader {
    Clear-Host
    Show-Banner
    Write-Host "  📚 LECTOR BÍBLICO" -ForegroundColor Yellow
    Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
    
    # Libros de ejemplo
    $books = @(
        @{Name="Génesis"; Chapters=50; Testament="AT"},
        @{Name="Éxodo"; Chapters=40; Testament="AT"},
        @{Name="Juan"; Chapters=21; Testament="NT"},
        @{Name="Salmos"; Chapters=150; Testament="AT"}
    )
    
    Write-Host "  Libros disponibles:" -ForegroundColor White
    for ($i = 0; $i -lt $books.Count; $i++) {
        Write-Host "  $($i+1). $($books[$i].Name) [$($books[$i].Testament)]" -ForegroundColor Gray
    }
    
    Write-Host ""
    $bookChoice = Read-Host "  Selecciona un libro (1-$($books.Count))"
    
    if ($bookChoice -match "^\d+$" -and [int]$bookChoice -ge 1 -and [int]$bookChoice -le $books.Count) {
        $book = $books[[int]$bookChoice - 1]
        Write-Host "`n  Has seleccionado: $($book.Name)" -ForegroundColor Green
        
        # Texto de ejemplo
        Write-Host "  Texto de ejemplo (Génesis 1:1-3):" -ForegroundColor White
        Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  1. En el principio creó Dios los cielos y la tierra." -ForegroundColor Gray
        Write-Host "  2. Y la tierra estaba desordenada y vacía..." -ForegroundColor Gray
        Write-Host "  3. Y dijo Dios: Sea la luz; y fue la luz." -ForegroundColor Gray
    }
    
    Write-Host ""
    Read-Host "  Presiona Enter para continuar..."
}

function Show-Search {
    Clear-Host
    Show-Banner
    Write-Host "  🔍 BUSCADOR BÍBLICO" -ForegroundColor Yellow
    Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
    
    $query = Read-Host "  Introduce palabra o frase a buscar"
    
    if ($query) {
        Write-Host "`n  Buscando '$query'..." -ForegroundColor Cyan
        Write-Host "  (Función completa en desarrollo)" -ForegroundColor Gray
        
        # Resultados de ejemplo
        Write-Host "`n  Resultados encontrados (ejemplo):" -ForegroundColor White
        Write-Host "  • Génesis 1:1 - '$query' encontrada" -ForegroundColor Gray
        Write-Host "  • Juan 3:16 - '$query' encontrada" -ForegroundColor Gray
        Write-Host "  • Salmos 23:1 - '$query' encontrada" -ForegroundColor Gray
    }
    
    Write-Host ""
    Read-Host "  Presiona Enter para continuar..."
}

function Show-Notes {
    Clear-Host
    Show-Banner
    Write-Host "  📝 NOTAS PERSONALES" -ForegroundColor Yellow
    Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
    
    $notesFile = "user_data\mis_notas.txt"
    
    Write-Host "  1. ✏️  Crear nueva nota" -ForegroundColor Green
    Write-Host "  2. 📋 Ver notas guardadas" -ForegroundColor Green
    Write-Host "  3. ↩️  Volver" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "  Selecciona opción [1-3]"
    
    switch ($choice) {
        "1" {
            $nota = Read-Host "`n  Escribe tu nota"
            $fecha = Get-Date -Format "dd/MM/yyyy HH:mm"
            
            "$fecha | $nota" | Out-File $notesFile -Append -Encoding UTF8
            
            Write-Host "`n  ✅ Nota guardada en: $notesFile" -ForegroundColor Green
            Read-Host "  Presiona Enter para continuar..."
        }
        "2" {
            if (Test-Path $notesFile) {
                Write-Host "`n  📓 MIS NOTAS" -ForegroundColor Cyan
                Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
                Get-Content $notesFile | ForEach-Object {
                    Write-Host "  • $_" -ForegroundColor Gray
                }
            } else {
                Write-Host "`n  No hay notas guardadas aún." -ForegroundColor Gray
            }
            Read-Host "`n  Presiona Enter para continuar..."
        }
    }
}

function Show-Config {
    Clear-Host
    Show-Banner
    Write-Host "  ⚙️  CONFIGURACIÓN" -ForegroundColor Yellow
    Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
    
    Write-Host "  1. 🔄 Actualizar desde GitHub" -ForegroundColor Green
    Write-Host "  2. 📊 Ver información del sistema" -ForegroundColor Green
    Write-Host "  3. 🗑️  Limpiar datos temporales" -ForegroundColor Green
    Write-Host "  4. ↩️  Volver" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "  Selecciona opción [1-4]"
    
    switch ($choice) {
        "1" {
            Write-Host "`n  Actualizando desde GitHub..." -ForegroundColor Yellow
            Write-Host "  Repositorio: https://github.com/donpelo/biblia" -ForegroundColor Gray
            Write-Host "  (Función de actualización en desarrollo)" -ForegroundColor Gray
            Read-Host "`n  Presiona Enter para continuar..."
        }
        "2" {
            Write-Host "`n  📊 INFORMACIÓN DEL SISTEMA" -ForegroundColor Cyan
            Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
            Write-Host "  Proyecto: Biblia Interactiva v2.0" -ForegroundColor Gray
            Write-Host "  Autor: Dsanti (@donpelo)" -ForegroundColor Gray
            Write-Host "  Email: mrgelladuga@gmail.com" -ForegroundColor Gray
            Write-Host "  GitHub: https://github.com/donpelo/biblia" -ForegroundColor Gray
            Write-Host "  Ubicación: C:\BibliaInteractiva" -ForegroundColor Gray
            Write-Host "  Usuario Windows: $env:USERNAME" -ForegroundColor Gray
            Write-Host "  Equipo: $env:COMPUTERNAME" -ForegroundColor Gray
            Write-Host ""
            Read-Host "  Presiona Enter para continuar..."
        }
        "3" {
            if (Test-Path "logs") {
                Remove-Item "logs\*" -Force -ErrorAction SilentlyContinue
                Write-Host "`n  ✅ Datos temporales eliminados" -ForegroundColor Green
            }
            Read-Host "`n  Presiona Enter para continuar..."
        }
    }
}

# Iniciar aplicación
Show-MainMenu
