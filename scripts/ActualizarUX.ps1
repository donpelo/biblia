# ACTUALIZADOR AUTOMÁTICO UX/UI
Write-Host "🔄 ACTUALIZANDO SISTEMA UX/UI..." -ForegroundColor Cyan

# 1. Descargar última versión del optimizador
$optimizerUrl = "https://raw.githubusercontent.com/donpelo/biblia/main/scripts/OptimizarUI.ps1"
Invoke-WebRequest -Uri $optimizerUrl -OutFile "$PSScriptRoot\OptimizarUI.ps1" -UseBasicParsing

# 2. Descargar módulos UX
$modules = @(
    @{Name="UI.psm1"; Url="https://raw.githubusercontent.com/donpelo/biblia/main/scripts/modules/UI.psm1"},
    @{Name="ThemeManager.psm1"; Url="https://raw.githubusercontent.com/donpelo/biblia/main/scripts/modules/ThemeManager.psm1"}
)

foreach ($module in $modules) {
    $modulePath = "$PSScriptRoot\modules\$($module.Name)"
    Invoke-WebRequest -Uri $module.Url -OutFile $modulePath -UseBasicParsing
    Write-Host "  ✅ $($module.Name) actualizado" -ForegroundColor Green
}

# 3. Ejecutar optimizador
Write-Host "`n🚀 EJECUTANDO OPTIMIZADOR..." -ForegroundColor Yellow
& "$PSScriptRoot\OptimizarUI.ps1"