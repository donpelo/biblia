# BibliaInteractiva Estado del proyecto

## Objetivo
Un launcher GUI (Tk) que permita:
- Lector bíblico real desde JSON de versiones
- Audio TTS configurable (voz, velocidad, volumen)
- UI bilingue es/en
- Lectura del día configurable
- (Futuro) imágenes de referencia por pasaje

## Estado actual
- Launcher biblia_gui.py compila y abre
- Se detectó BOM en RV1909-es.json, se ajustó a utf-8-sig
- Falta: loader definitivo que entienda la estructura del JSON y entregue texto de versículos
