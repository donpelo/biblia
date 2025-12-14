import os, json
from colorama import Fore

CONFIG_FILE = 'config.json'
VERSIONS_DIR = os.path.join('data','versions')

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

def menu_lectura():
    cfg = _get_config()
    version = cfg.get('version_biblia','RV1909-es')
    biblia = _load_version(version)
    if not biblia:
        input(Fore.RED + 'No se pudo cargar la versión seleccionada. Enter...')
        return
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '='*50)
        print(Fore.YELLOW + f'LECTOR BIBLIA ({version})'.center(50))
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
                seleccionar_capitulo(biblia[nombre_libro], nombre_libro, cfg)

def seleccionar_capitulo(libro_dict, nombre_libro, cfg):
    # Si existe nodo "chapters", usarlo
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
            mostrar_capitulo(cap_dict[sel], nombre_libro, sel, cfg)

def mostrar_capitulo(cap_dict, libro, cap, cfg):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '='*50)
    print(Fore.YELLOW + f'{libro} {cap}'.center(50))
    print(Fore.CYAN + '='*50)
    show_nums = cfg.get('mostrar_numeros_versiculos', True)
    for vers, texto in sorted(cap_dict.items(), key=lambda kv: int(str(kv[0]))):
        if show_nums:
            print(f"{vers}. {texto}")
        else:
            print(texto)
    input(Fore.GREEN + '\\nEnter para continuar...')