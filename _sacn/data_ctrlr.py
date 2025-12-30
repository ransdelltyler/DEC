



#* FIND PROJECT ROOT AND INSERT IF NOT IN SYSTEM PATH *#
import os, sys
from pathlib import Path
TREE = [str(p) for p in Path(__file__).resolve().parents]
ROOT = 'DEEREATCHAIN'  #? ROOT FOLDER TO LOOK FOR
for path in TREE:
    if Path(path).name == ROOT:
        if path not in sys.path:
            print(f'ADDING {ROOT} TO SYSTEM PATHS')
            sys.path.insert(0, path)
            
#* ROOT FINDER -------------------------------------- *#


import numpy as np

from system.utils.util_classes import ColorLog
from system.gen.settings import LOG_MSG
log = ColorLog('UNIV_CTRL', level=1)

from dataclasses import dataclass, field
from operator import attrgetter

import FreeSimpleGUI as sg

sg.theme('DarkGrey15')

DEF_CTRL_NAME = '-UNIV CONTROLLER-'
DEF_UNIV_DATA = bytearray(512)
DEF_PRIORITY = 100
DEF_START_ADDR = 1
DEF_UNIV = 1



@dataclass(slots=True, kw_only=True)
class Layer:
    name : str | None = DEF_CTRL_NAME
    
    #? HTP PRIORITY
    priority : int | None = DEF_PRIORITY
    
    # TODO: ENABLE PARTIAL UNIV
    start_addr : int | None = DEF_START_ADDR
    
    #? LAYER DMX DATA
    data : bytearray = field(default_factory=bytearray)
    
    #? FLAG: ENABLES LAYER -> OUTPUT
    enabled : bool | None = False
    
    #? FLAG: NEW DATA AVAILABLE (QUICK FLATTEN)
    update : bool | None = True



#* CONTROLLER / GUI : 
#* - MANAGES A SINGLE UNIVERSE OF DATA
#* - MULTIPLE LAYERS CAN BE ADDED FOR HTP
#* - WINDOW INCLUDES BASIC CONTROLS FOR UNIV DATA
# TODO: INPUT SOURCES 

