



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

DEF_CTRL_NAME = '-UNIV CONTROLLER-'
DEF_UNIV_DATA = bytearray(512)
DEF_PRIORITY = 100
DEF_START_ADDR = 1



@dataclass(slots=True, kw_only=True)
class Layer:
    name : str | None = DEF_CTRL_NAME
    priority : int | None = DEF_PRIORITY
    start_addr : int | None = DEF_START_ADDR
    data : bytearray = field(default_factory=bytearray)





class UnivCtrlr:
    def __init__(self, name : str | None = DEF_CTRL_NAME,) -> None:
        self.ctrlr_name = name
        
        #? FULL UNIVERSE DATA OUPUT
        self.output = DEF_UNIV_DATA

        self.layers = []
        
    
    #? CREATE NEW LAYER WITH NAME OR NEXT INDEX
    def add_layer(self, name : str | None = None ):
        if name: 
            self.layers.append(Layer(name=name, data=DEF_UNIV_DATA))
        else: # DEFAULT NAME TO NEXT LAYER LIST INDEX
            next_index = len(self.layers)-1
            self.layers[next_index] = Layer(data=DEF_UNIV_DATA)
    
    w
    #? USE PRIORITY TO UPDATE SELF.OUTPUT
    def flatten_layers(self):
        output = bytearray(512)
        # SORT BY PRIORITY: LOW -> HIGH
        self.layers.sort(key= attrgetter('priority'))
        for layer in self.layers:
            index = 0
            for addr in layer.data:
                # HIGHEST TAKES PRESCEDENCE
                if addr > output[index]: output[index] = addr
        self.output = output #& UPDATE SELF.OUTPUT
    
    
    