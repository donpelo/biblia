# BibliaInteractiva Proyecto Estado

## Objetivo
Consolidar una sola app GUI (Tkinter) con:
- Lector bíblico real (carga RV1909-es.json u otras versiones)
- Buscador
- Lectura del día (calendario)
- Audio Biblia TTS (configurable)
- Configuración: idioma UI (es/en), voz, velocidad, volumen
- Referencias visuales (imágenes) por libro/capítulo/evento

## Hecho
- Launcher BAT -> PowerShell -> pythonw abre biblia_gui.py
- Botón Salir funciona
- Configuración UI abre ventana y guarda ajustes
- requirements incluye colorama

## Problemas actuales
- Loader Biblia falla: "[ERROR] No se pudo cargar la Biblia. Revisa data/versions."
- Botón "Abrir BibliaInteractiva (GUI)" abre la app antigua (gui/main.py) además de la nueva.

## Próximo paso lógico
1) Confirmar estructura real de data/versions/RV1909-es.json (keys y ejemplo de versículo).
2) Ajustar loader para parsear correctamente y poblar Libro/Capítulo/Versículo.
3) Reemplazar botón que abre gui/main.py por "Modo clásico (antiguo)" o eliminarlo.

## TODO
- Loader Biblia OK
- UI bilingüe es/en con textos centralizados
- TTS integrado dentro de la misma GUI (no consola)
- Imagenes de referencia por lectura (catálogo local)
