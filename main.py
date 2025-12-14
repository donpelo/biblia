import os, json
from colorama import Fore
from modules import lector_biblia, audio_biblia

BASE = r'C:\\BibliaInteractiva'
CONFIG_FILE = os.path.join(BASE, 'config.json')
VERSIONS_DIR = os.path.join(BASE, 'data', 'versions')

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def mostrar():
    cfg = _load_json(CONFIG_FILE, default={})
    version = cfg.get('version_biblia','RV1909-es')
    biblia = _load_json(os.path.join(VERSIONS_DIR, version + '.json'), default={})
    if not biblia:
        print(Fore.RED + 'No se pudo cargar la Biblia.')
        return
    # ejemplo: mostrar Génesis 1:1
    libro = 'Genesis'
    cap = '1'
    ver = '1'
    if "chapters" in biblia.get(libro, {}):
        cap_dict = biblia[libro]["chapters"].get(cap, {})
    else:
        cap_dict = biblia[libro].get(cap, {})
    texto = cap_dict.get(ver, f"Versículo {ver} no encontrado")
    print(Fore.GREEN + f"{libro} {cap}:{ver} -> {texto}")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '='*50)
        print(Fore.YELLOW + 'MENÚ PRINCIPAL'.center(50))
        print(Fore.CYAN + '='*50)
        print('1. Leer Biblia')
        print('2. Buscar')
        print('3. Notas y marcadores')
        print('4. Audio Biblia (TTS)')
        print('5. Planes de lectura')
        print('6. Configuración')
        print('0. Salir')
        sel = input('\\nOpción: ').strip()
        if sel == '0': break
        elif sel == '1': lector_biblia.menu_lectura()
        elif sel == '4': audio_biblia.menu_audio()

if __name__ == '__main__':
    main()