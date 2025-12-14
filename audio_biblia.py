import json
import pyttsx3
import sys

sys.stdout.reconfigure(encoding='utf-8')

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def configurar_voz():
    for v in engine.getProperty('voices'):
        if 'spanish' in v.name.lower() or 'es' in v.id.lower():
            engine.setProperty('voice', v.id)
            break

def cargar_biblia(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def leer_capitulo(data, cap):
    chapters = data.get('chapters', {})
    verses = chapters.get(str(cap))
    if not verses:
        print('Capítulo no disponible')
        return
    for v in sorted(verses, key=lambda x: int(x)):
        engine.say(verses[v])
    engine.runAndWait()

if __name__ == '__main__':
    configurar_voz()
    data = cargar_biblia('data/biblia_es.json')
    leer_capitulo(data, 1)
