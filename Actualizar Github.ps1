# update-github.ps1
# Script para actualizar manualmente el repositorio GitHub
# Proyecto: BibliaInteractiva
# Autor: Santiago

# Ir al directorio del proyecto
cd C:\BibliaInteractiva

# Mostrar estado actual
git status

# Añadir todos los cambios (modificados y nuevos)
git add .

# Crear commit con fecha y hora automática
$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Actualización manual desde PowerShell - $fecha"

# Subir a la rama principal (main)
git push origin main

# Confirmación en consola
Write-Host "✅ Repositorio actualizado en GitHub (rama main)" -ForegroundColor Green
