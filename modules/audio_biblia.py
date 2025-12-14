import os, json, pyttsx3
from colorama import init, Fore
init(autoreset=True)

BASE = r'C:\\BibliaInteractiva'
VERSIONS_DIR = os.path.join(BASE, 'data', 'versions')
CONFIG_FILE = os.path.join(BASE, 'config.json')

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _get_config():
    return _load_json(CONFIG_FILE, default={})

def _load_version(version_name):
    file_path = os.path.join(VERSIONS_DIR, version_name + '.json')
    if not os.path.exists(file_path): return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _init_tts(cfg):
    engine = pyttsx3.init()
    rate = int(cfg.get('velocidad_audio', 150))
    engine.setProperty('rate', rate)
    return engine

def _speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def menu_audio():
    cfg = _get_config()
    version = cfg.get('version_biblia', 'RV1909-es')
    biblia = _load_version(version)
    if not biblia:
        input(Fore.RED + 'No se pudo cargar la versión seleccionada. Enter...')
        return
    engine = _init_tts(cfg)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '='*50)
        print(Fore.YELLOW + f'AUDIO BIBLIA ({version})'.center(50))
        print(Fore.CYAN + '='*50)
        libros = list(biblia.keys())
        for i, libro in enumerate(libros,1):
            print(f"{i}. {libro}")
        print(Fore.RED + '\\n0. Volver')
        sel = input(Fore.WHITE + '\\nSelecciona un libro: ').strip()
        if sel == '0': break
        if sel.isdigit():
            idx = int(sel)
            if 1 <= idx <= len(libros):
                nombre_libro = libros[idx-1]
                seleccionar_capitulo(engine, biblia[nombre_libro], nombre_libro, cfg)

def seleccionar_capitulo(engine, libro_dict, nombre_libro, cfg):
    if "chapters" in libro_dict:
        cap_dict = libro_dict["chapters"]
    else:
        cap_dict = libro_dict
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '='*50)
        print(Fore.YELLOW + f'{nombre_libro}'.center(50))
        print(Fore.CYAN + '='*50)
        caps = sorted([k for k in cap_dict.keys() if str(k).isdigit()],
                      key=lambda x: int(str(x)))
        print(Fore.GREEN + '\\nCapítulos disponibles:')
        if caps:
            print(', '.join([str(c) for c in caps]))
        else:
            print(Fore.RED + 'No hay capítulos disponibles en este libro.')
        print(Fore.RED + '\\n0. Volver')
        sel = input(Fore.WHITE + '\\nCapítulo: ').strip()
        if sel == '0': break
        if sel in caps:
            leer_capitulo(engine, cap_dict[sel], nombre_libro, sel, cfg)

def leer_capitulo(engine, cap_dict, libro, cap, cfg):
    show_nums = cfg.get('mostrar_numeros_versiculos', True)
    encabezado = f'{libro}, capítulo {cap}'
    print(Fore.CYAN + '\\nLeyendo: ' + encabezado)
    _speak(engine, encabezado)
    for vers, texto in sorted(cap_dict.items(), key=lambda kv: int(str(kv[0]))):
        frase = f'Versículo {vers}. {texto}' if show_nums else texto
        print(Fore.WHITE + (f'{vers}. ' if show_nums else '') + texto)
        _speak(engine, frase)
    input(Fore.GREEN + '\\nEnter para continuar...')