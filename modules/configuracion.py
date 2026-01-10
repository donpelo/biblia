import json
import os
from colorama import Fore

CONFIG_FILE = 'config.json'

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def menu_configuracion():
    cfg = _load_json(CONFIG_FILE, default={})
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + 'CONFIGURACIÓN'.center(50))
        print(Fore.CYAN + '=' * 50)
        print(f"\nIdioma: {cfg.get('idioma','es')}")
        print(f"Versión Biblia: {cfg.get('version_biblia','RV1909-es')}")
        print(f"Velocidad audio: {cfg.get('velocidad_audio',150)}")
        print(f"Voz audio: {cfg.get('voz_audio','auto')}")
        print(f"Mostrar números de versículos: {cfg.get('mostrar_numeros_versiculos',True)}")
        print(f"Tema: {cfg.get('tema','claro')}")
        print(Fore.GREEN + '\n1. Cambiar idioma')
        print(Fore.GREEN + '2. Cambiar versión de Biblia')
        print(Fore.GREEN + '3. Cambiar velocidad audio')
        print(Fore.GREEN + '4. Cambiar voz audio')
        print(Fore.GREEN + '5. Alternar mostrar números de versículos')
        print(Fore.GREEN + '6. Cambiar tema')
        print(Fore.RED + '0. Volver')
        op = input(Fore.WHITE + '\nSelecciona: ').strip()
        if op == '0':
            break
        elif op == '1':
            cfg['idioma'] = input('Nuevo idioma (es/en): ').strip()
        elif op == '2':
            cfg['version_biblia'] = input('Nueva versión (ej: RV1909-es): ').strip()
        elif op == '3':
            try:
                cfg['velocidad_audio'] = int(input('Nueva velocidad (ej: 150): ').strip())
            except ValueError:
                pass
        elif op == '4':
            cfg['voz_audio'] = input('Nueva voz (ej: auto): ').strip()
        elif op == '5':
            cfg['mostrar_numeros_versiculos'] = not cfg.get('mostrar_numeros_versiculos', True)
        elif op == '6':
            cfg['tema'] = input('Tema (claro/oscuro): ').strip()
        _save_json(CONFIG_FILE, cfg)