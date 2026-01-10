import json

def guardar(data):
    with open("data/progreso.json", "w") as f:
        json.dump(data, f)

def cargar():
    try:
        with open("data/progreso.json") as f:
            return json.load(f)
    except:
        return {}
