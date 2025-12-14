import os
import json
import pyttsx3
from colorama import Fore

BIBLIA_FILE = 'biblia.json'
CONFIG_FILE = 'config.json'

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _tts_init():
    try:
        cfg = _load_json(CONFIG_FILE, default={})
        engine = pyttsx3.init()
        rate = cfg.get('velocidad_audio', 150)
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.9)
        desired = cfg.get('voz_audio', 'auto')
        voices = engine.getProperty('voices')
        selected = None
        for v in voices:
            name = (v.name or '').lower()
            # Algunas voces exponen language por atributo, no siempre
            if desired == 'es' and ('spanish' in name or 'es_' in name):
                selected = v.id; break
            if desired == 'en' and ('english' in name or 'en_' in name):
                selected = v.id; break
        if selected:
            engine.setProperty('voice', selected)
        return engine, cfg
    except Exception as e:
        print(Fore.RED + f'Error TTS: {e}')
        return None, None

def menu_audio():
    biblia = _load_json(BIBLIA_FILE, default=None)
    if not biblia:
        input(Fore.RED + 'No se encontrÃ³ biblia.json. Enter...'); return
    engine, cfg = _tts_init()
    if not engine:
        input(Fore.RED + 'No se pudo inicializar TTS. Enter...'); return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + 'AUDIO BIBLIA (TTS)'.center(50))
        print(Fore.CYAN + '=' * 50)
        print(Fore.GREEN + '\\n1. Escuchar capÃ­tulo completo')
        print(Fore.GREEN + '2. Escuchar versÃ­culo especÃ­fico')
        print(Fore.GREEN + '3. Configurar voz y velocidad')
        print(Fore.RED + '0. Volver')
        op = input(Fore.WHITE + '\\nSelecciona: ').strip()
        if op == '0':
            engine.stop()
            break
        elif op == '1':
            escuchar_capitulo(engine, biblia)
        elif op == '2':
            escuchar_versiculo(engine, biblia)
        elif op == '3':
            configurar_audio(engine)

def escuchar_capitulo(engine, biblia):
    ref = input(Fore.WHITE + '\\nLibro y capÃ­tulo (Ej: GÃ©nesis 1): ').strip()
    try:
        partes = ref.split()
        libro = ' '.join(partes[:-1])
        cap = partes[-1]
        texto = ''
        for bloque in ['antiguo_testamento', 'nuevo_testamento']:
            if libro in biblia.get(bloque, {}):
                if cap in biblia[bloque][libro]:
                    for num, t in biblia[bloque][libro][cap].items():
                        texto += f'VersÃ­culo {num}. {t} '
                    break
        if texto:
            print(Fore.GREEN + '\\nReproduciendo...')
            engine.say(f'CapÃ­tulo {cap} del libro de {libro}')
            engine.say(texto)
            engine.runAndWait()
            print(Fore.GREEN + 'Completado.')
        else:
            print(Fore.RED + 'No encontrado.')
    except KeyboardInterrupt:
        engine.stop()
        print(Fore.YELLOW + '\\nDetenido por el usuario.')
    input(Fore.WHITE + '\\nEnter para continuar...')

def escuchar_versiculo(engine, biblia):
    ref = input(Fore.WHITE + '\\nReferencia (Ej: Juan 3:16): ').strip()
    try:
        partes = ref.split()
        libro = ' '.join(partes[:-1])
        cap_vers = partes[-1].split(':')
        cap = cap_vers[0]; vers = cap_vers[1] if len(cap_vers) > 1 else '1'
        texto = ''
        for bloque in ['antiguo_testamento', 'nuevo_testamento']:
            if libro in biblia.get(bloque, {}):
                if cap in biblia[bloque][libro] and vers in biblia[bloque][libro][cap]:
                    texto = biblia[bloque][libro][cap][vers]
                    break
        if texto:
            print(Fore.GREEN + '\\nReproduciendo...')
            engine.say(f'{libro} capÃ­tulo {cap} versÃ­culo {vers}')
            engine.say(texto)
            engine.runAndWait()
            print(Fore.GREEN + 'Completado.')
        else:
            print(Fore.RED + 'No encontrado.')
    except KeyboardInterrupt:
        engine.stop()
        print(Fore.YELLOW + '\\nDetenido por el usuario.')
    input(Fore.WHITE + '\\nEnter para continuar...')

def configurar_audio(engine):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 50)
    print(Fore.YELLOW + 'CONFIGURACIÃ“N DE AUDIO'.center(50))
    print(Fore.CYAN + '=' * 50)
    try:
        v = int(input(Fore.WHITE + '\\nNueva velocidad (100â€“300): ').strip())
        if 100 <= v <= 300:
            engine.setProperty('rate', v)
            cfg = _load_json(CONFIG_FILE, default={})
            cfg['velocidad_audio'] = v
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
            print(Fore.GREEN + 'Velocidad actualizada.')
        else:
            print(Fore.RED + 'Rango invÃ¡lido.')
    except ValueError:
        print(Fore.RED + 'Valor invÃ¡lido.')
    input(Fore.WHITE + '\\nEnter para continuar...')