class UnivCtrlr:
    def __init__(self, name : str | None = DEF_CTRL_NAME,) -> None:
        self.ctrlr_name = name
        self.universe = DEF_UNIV
        self.layers = []
        self.channel_check_index = 1
        
        #? FLAG: GUI RUNNING
        self.running = False
        
        #? FULL UNIVERSE DATA OUPUT
        self.output = DEF_UNIV_DATA
        self.output_on = False

        #? BUILD GUI
        #self.layout = self.build_layout()
        self.layout = self.build_check_layout()
        self.window = sg.Window('- UNIVERSE CONTROLLER -', layout=self.layout)
        
               
    #* CONTEXT MANAGER - @INIT FUNCTION
    def __enter__(self):
        return self

    #* CONTEXT MANAGER - @EXIT FUNCTION
    def __exit__(self, exc_type, exc_val, exc_tb):
        #? STOP GUI
        self.running = False
        if hasattr(self, 'window'):
            self.window.close()
            if LOG_MSG: log.success(f'UNIV CONTROLLER SHUTDOWN')


    #* START GUI LOOP
    def run(self):
        if hasattr(self, 'window'):
            # UPDATE FLAG
            self.running = True
            while True:
                event, values = self.window.read(timeout=0.1) # type: ignore
                # QUIT WINDOW
                if event in (sg.WIN_CLOSED, '-QUIT-'):
                    break
                
                # STARTS UPDATING OUTPUT VARIABLE
                if event == '-START-':
                    self.output_on = True
                
                # STOPS UPDATING OUTPUT VARIABLE
                # DOES NOT STOP UPDATING LAYERS
                if event == '-STOP-':
                    self.output_on = False
                
                # CHANNEL CHECK CONTROLS
                if event == '-UP-':
                    if self.channel_check_index < 512:
                        self.channel_check_index += 1
                        self.window['-INDEX-'].update(str(self.channel_check_index)) # type: ignore
                if event == '-DOWN-':
                    if self.channel_check_index > 1:
                        self.channel_check_index -= 1
                        self.window['-INDEX-'].update(str(self.channel_check_index)) # type: ignore
            
            # UPDATE FLAG
            self.running = False
    
    
    #* LAYOUT:RETURNS GRAPHIC INTERFACE FOR USER INPUT
    def build_layout(self) -> list:
        return [
            [sg.Text(f'UNIVERSE:{self.universe}'), sg.Spin(k= '-UNIVERSE-', values=range(1,65536), initial_value=1,),
            sg.Text(f'START:'), sg.Button(k= '-START-', button_text='ENABLE'),
            sg.Text(f'STOP'), sg.Button(k= '-STOP-', button_text='DISABLE'),
            sg.Button(k='-QUIT-', button_text='QUIT')],
            *self.build_fader_bank([str(i) for i in range(1,20)]),
            *self.build_fader_bank([str(i) for i in range(20,39)]),
        ]
    
    
    #* LAYOUT: HORIZONTAL BANK OF VERTICAL SLIDERS W/ <NAMES>
    def build_fader_bank(self, names: list[str]) -> list:
        fader_bank = []
        for name in names:
            # Create a vertical column for each fader + label pair
            column = [
                [sg.Text(name, size=(3, 1), justification='center', pad=(0, 0))],
                [sg.Slider(range=(0, 255), 
                        disable_number_display=True, 
                        orientation='v', 
                        size=(10, 20), # Adjusted size for better scaling
                        default_value=0, 
                        key=name,
                        pad=(5, 0))] # Horizontal padding keeps sliders apart
            ]
            fader_bank.append(sg.Column(column, element_justification='center'))
        # Return a single row (list inside a list) containing all columns
        return [fader_bank]
    
    
    #* LAYOUT: CHANNEL CHECK LAYOUT
    def build_check_layout(self):
        # 1. We put the relief/border on the COLUMN, not the text.
        # 2. We use VPush to "sandwich" the text into the vertical center.
        indicator = sg.Column([
            [sg.VPush()],
            [sg.Text(
                text=str(self.channel_check_index),
                font=('Roboto', 40, 'bold'),
                key='-INDEX-',
                justification='right',
                # Removed expand_y/x and relief from here
            )],
            [sg.VPush()]
        ],
            size=(120, 120),
            element_justification='center', # Centers text horizontally
            pad=(5, 20)
        )

        buttons = [
            sg.Button('START', k='-START-', size=(6, 2)),
            sg.Button('STOP', k='-STOP-', size=(6, 2)),
            sg.Button('QUIT', k='-QUIT-', size=(6, 2)),
            sg.Button('▲', k='-UP-', size=(4, 2)),
            sg.Button('▼', k='-DOWN-', size=(4, 2))
        ]

        # Use Push() to center the indicator row horizontally in the window
        return [[sg.Push(), indicator], buttons]
        
    
    #* CREATE NEW LAYER WITH NAME OR NEXT INDEX
    #? LAYERS ARE ALWAYS FULL 512CH DMX FRAMES
    def add_layer(self, name : str | None = None ):
        if name: 
            self.layers.append(Layer(name=name, data=DEF_UNIV_DATA))
        else: # DEFAULT NAME TO NEXT LAYER LIST INDEX
            next_index = len(self.layers)-1
            self.layers[next_index] = Layer(data=DEF_UNIV_DATA)
    
    
    #* USE PRIORITY TO UPDATE SELF.OUTPUT
    # TODO: SMART FLATTEN BY UPDATED LAYER
    def flatten_layers(self):
        output = bytearray(512)
        # SORT BY PRIORITY: LOW -> HIGH
        self.layers.sort(key= attrgetter('priority'))
        for layer in self.layers:
            if layer.enabled:
                index = 0
                for addr in layer.data:
                    # HIGHEST TAKES PRESCEDENCE
                    if addr > output[index]: output[index] = addr
        self.output = output #& UPDATE SELF.OUTPUT
    
    
    #* UPDATE SELF.OUTPUT IF OUPUT_ON
    def update_output(self):
        if not self.output_on:
            if LOG_MSG: log.warning(f'update_output() -> OUTPUT_ON:{self.output_on}')
        else: # UPDATES SELF.OUTPUT FROM SELF.LAYERS
            self.flatten_layers()
    
    
    #* UPDATE LAYER BY NAME WITH DATA
    # TODO: ADD PARTIAL FRAMES
    def update_layer(self, layer_key : str, layer_data):
        for layer in self.layers:
            if layer_key == layer.name:
                if isinstance(layer_data, bytearray) and len(layer_data) is 512:
                    layer.data = layer_data
                else:
                    if LOG_MSG: log.debug(f'update_layer() -> layer_data:{type(layer_data)}')
                    

def test():
    with UnivCtrlr() as ctrlr:
        ctrlr.add_layer('Layer 1')
        ctrlr.add_layer('Layer 2')
        print(f'CTRL NAME:{ctrlr.ctrlr_name}')
        print(f'LAYERS:{len(ctrlr.layers)}')
        for layer in ctrlr.layers:
            print(f'LAYER NAME:{layer.name} | PRIORITY:{layer.priority} | ENABLED:{layer.enabled}')
        
        ctrlr.run()

test()