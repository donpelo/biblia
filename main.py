import lector_biblia
import audio_biblia
import json

def cargar():
    with open('data/biblia_es.json', encoding='utf-8') as f:
        return json.load(f)

def menu():
    print('1 Leer Biblia')
    print('2 Escuchar Biblia')
    op = input('Opción: ')
    data = cargar()
    if op == '1':
        lector_biblia.leer_capitulo(data, 1)
    if op == '2':
        audio_biblia.leer_capitulo(data, 1)

menu()
