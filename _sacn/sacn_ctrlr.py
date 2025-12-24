



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
import threading
from time import sleep

#? FREE-SIMPLE-GUI + THEME
import FreeSimpleGUI as sg
sg.theme('DarkAmber')

#& DEFAULT EMPTY UNIVERSE OF DATA
EMPTY_UNIV = bytearray(512)
DEF_NAME = '- PYTHON SACN CTRLR -'
DEF_UNIV = 1
DEF_IN_DELAY = 1/30
DEF_OUT_DELAY = 1/30
DEF_GUI_TIMEOUT = 100

class sACNCtrlr:
    def __init__(self, name : str = DEF_NAME, univ : int = 1, ) -> None:
                
        #* CONTROLLER NAME
        self.name = name
        if LOG_MSG: log.info(f'CREATING: {self.name}')
        
        #* GUI SETUP
        if LOG_MSG: log.info(f'GUI INIT')
        self.layout = self.build_layout()
        self.window = sg.Window('DEC > sACN Controller', self.layout)


        #* SACN TRANSMITTER INIT
        #? TX VARIABLES
        self.source_name = self.name
        if LOG_MSG: log.info(f' -> STARTING SACN_TX: {self.source_name}')
        self.multicast = False
        self.unicast_ip = '10.101.33.33'
        self.cid = uuid.UUID('1ACAA578-60C3-22D4-AA6F-577E7724B769').bytes
        self.universe = DEF_UNIV
        self.tx_delay = DEF_OUT_DELAY
        #? TX CREATION
        self.sacn_tx = sacn.sACNsender(source_name=self.source_name, cid=tuple(self.cid))
        self.sacn_tx.start()
        if self.sacn_tx and LOG_MSG: log.success(
            f'|+sACN TRANSMITTER CREATED \n' + 
            f'||SOURCE-NAME:{self.source_name}|MCAST:{self.multicast}|UCAST IP:{self.unicast_ip}|\n'
            f'||')

        #* SACN RECIEVER INIT
        #? RX VARIABLES
        self.rx_bind_addr = ''
        self.rx_delay = DEF_IN_DELAY
        #? RX CREATION
        self.sacn_rx = sacn.sACNreceiver(bind_address=self.rx_bind_addr)
        self.sacn_rx.start()
        if self.sacn_rx and LOG_MSG: log.success(
            f'+ sACN RECEIVER CREATED \n' +
            f'||BOUND-INPUT-ID:{self.rx_bind_addr}|UPDATE-DELAY:{self.rx_delay}')
        # TODO: COLORLOG [STRING] FORMATTING
        
        #* UNIVERSE DATA BUFFER LISTS
        #? { UNIV : BYTEARRAY(512) }
        self.output_buffers = {}
        self.input_buffers = {}
    
        
        
     #^ CONTEXT MANAGER FUNCTIONS
    #? RETURN SCRAPER INSTANCE FOR USE IN WITH STATEMENTS
    def __enter__(self):
        self.running = False
        return self

    #? GUARANTEED SELENIUM CLEANUP @ EXIT 
    def __exit__(self, exc_type, exc_val, exc_tb):
        #? STOP GUI
        self.gui_runs = False
        
        #? CLEAN SHUTDOWN TX + RX THREADS
        if hasattr(self, 'sacnRX_thread') and self.sacnRX_thread.is_alive():
            # WAIT FOR RX TO FINISH ACTIVE LOOP THEN SHUT DOWN
            self.sacnRX_thread.join(timeout=1.0)
            self.sacn_tx.stop()
        if hasattr(self, 'sacnTX_thread') and self.sacnTX_thread.is_alive():
            # WAIT FOR TX TO FINISH ACTIVE LOOP THEN SHUT DOWN
            self.sacnTX_thread.join(timeout=1.0)
            self.sacn_rx.stop()
        
    
    
    #? START SACN_TX NETWORK SACN RX + TX THREADS
    def start_netw(self):
        #? SACN_TX INPUT - SACN RECIEVERS
        self.sacnRX_thread = threading.Thread( target=self.loop_sacnRX(), daemon=True)
        self.sacnRX_thread.start()
        if self.sacnRX_thread: self.rx_ON = True
        
        #? SACN_TX OUTPUT - SACN TRANSMITTERS
        self.sacnTX_thread = threading.Thread( target=self.loop_sacnTX(), daemon=True)
        self.sacnTX_thread.start()
        if self.sacnTX_thread: self.tx_ON = True
        
    
    
    #? SACN RECIEVER LOOP
    def loop_sacnRX(self):
        while self.tx_ON:
            active_univs = []
            for univ in active_univs:
                # TODO: GET INPUT DATA FRAMES
                pass
            sleep(self.tx)
    
    #? SACN UPDATE <SACN_TX> WITH 
    def loop_sacnTX(self):
        while self.rx_ON:
            active_univs = self.sacn_tx.get_active_outputs()
            for univ in active_univs:
                if univ in self.data_buffers:
                    self.update_univ_data(univ)
            sleep(self.packet_delay)
    
    # TODO: INFINITE DAEMONS
    
    #* START GUI LOOP
    def run(self):
        # TRUE WHILE GUI IS ACTIVE
        self.gui_runs = True
        
        if LOG_MSG: log.success(f'STARTED THREADS')
        
        while True:
            #? GET EVENTS FROM GUI, (sg.WINDOW_CLOSED REQUIRED)
            event, values = self.window.read(timeout=DEF_GUI_TIMEOUT) # type: ignore
            if event == sg.WINDOW_CLOSED or event  == 'Cancel':
                break
            
            if event == 'START-OUTPUT':
                self.update_buffer(univ=1, lvls=1)
        
        
        self.gui_runs = False
    
