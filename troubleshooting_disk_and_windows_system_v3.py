import subprocess, time, PySimpleGUI as sg


sg.theme('DarkRed1')

''' FUNÇÃO QUE RODA A VERIFICAÇÃO DE ARQUIVOS DO WINDOWS

O que essa função faz:

1 - Executa 'sfc /scannow' como um processo do sistema operacional via Popen,
    unindo stdout e stderr num único stream de texto (bufsize=1 = leitura
    linha a linha, sem esperar o processo terminar).
2 - Para cada linha lida, aguarda 0.5s (throttle) e envia via
    window.write_event_value('-SCAN-RESULTADO-', item) para a thread
    principal da GUI.
3 - Ao final do processo, envia '-SCAN-RESULTADO-FIM-' sinalizando o
    término da varredura.

Ela é acessível a partir do window.perform_long_operation

'''

def rodar_sfc():
    scan = subprocess.Popen(('sfc', '/scannow'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,)

    for item in scan.stdout:
        time.sleep(0.5)
        window.write_event_value('-SCAN-RESULTADO-', item)

    window.write_event_value('-SCAN-RESULTADO-FIM-', None)

resultado=''

layout = [
        [sg.Text('troubleshooting disk and windows system V2')],
        [sg.ButtonMenu('Qual opção:', 
                       ['Menu', [
                        '1. Validar e corrigir corrupção de arquivos do sistema Windows', 
                        '! 2. Validar e corrigir integridade do sistema de arquivos de um disco', 
                        '3. Limpar os arquivos temporários do Windows', 
                        '! 4. Sair do app' ]
                        ], key='-MENU-')],
        [sg.Text('Essa verificação de integridade usa como padrão o comando sfc /scannow. O sfc /scannow comando examinará todos os arquivos do sistema protegidos e substituirá arquivos corrompidos por uma cópia armazenada em cache. Os resultados da verificação serão mostrados depois que esse processo for concluído', key='-INFO-SCAN-', size=(70,0), visible=False)],
        [sg.Multiline(size=(80,20), key='-RESULTADO-', font=('Calibri', 11), autoscroll=True, disabled=True)]
]

window = sg.Window('troubleshooting disk and windows system V2', layout, icon="folder_managed.ico")


while True:
    
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == '-MENU-':

        opcao = values['-MENU-']

        if '1. Validar e corrigir corrupção de arquivos do sistema Windows' in opcao:
            window.perform_long_operation(lambda: rodar_sfc())
            window['-MENU-'].update(visible=False)
            window['-INFO-SCAN-'].update(visible=True)


    if event == '-SCAN-RESULTADO-':
        resultado += values['-SCAN-RESULTADO-']
        window['-RESULTADO-'].update(resultado)
    elif event == '-SCAN-RESULTADO-FIM-':
        window['-MENU-'].update(visible=True)
        window['-INFO-SCAN-'].update(visible=False)
