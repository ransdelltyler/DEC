



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
log = ColorLog('SACN_CTRL', level=1)


import sacn  #? LIBRARY: [sACN TX / RX]
import uuid  #? LIBRARY: UNIVERSAL UNIQUE ID GEN

#? FREE-SIMPLE-GUI + THEME
import FreeSimpleGUI as sg
sg.theme('DarkAmber')

#& DEFAULT EMPTY UNIVERSE OF DATA
EMPTY_UNIV = bytearray(512)


class sACNCtrlr:
    def __init__(self, name) -> None:
                
        #* CONTROLLER NAME
        self.name = name or 'DEFAULT SACN CTRLR'
        if LOG_MSG: log.info(f'CREATING: {self.name}')
        
        #* GUI SETUP
        if LOG_MSG: log.info(f'GUI INIT')
        self.layout = self.build_layout()
        self.window = sg.Window('DEC > sACN Controller', self.layout)

        #* SACN SENDER SETUP VARIABLES
        self.source_name = '- PYTHON -'
        if LOG_MSG: log.info(f' -> STARTING SENDER: {self.source_name}')
        self.multicast = False
        self.unicast_ip = '10.101.33.33'
        self.cid = uuid.UUID('1ACAA578-60C3-22D4-AA6F-577E7724B769').bytes
        self.universe = 1
        
        #* CREATE SENDER
        self.sender = sacn.sACNsender(source_name=self.source_name, cid=tuple(self.cid))
        self.sender.start()
        
        #* UNIVERSE DATA BUFFER LIST
        #* { UNIV : BYTEARRAY(512) }
        self.data_buffers = {}
        
        # TODO: SACN THREAD
        
        
    # CONTEXT MANAGERS
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sender.stop()
        return False
    
    
    #* START GUI LOOP
    def run(self):
        while True:
            event, values = self.window.read() # type: ignore
            if event == sg.WINDOW_CLOSED or event  == 'Cancel':
                break
            
    
#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#
    
    #* SETUP INITIAL GUI LAYOUT
    def build_layout(self) -> list:
        layout = [[sg.Text('Controller Active')], [sg.Button('Cancel')]]
        return layout
    



#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#

    #* ACTIVATE <UNIV>, ADD <UNIV> BUFFER
    def start_univ(self, univ : int) -> None:
        # CHECK IF UNIV IS ALREADY ACTIVE
        if univ in self.sender.get_active_outputs():
            if LOG_MSG: log.info(f'UNIV: {univ} IS ALREADY ACTIVE.')

        else: # UNIVERSE NOT ACTIVE 
            if LOG_MSG: log.info(f'ACTIVATING UNIV:{univ}...')
            #? START <UNIVERSE> OUTPUT
            self.sender.activate_output(univ)
        
        #? ADD BUFFER (CHECKS FOR DUPLICATES)
        self.new_buffer(univ=univ)

    
    #* CREATE NEW <EMPTY_UNIV> BUFFER FOR <UNIV>
    def new_buffer(self, univ : int) -> None:
        #? IF BUFFER <UNIV> DOESN'T EXIST YET CREATE ONE
        if univ not in self.data_buffers:
            if LOG_MSG: log.info(f'CREATING NEW UNIV:{univ} BUFFER')
            #? CREATE NEW BUFFER AND SET DATA (DEFAULT EMPTY)
            self.data_buffers[univ] = bytearray(512)
    
    
    #* DELETE BUFFER FOR <UNIV> IF EXISTS
    def remove_buffer(self, univ: int) -> None:
        if univ in self.data_buffers:
            if LOG_MSG: log.info(f'REMOVING UNIV:{univ} BUFFER')
            del self.data_buffers[univ] 
        else:
            if LOG_MSG: log.warning(f'REMOVE UNIV:{univ} BUFFER FAILED TO FIND')
            
    
    #* UPDATE <BUFFER_DATA[<UNIV>]> W/ <DATA>
    #* ( BYTES, BYTEARRAY, LIST, TUPLE ) -> UPDATE ALL OR START_ADDR FORWARD
    #* ( INT ) -> UPDATE START_ADDR LEVEL
    #* ( DICT ) -> UPDATE MULTIPLE ADDRESS LEVELS { ADDR : LEVEL, ... }
    def update_buffer(self, univ : int, data, start_addr : int = 1) -> None:
        #? ADD BUFFER FOR <UNIV> (CATCHES DUPLICATES)
        self.new_buffer(univ)
        start_index = start_addr - 1  # NORMALIZE ADDR INDEX
        
        #? ~LIST -> UPDATE FULL DMX FRAME
        if isinstance(data, (bytes, bytearray, list, tuple)):
            length = min( len(data), 512 - start_index ) # CAP DATA COPY TO UNIV LENGTH
            self.data_buffers[univ][start_index : start_index + length] = data[:length] #& UPDATE &#

        #? INTEGER -> UPDATE SINGLE ADDRESS
        elif isinstance(data, int):
            data = max(0, min(255, data)) # CLAMP TO VALID LEVEL
            self.data_buffers[univ][start_index] = data #& UPDATE &#
        
        #? DICT -> UPDATE SPECIFIC ADDRESSES
        elif isinstance(data, dict):
            for addr, lvl in data.items():
                if 0 <= addr-1 < 512: # CHECK FOR VALID DMX ADDRESS
                    lvl = max(0, min(255, lvl)) # CLAMP TO VALID LEVEL
                    self.data_buffers[univ][addr-1] = lvl #& UPDATE &#
        else: #? UNKNOWN -> SKIP
            if LOG_MSG: log.error(f'DATA IS UNSUPPORTED TYPE: {type(data)}')


    #* APPLY <BUFFER_DATA[<UNIV>]> TO <SELF.SENDER[UNIV]>
    def update_univ_data(self, univ : int) -> None:
        #? CHECK <UNIV> OUTPUT IS ACTIVE
        if univ in self.sender.get_active_outputs():
            universe = self.sender[univ]
            if universe:
                #? CHECK FOR DATA BUFFER
                if univ in self.data_buffers:
                    if LOG_MSG: log.info(f'FOUND UNIV:{univ} BUFFER')
                    # MANUAL_FLUSH SHOULD ONLY BE TRUE DURING DATA UPDATES, NEVER LEFT ON
                    #self.sender.manual_flush = True
                    #& !! - UPDATE OUTPUT UNIV DATA - !! &#
                    universe.dmx_data = self.data_buffers[univ]
                    #self.sender.manual_flush = False

                else:
                    if LOG_MSG: log.warning(f'UNIV:{univ} BUFFER DOES NOT EXIST... IGNORING UPDATE')
            else:
                if LOG_MSG: log.warning(f'SELF.SENDER[{univ}] ACTIVE, BAD <UNIVERSE=SELF.SENDER[{univ}]>')
        else: 
            if LOG_MSG: log.error(f'UNIV:{univ} NOT ACTIVE, IGNORING UPDATE')


    