#? ======================================================== ?#
#?                     GUI FUNCTIONS                        ?#
#? ======================================================== ?#
    
    #* SETUP INITIAL GUI LAYOUT
    def build_layout(self) -> list:
        layout = [[sg.Text('Controller Active')], [sg.Button('Cancel')]]
        return layout
    


#? ======================================================== ?#
#?                  SACN-CTRLR FUNCTIONS                    ?#
#? ======================================================== ?#

    
    #* ACTIVATE <UNIV>, ADD <UNIV> BUFFER
    def start_univ(self, univ : int) -> None:
        # CHECK IF UNIV IS ALREADY ACTIVE
        if univ in self.sacn_tx.get_active_outputs():
            if LOG_MSG: log.info(f'UNIV: {univ} IS ALREADY ACTIVE.')

        else: # UNIVERSE NOT ACTIVE 
            if LOG_MSG: log.info(f'ACTIVATING UNIV:{univ}...')
            #? START <UNIVERSE> OUTPUT
            self.sacn_tx.activate_output(univ)
        
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
    def update_buffer(self, univ : int, lvls, start_addr : int = 1) -> None:
        #? ADD BUFFER FOR <UNIV> (CATCHES DUPLICATES)
        self.new_buffer(univ)
        start_index = start_addr - 1  # NORMALIZE ADDR INDEX
        
        #? ~LIST -> UPDATE FULL DMX FRAME
        if isinstance(lvls, (bytes, bytearray, list, tuple)):
            length = min( len(lvls), 512 - start_index ) # CAP DATA COPY TO UNIV LENGTH
            self.data_buffers[univ][start_index : start_index + length] = lvls[:length] #& UPDATE &#

        #? INTEGER -> UPDATE SINGLE ADDRESS
        elif isinstance(lvls, int):
            lvls = max(0, min(255, lvls)) # CLAMP TO VALID LEVEL
            self.data_buffers[univ][start_index] = lvls #& UPDATE &#
        
        #? DICT -> UPDATE SPECIFIC ADDRESSES
        elif isinstance(lvls, dict):
            for addr, lvl in lvls.items():
                if 0 <= addr-1 < 512: # CHECK FOR VALID DMX ADDRESS
                    lvl = max(0, min(255, lvl)) # CLAMP TO VALID LEVEL
                    self.data_buffers[univ][addr-1] = lvl #& UPDATE &#
        #? UNKNOWN -> SKIP
        else:
            if LOG_MSG: log.error(f'DATA IS UNSUPPORTED TYPE: {type(lvls)}')
        

    #* APPLY <BUFFER_DATA[<UNIV>]> TO <SELF.SACN_TX[UNIV]>
    def update_univ_data(self, univ : int) -> None:
        #? CHECK <UNIV> OUTPUT IS ACTIVE
        if univ in self.sacn_tx.get_active_outputs():
            universe = self.sacn_tx[univ]
            if universe:
                #? CHECK FOR DATA BUFFER
                if univ in self.data_buffers:
                    if LOG_MSG: log.info(f'FOUND UNIV:{univ} BUFFER')
                    # MANUAL_FLUSH SHOULD ONLY BE TRUE DURING DATA UPDATES, NEVER LEFT ON
                    #self.sacn_tx.manual_flush = True
                    #& !! - UPDATE OUTPUT UNIV DATA - !! &#
                    universe.dmx_data = self.data_buffers[univ]
                    #self.sacn_tx.manual_flush = False

                else:
                    if LOG_MSG: log.warning(f'UNIV:{univ} BUFFER DOES NOT EXIST... IGNORING UPDATE')
            else:
                if LOG_MSG: log.warning(f'SELF.SACN_TX[{univ}] ACTIVE, BAD <UNIVERSE=SELF.SACN_TX[{univ}]>')
        else: 
            if LOG_MSG: log.error(f'UNIV:{univ} NOT ACTIVE, IGNORING UPDATE')


    
def test():
    with sACNCtrlr(name = '- PYTHON sACNCTRLR -') as ctrlr:
        ctrlr.