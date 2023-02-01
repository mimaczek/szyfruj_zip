# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import pyzipper
import secrets
import pyperclip

dlugosc = 12
haslo = secrets.token_urlsafe(dlugosc)

sg.theme('DarkAmber')

layout = [
    [sg.Text('Hasło do pliku:'), sg.InputText(haslo, size=(20, 1), key='-HASLO-')],
    [sg.Text('Nazwa pliku:'), sg.InputText('haslo.txt', size=(20, 1), key='-PLIK_TXT-')],
    [sg.Text('Tekst do zaszyfrowania:')],
    [sg.Multiline(key='-TEKST-', size=(50, 20))],
    [sg.In(size=(45, 1), enable_events=True, key='-IN-'), sg.FileSaveAs(button_text='Zapisz jako...', file_types=(('zip', '.zip'),), key="-PLIK_ZIP-")],
    [sg.Button('Ok'), sg.Button('Cancel')]
]

window = sg.Window('Szyfrator', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Ok':
        if len(values['-PLIK_ZIP-']) == 0 or len(values['-HASLO-']) == 0 or \
                len(values['-PLIK_ZIP-']) == 0 or len(values['-PLIK_TXT-']) == 0:
            sg.popup("WYPEłNIJ wszystkie pola!")
        else:
            with pyzipper.AESZipFile(values['-PLIK_ZIP-'],
                                     'w',
                                     compression=pyzipper.ZIP_LZMA,
                                     encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(str.encode(values['-HASLO-']))
                zf.writestr(values['-PLIK_TXT-'], values['-TEKST-'])
            sg.popup(
                'HASLO: ' + values['-HASLO-'] + ' (W schowku)\n' +
                'TEXT: ' + values['-TEKST-'] + '\n' +
                'PLIK_TXT: ' + values['-PLIK_TXT-'] + '\n' +
                'PLIK_ZIP: ' + values['-PLIK_ZIP-']
            )
            pyperclip.copy(values['-HASLO-'])
            break

    print('HASLO: ', values['-HASLO-'])
    print('TEXT: ', values['-TEKST-'])
    print('PLIK_TXT: ', values['-PLIK_TXT-'])
    print('PLIK_ZIP: ', values['-PLIK_ZIP-'])

window.close()


