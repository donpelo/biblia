# push-ai-context.ps1
# Script para generar y subir automáticamente el archivo AI_context.txt al repositorio GitHub
# Proyecto: BibliaInteractiva
# Autor: Santiago

cd C:\BibliaInteractiva

# Generar contenido dinámico de AI_context.txt
$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$context = @"
# AI Context - BibliaInteractiva
Generado automáticamente el $fecha

## Hardware
- CPU: Intel Core i5-13400F
- GPU: NVIDIA RTX 4070
- RAM: 32 GB
- Almacenamiento: SSD/NVMe
- Sistema operativo: Windows 10 IoT Enterprise LTSC

## Proyecto
BibliaInteractiva es una aplicación multiplataforma para estudio bíblico con:
- Lectura interactiva de capítulos y versículos
- Audio con voz sintética (pyttsx3)
- Devocionales diarios
- Planes de lectura
- Interfaz gráfica (carpeta gui/)
- Módulos de lógica (carpeta core/)
- Scripts PowerShell para automatización

## Estado actual
- Repositorio sincronizado en GitHub
- Archivos JSON corregidos y cargados
- Módulos lector y audio ajustados para soportar "chapters" y filtrar metadata
- Scripts de navegación y automatización listos
- Contexto AI disponible para asistentes inteligentes
"@

Set-Content -Path "AI_context.txt" -Value $context -Encoding UTF8

# Subir a GitHub
git add AI_context.txt
$mensaje = "Generación automática de AI_context.txt - $fecha"
git commit -m $mensaje
git push origin main

Write-Host "AI_context.txt generado y subido a GitHub (rama main)" -ForegroundColor Green

# Registrar en log local
$logPath  = "C:\BibliaInteractiva\update-log.txt"
$logEntry = "[$fecha] Commit realizado: $mensaje"
Add-Content -Path $logPath -Value $logEntry

Write-Host "Registro añadido en update-log.txt" -ForegroundColor Cyan
