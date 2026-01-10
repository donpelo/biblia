cd C:\BibliaInteractiva
git status
git add .
\2025-12-14 00:02:56 = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
\Actualización manual desde PowerShell - 2025-12-14 00:02:56 = "Actualización manual desde PowerShell - \2025-12-14 00:02:56"
git commit -m \Actualización manual desde PowerShell - 2025-12-14 00:02:56
git push origin main
\C:\BibliaInteractiva\update-log.txt = "C:\BibliaInteractiva\update-log.txt"
\[2025-12-14 00:02:56] Commit realizado: Actualización manual desde PowerShell - 2025-12-14 00:02:56 = "[2025-12-14 00:02:56] Commit realizado: \Actualización manual desde PowerShell - 2025-12-14 00:02:56"
Add-Content -Path \C:\BibliaInteractiva\update-log.txt -Value \[2025-12-14 00:02:56] Commit realizado: Actualización manual desde PowerShell - 2025-12-14 00:02:56
Write-Host "✅ Repositorio actualizado y registrado en update-log.txt" -ForegroundColor Green