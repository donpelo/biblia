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

def _save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _get_config():
    cfg = _load_json(CONFIG_FILE, default={
        'idioma':'es','version_biblia':'RV1909-es','velocidad_audio':150,
        'voz_audio':'auto','mostrar_numeros_versiculos':True,'tema':'claro'
    })
    if cfg is None: cfg = {}
    return cfg

def _load_version(version_name):
    file_path = os.path.join(VERSIONS_DIR, version_name + '.json')
    if not os.path.exists(file_path): return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _init_tts(cfg):
    engine = pyttsx3.init()
    # Configurar velocidad
    rate = int(cfg.get('velocidad_audio', 150))
    engine.setProperty('rate', rate)
    # Seleccionar voz
    preferred = cfg.get('voz_audio', 'auto')
    voices = engine.getProperty('voices') or []
    selected = None
    if preferred != 'auto':
        for v in voices:
            if preferred.lower() in (v.name or '').lower() or preferred.lower() in (v.id or '').lower():
                selected = v.id; break
    else:
        # Intentar voz en español
        for v in voices:
            meta = (v.name or '') + ' ' + (v.id or '')
            if any(tag in meta.lower() for tag in ['es', 'spanish', 'es-la', 'es-es']):
                selected = v.id; break
    if selected: engine.setProperty('voice', selected)
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
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + f'AUDIO BIBLIA ({version})'.center(50))
        print(Fore.CYAN + '=' * 50)
        books = list(biblia.keys())
        for i, book in enumerate(books, 1):
            print(f'{i:2}. {book}')
        print(Fore.RED + '\\n0. Volver')
        sel = input(Fore.WHITE + '\\nSelecciona un libro: ').strip()
        if sel == '0': break
        if sel.isdigit():
            idx = int(sel)
            if 1 <= idx <= len(books):
                nombre_libro = books[idx-1]
                _menu_capitulos(engine, biblia[nombre_libro], nombre_libro, cfg)

def _menu_capitulos(engine, libro_dict, nombre_libro, cfg):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + f'{nombre_libro}'.center(50))
        print(Fore.CYAN + '=' * 50)
        caps = sorted(list(libro_dict.keys()), key=lambda x: int(str(x)))
        print(Fore.GREEN + '\\nCapítulos disponibles:')
        print(', '.join([str(c) for c in caps]))
        print(Fore.RED + '\\n0. Volver')
        sel = input(Fore.WHITE + '\\nCapítulo a leer en voz alta: ').strip()
        if sel == '0': break
        key = sel if sel in libro_dict else (str(int(sel)) if sel.isdigit() and str(int(sel)) in libro_dict else None)
        if key:
            _leer_capitulo(engine, libro_dict[key], nombre_libro, key, cfg)

def _leer_capitulo(engine, cap_dict, libro, cap, cfg):
    show_nums = cfg.get('mostrar_numeros_versiculos', True)
    encabezado = f'{libro}, capítulo {cap}'
    print(Fore.CYAN + '\\nLeyendo: ' + encabezado)
    _speak(engine, encabezado)
    for vers, texto in sorted(cap_dict.items(), key=lambda kv: int(str(kv[0]))):
        frase = f'Versículo {vers}. {texto}' if show_nums else texto
        print(Fore.WHITE + (f'{vers}. ' if show_nums else '') + texto)
        _speak(engine, frase)
    input(Fore.GREEN + '\\nEnter para continuar...')