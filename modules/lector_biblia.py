import os, json
from colorama import init, Fore
init(autoreset=True)

BASE = r'C:\\BibliaInteractiva'
VERSIONS_DIR = os.path.join(BASE, 'data', 'versions')
CONFIG_FILE = os.path.join(BASE, 'config.json')
PROGRESS_FILE = os.path.join(BASE, 'progress.json')

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def _list_versions():
    if not os.path.isdir(VERSIONS_DIR): return []
    return [os.path.splitext(f)[0] for f in os.listdir(VERSIONS_DIR) if f.endswith('.json')]

def _load_version(version_name):
    file_path = os.path.join(VERSIONS_DIR, version_name + '.json')
    if not os.path.exists(file_path): return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _get_config():
    cfg = _load_json(CONFIG_FILE, default={})
    if not cfg:
        cfg = {'idioma':'es','version_biblia':'RV1909-es','velocidad_audio':150,'voz_audio':'auto','mostrar_numeros_versiculos':True,'tema':'claro'}
        _save_json(CONFIG_FILE, cfg)
    return cfg

def _update_last_read(book, chapter):
    prog = _load_json(PROGRESS_FILE, default={'plan_activo_id': None, 'progresos': {}, 'ultima_lectura': {}})
    prog['ultima_lectura'] = {'libro': book, 'capitulo': str(chapter)}
    _save_json(PROGRESS_FILE, prog)

def menu_lectura():
    cfg = _get_config()
    versions = _list_versions()
    if not versions:
        input(Fore.RED + 'No hay versiones en data\\versions. Enter...')
        return
    # Selección de versión
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 50)
    print(Fore.YELLOW + 'SELECCIÓN DE VERSIÓN'.center(50))
    print(Fore.CYAN + '=' * 50)
    for i, v in enumerate(versions, 1):
        mark = ' (actual)' if v == cfg.get('version_biblia') else ''
        print(f'{i}. {v}{mark}')
    try:
        idx = int(input(Fore.WHITE + '\\nNúmero de versión: ').strip())
        if 1 <= idx <= len(versions):
            cfg['version_biblia'] = versions[idx-1]
            _save_json(CONFIG_FILE, cfg)
    except ValueError:
        pass
    ver = cfg['version_biblia']
    biblia = _load_version(ver)
    if not biblia:
        input(Fore.RED + 'No se pudo cargar la versión seleccionada. Enter...')
        return
    # Listar libros
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + f'LECTOR ({ver})'.center(50))
        print(Fore.CYAN + '=' * 50)
        books = list(biblia.keys())
        for i, book in enumerate(books, 1):
            print(f'{i:2}. {book}')
        print(Fore.RED + '\\n0. Volver')
        try:
            op = int(input(Fore.WHITE + '\\nSelecciona un libro: ').strip())
        except ValueError:
            continue
        if op == 0: break
        if 1 <= op <= len(books):
            nombre_libro = books[op-1]
            seleccionar_capitulo(biblia[nombre_libro], nombre_libro, cfg)

def seleccionar_capitulo(libro_dict, nombre_libro, cfg):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + f'{nombre_libro}'.center(50))
        print(Fore.CYAN + '=' * 50)
        caps = sorted(list(libro_dict.keys()), key=lambda x: int(str(x)))
        print(Fore.GREEN + '\\nCapítulos disponibles:')
        print(', '.join([str(c) for c in caps]))
        print(Fore.RED + '\\n0. Volver')
        sel = input(Fore.WHITE + '\\nCapítulo: ').strip()
        if sel == '0': break
        if sel in libro_dict or sel.isdigit() and str(int(sel)) in libro_dict:
            chapter_key = sel if sel in libro_dict else str(int(sel))
            mostrar_capitulo(libro_dict[chapter_key], nombre_libro, chapter_key, cfg)

def mostrar_capitulo(cap_dict, libro, cap, cfg):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 60)
    print(Fore.YELLOW + f'{libro} - Capítulo {cap}'.center(60))
    print(Fore.CYAN + '=' * 60 + '\\n')
    show_nums = cfg.get('mostrar_numeros_versiculos', True)
    for vers, texto in sorted(cap_dict.items(), key=lambda kv: int(str(kv[0]))):
        if show_nums:
            print(Fore.WHITE + f'{vers}. {texto}')
        else:
            print(Fore.WHITE + f'{texto}')
    _update_last_read(libro, cap)
    print(Fore.CYAN + '\\n' + '=' * 60)
    input(Fore.GREEN + '\\nEnter para continuar...')