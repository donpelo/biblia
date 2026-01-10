import json

def cargar_biblia(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def obtener_versiculo(biblia, capitulo, versiculo):
    return biblia['chapters'][capitulo][versiculo]