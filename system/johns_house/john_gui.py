

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
    
from system.gen.settings import LOG_MSG

from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_GUIS')

from system.utils.design_models import Anchor
    
import FreeSimpleGUI as sg
from dataclasses import field, fields

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]


class JohnGUI:
    def __init__(self) -> None:
        self.anch = Anchor(name='TEST')
        self.layout = self.build_eqtable(self.anch)
        self.window = sg.Window('Window Title', self.layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()  # type: ignore
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            print('You entered ', values[0])

        self.window.close()
    

    # CONTEXT MANAGER
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    
    
    # TODO: ADD DROPDOWNS, CHECKBOXES, COLLAPSABLE TABS
    def build_eqtable(self, dataobj):
        layout = []
        
        for field in fields(dataobj):
            cur_val = getattr(dataobj, field.name)
            
            val_as_str = str(cur_val) if cur_val is not None else ''
            
            input_key = f'-Data-{field.name}'
            color = 'PaleGreen'
            log.debug(f'STR VALUE:{val_as_str}')
            if '*' in val_as_str or val_as_str == '' or cur_val is None or not cur_val:
                if LOG_MSG:
                    log.info(f'Field: {field.name} is empty.')
                    color = 'violet'
            row = [
                sg.Text(f'{field.name.replace('_', ' ').title()}:', size=(10,1), text_color='white'),
                sg.Input(cur_val, key=input_key, background_color=color, size=(25,1), text_color='black')
            ]
            layout.append(row)
        return layout
    
    

with JohnGUI() as john:
    pass

# TODO: SCRAPER GUI LAYOUT 
  # TODO: FORMAT / SHOW FULL SCRAPE IN RESULTS TAB
  # TODO:    - HIGHLIGHT PARAMETERS DETERMINED TO BE PARAMS
  # TODO: SAVE IMAGES AGAIN -> SHOW IN IMAGE
  # TODO: WINDOW SIZE CONSTANT
  # TODO: VISUALIZE DATABASE TAB
  
# TODO: DESIGNER LAYOUT