import json
import pyttsx3
from lector_biblia import cargar_biblia, obtener_versiculo

engine = pyttsx3.init()

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

biblia = cargar_biblia(config['data_path'])

texto = obtener_versiculo(
    biblia,
    config['last_chapter'],
    config['last_verse']
)

engine.say(texto)
engine.runAndWait()