cd C:\BibliaInteractiva
git add AI_context.txt
\ = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
\ = "Actualización AI_context.txt - \"
git commit -m \
git push origin main
\ = "C:\BibliaInteractiva\update-log.txt"
\ = "[] Commit realizado: \"
Add-Content -Path \ -Value \
Write-Host "✅ AI_context.txt actualizado y subido a GitHub (rama main)" -ForegroundColor Green