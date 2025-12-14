import os
from modules import lector_biblia, buscador, planes, audio_biblia, notas_marcadores, configuracion

def mostrar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('=' * 50)
    print('Biblia Interactiva v2.0'.center(50))
    print('=' * 50)
    print('\\nMENU PRINCIPAL\\n')
    print('1. Leer Biblia')
    print('2. Buscar VersÃ­culos')
    print('3. Planes de Lectura')
    print('4. Audio Biblia (TTS)')
    print('5. Notas y Marcadores')
    print('6. ConfiguraciÃ³n')
    print('7. Salir')
    print('\\n' + '=' * 50)

def main():
    while True:
        mostrar_menu()
        op = input('\\nSelecciona una opciÃ³n (1-7) o 0 para salir: ').strip()
        if op in ['0', '7']:
            print('\\nÂ¡Gracias por usar la Biblia Interactiva!')
            break
        elif op == '1':
            lector_biblia.menu_lectura()
        elif op == '2':
            buscador.menu_busqueda()
        elif op == '3':
            planes.menu_planes()
        elif op == '4':
            audio_biblia.menu_audio()
        elif op == '5':
            notas_marcadores.menu_notas()
        elif op == '6':
            configuracion.menu_configuracion()
        else:
            input('\\nOpciÃ³n invÃ¡lida. Enter para continuar...')

if __name__ == '__main__':
    main()