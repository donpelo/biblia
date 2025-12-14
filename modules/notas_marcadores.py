import json
import os
from colorama import Fore

NOTAS_FILE = 'notas.json'

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def menu_notas():
    data = _load_json(NOTAS_FILE, default={'notas': [], 'marcadores': []})
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + 'NOTAS Y MARCADORES'.center(50))
        print(Fore.CYAN + '=' * 50)
        print(Fore.GREEN + f"\n📝 Notas ({len(data['notas'])})")
        for i, nota in enumerate(data['notas'], 1):
            print(f"{i}. {nota['titulo']} ({nota['referencia']})")
        print(Fore.GREEN + f"\n🔖 Marcadores ({len(data['marcadores'])})")
        for i, marc in enumerate(data['marcadores'], 1):
            print(f"{i}. {marc['referencia']}")
        print(Fore.GREEN + '\n1. Agregar nota')
        print(Fore.GREEN + '2. Agregar marcador')
        print(Fore.GREEN + '3. Eliminar nota')
        print(Fore.GREEN + '4. Eliminar marcador')
        print(Fore.RED + '0. Volver')
        op = input(Fore.WHITE + '\nSelecciona: ').strip()
        if op == '0':
            break
        elif op == '1':
            agregar_nota(data)
        elif op == '2':
            agregar_marcador(data)
        elif op == '3':
            eliminar_nota(data)
        elif op == '4':
            eliminar_marcador(data)

def agregar_nota(data):
    titulo = input('Título: ').strip()
    ref = input('Referencia (ej: Juan 3:16): ').strip()
    contenido = input('Contenido: ').strip()
    data['notas'].append({'titulo': titulo, 'referencia': ref, 'contenido': contenido})
    _save_json(NOTAS_FILE, data)
    print(Fore.GREEN + 'Nota guardada.'); input('Enter...')

def agregar_marcador(data):
    ref = input('Referencia (ej: Salmos 23:1): ').strip()
    data['marcadores'].append({'referencia': ref})
    _save_json(NOTAS_FILE, data)
    print(Fore.GREEN + 'Marcador guardado.'); input('Enter...')

def eliminar_nota(data):
    try:
        idx = int(input('Número de nota a eliminar: ').strip())
        if 1 <= idx <= len(data['notas']):
            data['notas'].pop(idx-1)
            _save_json(NOTAS_FILE, data)
            print(Fore.GREEN + 'Nota eliminada.')
        else:
            print(Fore.RED + 'Número inválido.')
    except ValueError:
        print(Fore.RED + 'Entrada inválida.')
    input('Enter...')

def eliminar_marcador(data):
    try:
        idx = int(input('Número de marcador a eliminar: ').strip())
        if 1 <= idx <= len(data['marcadores']):
            data['marcadores'].pop(idx-1)
            _save_json(NOTAS_FILE, data)
            print(Fore.GREEN + 'Marcador eliminado.')
        else:
            print(Fore.RED + 'Número inválido.')
    except ValueError:
        print(Fore.RED + 'Entrada inválida.')
    input('Enter...')