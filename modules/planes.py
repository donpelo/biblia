import json
import os
from datetime import datetime
from colorama import Fore

PLANES_FILE = 'planes_lectura.json'
PROGRESS_FILE = 'progress.json'

def _load_json(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def _save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def menu_planes():
    planes = _load_json(PLANES_FILE, default={'planes': []})
    progress = _load_json(PROGRESS_FILE, default={'plan_activo_id': None, 'progresos': {}})
    if progress.get('progresos') is None:
        progress['progresos'] = {}
    for p in planes.get('planes', []):
        progress['progresos'].setdefault(str(p['id']), {'dias_completados': 0})
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + '=' * 50)
        print(Fore.YELLOW + 'PLANES DE LECTURA'.center(50))
        print(Fore.CYAN + '=' * 50)
        print(Fore.GREEN + '\nPlanes disponibles:\n')
        for plan in planes['planes']:
            activo = (progress['plan_activo_id'] == plan['id'])
            estado = Fore.GREEN + '[ACTIVO]' if activo else Fore.YELLOW + '[INACTIVO]'
            comp = progress['progresos'][str(plan['id'])]['dias_completados']
            print(f"{plan['id']}. {plan['nombre']} {estado}")
            print(f"   {plan['descripcion']}")
            print(f"   Progreso: {comp}/{plan['duracion']} días\n")
        print(Fore.GREEN + '1. Activar/Desactivar plan')
        print(Fore.GREEN + '2. Marcar día como leído')
        print(Fore.GREEN + '3. Ver progreso detallado')
        print(Fore.RED + '0. Volver')
        op = input(Fore.WHITE + '\nSelecciona una opción: ').strip()
        if op == '0':
            break
        elif op == '1':
            activar_plan(planes, progress)
        elif op == '2':
            marcar_dia_leido(planes, progress)
        elif op == '3':
            ver_progreso(planes, progress)

def activar_plan(planes, progress):
    try:
        pid = int(input(Fore.WHITE + '\nID del plan: ').strip())
        ids = [p['id'] for p in planes['planes']]
        if pid not in ids:
            print(Fore.RED + 'Plan no encontrado.'); input('Enter...'); return
        progress['plan_activo_id'] = pid if progress['plan_activo_id'] != pid else None
        _save_json(PROGRESS_FILE, progress)
        print(Fore.GREEN + 'Estado actualizado.'); input('Enter...')
    except ValueError:
        input(Fore.RED + 'ID inválido. Enter...')

def marcar_dia_leido(planes, progress):
    pid = progress.get('plan_activo_id')
    if pid is None:
        print(Fore.RED + 'No hay plan activo.'); input('Enter...'); return
    plan = next(p for p in planes['planes'] if p['id'] == pid)
    prog = progress['progresos'][str(pid)]
    if prog['dias_completados'] < plan['duracion']:
        prog['dias_completados'] += 1
        _save_json(PROGRESS_FILE, progress)
        print(Fore.GREEN + f"Día {prog['dias_completados']} marcado como leído.")
        if prog['dias_completados'] == plan['duracion']:
            print(Fore.CYAN + '¡Has completado el plan!')
    else:
        print(Fore.YELLOW + 'Plan ya completado.')
    input('Enter...')

def ver_progreso(planes, progress):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + '=' * 50)
    print(Fore.YELLOW + 'PROGRESO'.center(50))
    print(Fore.CYAN + '=' * 50)
    pid = progress.get('plan_activo_id')
    if pid is None:
        print(Fore.RED + '\nNo hay plan activo.')
        input('Enter...'); return
    plan = next(p for p in planes['planes'] if p['id'] == pid)
    comp = progress['progresos'][str(pid)]['dias_completados']
    porc = (comp / plan['duracion']) * 100
    barra = '█' * int(porc / 5) + '░' * (20 - int(porc / 5))
    print(Fore.GREEN + f"\n{plan['nombre']}")
    print(Fore.WHITE + f"Progreso: {comp}/{plan['duracion']} días")
    print(Fore.CYAN + f"[{barra}] {porc:.1f}%")
    input('\nEnter para continuar...')