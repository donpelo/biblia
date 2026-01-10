import json

def cargar_notas():
    with open('notas.json', encoding='utf-8') as f:
        return json.load(f)

def guardar_notas(data):
    with open('notas.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
