import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

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
        print(f'{v}: {verses[v]}')

if __name__ == '__main__':
    data = cargar_biblia('data/biblia_es.json')
    leer_capitulo(data, 1)
