import logging
import os

import PySimpleGUI as sg

from maplepy.game.game import Game

# -- PySimpleGUI window layout and creation -----------------------------------

layout = [[sg.Text('Test of PySimpleGUI with PyGame')],
          [sg.Graph((500, 500), (0, 0), (500, 500),background_color='lightblue', key='-GRAPH-')],
          ]

window = sg.Window('PySimpleGUI + PyGame', layout, finalize=True)
graph = window['-GRAPH-']

# -- Magic code to integrate PyGame with tkinter ------------------------------

# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_PyGame_Integration.py
# https://github.com/pygame/pygame/issues/1574
# https://github.com/pygame/pygame/pull/2981

embed = graph.TKCanvas
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# -- Logging module -----------------------------------------------------------

logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

# -- PyGame Code --------------------------------------------------------------

game = Game('config.json')
game.run()
