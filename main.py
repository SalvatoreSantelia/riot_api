from pescriot import *
from googleApi import *
from cassioLib import *

import PySimpleGUI as sg

sg.theme('DarkBlue')

layout = [[sg.Text('Inserisci Game ID')],
          [sg.InputText()],
          [sg.Text('Inserisci Nome Team/Player')],
          [sg.InputText()],
          [sg.Submit(button_text='Crea Foglio')]]

window = sg.Window('GameTracker.gg', layout, margins=(50, 50))

while True:  # The Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    game_id = values[0]
    player_team = values[1]
    if game_id != '' and player_team != '':
        foglio = clonaFoglio("tutorial", nome_clonato="Game_Stats")
        rows = makeRowsOfMatch(game_id, player_team)
        appendiRigheFoglio("Game_Stats", rows)
        sg.popup('Controlla la tua e-mail e/o google drive')
    else:
        sg.popup('Inserire tutti i dati')

window.close()

