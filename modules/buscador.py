import os
import json
from colorama import Fore

BIBLIA_FILE = 'biblia.json'

def _load_biblia():
    try:
        with open(BIBLIA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def menu_busqueda():
    biblia = _load_biblia()
    if not biblia:
        input(Fore.RED + 'No se encontrÃ³ biblia.json. Enter para volver...')
        return
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + 'BUSCADOR DE VERSÃCULOS'.center(50))
        print(Fore.CYAN + '=' * 50)
        print(Fore.GREEN + '\\n1. Buscar por palabra clave')
        print(Fore.GREEN + '2. Buscar por referencia (Ej: GÃ©nesis 1:1)')
        print(Fore.RED + '0. Volver')
        op = input(Fore.WHITE + '\\nSelecciona una opciÃ³n: ').strip()
        if op == '0':
            break
        elif op == '1':
            buscar_por_palabra(biblia)
        elif op == '2':
            buscar_por_referencia(biblia)

def buscar_por_palabra(biblia):
    palabra = input(Fore.WHITE + '\\nPalabra: ').lower().strip()
    resultados = []
    for libro, contenido in biblia.get('antiguo_testamento', {}).items():
        for cap, versos in contenido.items():
            for vnum, texto in versos.items():
                if palabra in texto.lower():
                    resultados.append(f'{libro} {cap}:{vnum} - {texto}')
    for libro, contenido in biblia.get('nuevo_testamento', {}).items():
        for cap, versos in contenido.items():
            for vnum, texto in versos.items():
                if palabra in texto.lower():
                    resultados.append(f'{libro} {cap}:{vnum} - {texto}')
    mostrar_resultados(resultados, palabra)

def buscar_por_referencia(biblia):
    ref = input(Fore.WHITE + '\\nReferencia (Libro CapÃ­tulo:VersÃ­culo): ').strip()
    try:
        partes = ref.split()
        libro = ' '.join(partes[:-1])
        cap_vers = partes[-1].split(':')
        cap = cap_vers[0]
        vers = cap_vers[1] if len(cap_vers) > 1 else '1'
        for bloque in ['antiguo_testamento', 'nuevo_testamento']:
            if libro in biblia[bloque]:
                if cap in biblia[bloque][libro] and vers in biblia[bloque][libro][cap]:
                    texto = biblia[bloque][libro][cap][vers]
                    mostrar_versiculo(libro, cap, vers, texto)
                    return
        print(Fore.RED + 'Referencia no encontrada.')
    except Exception:
        print(Fore.RED + 'Formato incorrecto.')
    input(Fore.WHITE + '\\nEnter para continuar...')

def mostrar_resultados(resultados, palabra):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 50)
    print(Fore.YELLOW + f"RESULTADOS PARA: '{palabra}'".center(50))

    print(Fore.CYAN + '=' * 50)
    if resultados:
        print(Fore.GREEN + f'\\n{len(resultados)} resultados:\\n')
        for i, r in enumerate(resultados[:30], 1):
            print(Fore.WHITE + f'{i}. {r}')
        if len(resultados) > 30:
            print(Fore.YELLOW + f"\n... y {len(resultados) - 30} más")

    else:
        print(Fore.RED + '\\nNo se encontraron resultados.')
    input(Fore.GREEN + '\\nEnter para continuar...')

def mostrar_versiculo(libro, cap, vers, texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 60)
    print(Fore.YELLOW + f'{libro} {cap}:{vers}'.center(60))
    print(Fore.CYAN + '=' * 60 + '\\n')
    print(Fore.WHITE + texto)
    print(Fore.CYAN + '\\n' + '=' * 60)
    input(Fore.GREEN + '\\nEnter para continuar...')