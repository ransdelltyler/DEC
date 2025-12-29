



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
from enum import Enum, auto

#? FREE-SIMPLE-GUI + THEME
import FreeSimpleGUI as sg
sg.theme('DarkAmber')

EMPTY_UNIV = bytearray(512)
DEF_NAME = '- PYTHON SACN CTRLR -'
DEF_UNIV = 1
DEF_RX_DELAY = 1/30
DEF_TX_DELAY = 1/30
DEF_GUI_TIMEOUT = 100
DEF_IP = '10.101.33.33'
DEF_CID = uuid.UUID('1ACAA578-60C3-22D4-AA6F-577E7724B769').bytes

class BufferType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    

class sACNCtrlr:
    def __init__(self, name : str = DEF_NAME, univ : int = 1, ) -> None:
                
        #* CONTROLLER NAME
        self.name = name
        if LOG_MSG: log.info(f'CREATING: {self.name}')
        
        #* GUI SETUP
        if LOG_MSG: log.info(f'GUI INIT')
        self.layout = self.build_layout()
        self.window = sg.Window('DEC > sACN Controller', self.layout)

        #* SACN SENDER / RECIEVER SETUP
        #? EACH HOLDS MULTIPLE UNIVERSES 
        
        
        
        #* UNIVERSE DATA BUFFER LISTS
        #? { UNIV : BYTEARRAY(512) }
        self.output_buffers = {}
        self.input_buffers = {}

        #* MAP FOR CONNECTING BUFFERS IN -> OUT
        #? { IN_UNIV : [OUT_UNIV, OUT_UNIV]}
        self.univ_patch = {}
        
        
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
            if LOG_MSG: log. success(f'sACNRX THREAD SHUTDOWN')
        if hasattr(self, 'sacnTX_thread') and self.sacnTX_thread.is_alive():
            # WAIT FOR TX TO FINISH ACTIVE LOOP THEN SHUT DOWN
            self.sacnTX_thread.join(timeout=1.0)
            self.sacn_rx.stop()
            if LOG_MSG: log. success(f'sACNTX THREAD SHUTDOWN')
        if hasattr(self, 'window'):
            self.window.close()
            if LOG_MSG: log. success(f'WINDOW SHUTDOWN')
    
    
    
    #* START SACN SENDER AND THREAD FOR DATA UPDATES
    def start_tx(self,
                 source_name = DEF_NAME,
                 multicast = False,
                 unicast_ip = DEF_IP,
                 cid = DEF_CID,
                 universe = DEF_UNIV,
                 tx_delay = DEF_TX_DELAY) -> sacn.sACNsender:
        
        #? TX CREATION
        self.sacn_tx = sacn.sACNsender(source_name=source_name, cid=tuple(cid))
        self.sacn_tx.start()
        if self.sacn_tx and LOG_MSG: log.success(
            f'|+sACN TRANSMITTER CREATED \n' + 
            f'||SOURCE-NAME:{source_name}|MCAST:{multicast}|UCAST IP:{unicast_ip}|UNIVERSE:{universe}')
        
        #& STARTS TRANSMITTER THREAD | UPDATES ACTIVE UNIV DMX DATA BASED ON BUFFER DATA
        self.sacnTX_thread = threading.Thread( target=self.loop_sacnTX(tx_delay=tx_delay), daemon=True)
        self.sacnTX_thread.start()
        if self.sacnTX_thread: self.tx_ON = True
        
        return self.sacn_tx #!EXIT!# 


    #* START SACN RECIEVER AND THREAD FOR DATA UPDATES
    def start_rx(self, rx_bind_addr = DEF_IP, rx_delay = DEF_RX_DELAY) -> sacn.sACNreceiver:
        #? RX CREATION
        self.sacn_rx = sacn.sACNreceiver(bind_address=rx_bind_addr)
        self.sacn_rx.start()
        if self.sacn_rx and LOG_MSG: log.success(
            f'+ sACN RECEIVER CREATED \n' +
            f'||BOUND-INPUT-ID:{rx_bind_addr}|UPDATE-DELAY:{rx_delay}')
        
        #& STARTS RECIEVING THREAD | UPDATES BUFFERS BASED ON RX.ACTIVE UNIVERSES
        self.sacnRX_thread = threading.Thread( target=self.loop_sacnRX(rx_delay=rx_delay), daemon=True)
        self.sacnRX_thread.start()
        if self.sacnRX_thread: self.rx_ON = True
        
        return self.sacn_rx #!EXIT!#
    
    
    
    #* CALLED WHEN ANY SACN PACKET ARRIVES
    #? REGISTER (INPUT) LISTENERS -> reciever.register_listener()
    def _new_data_ready(self, packet): #(sacn.DataPacket)
        if packet.dmxStartCode == 0x00:
            univ = packet.universe
            data = packet.dmxData
            self.update_buffer(type_=BufferType.INPUT, univ=univ, lvls=data)
            
            
    
    #* SACN RECIEVER LOOP
    #? SACN UPDATE DATA BUFFERS WITH DATA FROM RECIEVED FRAMES
    def loop_sacnRX(self, rx_delay = DEF_RX_DELAY):
        while self.rx_ON:
            active_univs = []
            for univ in active_univs:
                # TODO: GET INPUT DATA FRAMES
                pass
            sleep(rx_delay)
    
    
    #* SACN TRANSMITTER LOOP
    #? SACN UPDATE <SACN_TX>(ACTIVE UNIVERSES) WITH BUFFER VALUES
    def loop_sacnTX(self, tx_delay):
        while self.tx_ON:
            active_univs = self.sacn_tx.get_active_outputs()
            for univ in active_univs:
                if univ in self.output_buffers:
                    self.update_univ_data(univ)
            sleep(tx_delay)
    
    
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
                   
        
        self.gui_runs = False


    # TODO: INFINITE DAEMONS
    # TODO: HTP LAYERS 
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
    def start_univ(self, univ : int, type_ : BufferType) -> None:
        # CHECK IF UNIV IS ALREADY ACTIVE
        if univ in self.sacn_tx.get_active_outputs():
            if LOG_MSG: log.info(f'UNIV: {univ} IS ALREADY ACTIVE.')

        else: # UNIVERSE NOT ACTIVE 
            if LOG_MSG: log.info(f'ACTIVATING UNIV:{univ}...')
            #? START <UNIVERSE> OUTPUT
            self.sacn_tx.activate_output(univ)
        
        #? ADD BUFFER (CHECKS FOR DUPLICATES)
        self.new_buffer( univ=univ, type_=type_)

    
    #* CREATE NEW <EMPTY_UNIV> BUFFER FOR <UNIV>
    def add_or_get_buffer(self, univ : int, type_: BufferType) -> bytearray | None:
        #? INPUT BUFFERS
        if type_ is BufferType.INPUT:
            if univ not in self.input_buffers:
                # CREATE NEW BUFFER AND SET DATA (DEFAULT EMPTY)
                if LOG_MSG: log.info(f'CREATING NEW INPUT UNIV:{univ} BUFFER')
                self.input_buffers[univ] = bytearray(512)
            return self.input_buffers[univ] #!EXIT!# 
        
        #? OUTPUT BUFFERS
        elif type_ is BufferType.OUTPUT:
            if univ not in self.output_buffers:
                # CREATE NEW AND SET DATA (DEFAULT EMPTY)
                if LOG_MSG: log.info(f'CREATING NEW OUTPUT UNIV:{univ} BUFFER')            
                self.output_buffers[univ] = bytearray(512)
            return self.output_buffers[univ] #!EXIT!#
        
        else: # CATCH: UNSUPPORTED TYPES
            if LOG_MSG: log.error(f'new_buffer() GOT UNSUPPORTED BUFFER TYPE:{type_}')
            return None #!EXIT!#
     
    #* DELETE BUFFER FOR <UNIV> IF EXISTS
    def remove_buffer(self, univ: int, type_: BufferType) -> None:
        #? INPUT BUFFERS
        if type_ is BufferType.INPUT:
            if univ not in self.input_buffers:
                # CREATE NEW BUFFER AND SET DATA (DEFAULT EMPTY)
                if LOG_MSG: log.info(f'DELETING INPUT UNIV:{univ} BUFFER')
                del self.input_buffers[univ]
            elif LOG_MSG: log.debug(f'UNIV:{univ} BUFFER NOT IN INPUTS')
        
        #? OUTPUT BUFFERS
        elif type_ is BufferType.OUTPUT:
            if univ not in self.output_buffers:
                # CREATE NEW AND SET DATA (DEFAULT EMPTY)
                if LOG_MSG: log.info(f'DELETING OUTPUT UNIV:{univ} BUFFER')            
                del self.output_buffers[univ]
            elif LOG_MSG: log.debug(f'UNIV:{univ} BUFFER NOT IN OUTPUTS')
                
        #? UNSUPPORTED TYPES
        else:
            if LOG_MSG: log.error(f'new_buffer() GOT UNSUPPORTED BUFFER TYPE:{type_}')
                
    
    #* UPDATE <BUFFER_DATA[<UNIV>]> W/ <DATA>
    #? ( BYTES, BYTEARRAY, LIST, TUPLE ) -> UPDATE ALL OR START_ADDR FORWARD
    #? ( INT ) -> UPDATE START_ADDR LEVEL
    #? ( DICT ) -> UPDATE MULTIPLE ADDRESS LEVELS { ADDR : LEVEL, ... }
    def update_buffer(self, univ : int, type_ : BufferType, lvls, start_addr : int = 1) -> None:
        buffer = self.add_or_get_buffer(univ=univ, type_=type_)
  
        #? UPDATE BUFFER DATA
        if buffer is not None:    
            start_index = start_addr - 1  # NORMALIZE ADDR INDEX
            #? ~LIST -> UPDATE FULL DMX FRAME
            if isinstance(lvls, bytearray):
                length = min( len(lvls), 512 - start_index ) # CAP DATA COPY TO UNIV LENGTH
                #& UPDATE BUFFER DATA &#
                buffer[start_index : start_index + length] = lvls[:length] 
            else: # CATCH: UNSUPPORTED DATA TYPE ERROR
                if LOG_MSG: log.error(f'DATA IS UNSUPPORTED TYPE: {type(lvls)}')
        else: # CATCH: BUFFER DIDN'T RESOLVE CORRECTLY
            if LOG_MSG: log.debug(f'update_buffer() RESOLVED TEMP BUFFER AS:{type(buffer)}')
        
    
    
    #* APPLY <BUFFER_DATA[<UNIV>]> TO <SELF.SACN_TX[UNIV]>
    def update_univ_data(self, univ : int) -> None:
        #? CHECK <UNIV> OUTPUT IS ACTIVE
        if univ in self.sacn_tx.get_active_outputs():
            universe = self.sacn_tx[univ]
            if universe:
                #? CHECK FOR DATA BUFFER
                if univ in self.output_buffers:
                    if LOG_MSG: log.info(f'FOUND UNIV:{univ} BUFFER')
                    self.sacn_tx.manual_flush = True # ONLY BE TRUE DURING DATA UPDATES
                    #& !! - UPDATE OUTPUT UNIV DATA - !! &#
                    universe.dmx_data = self.output_buffers[univ]
                    self.sacn_tx.manual_flush = False # NEVER LEAVE ON

                else: # CATCH: MISSING BUFFER
                    if LOG_MSG: log.warning(f'UNIV:{univ} BUFFER DOES NOT EXIST... IGNORING UPDATE')
            else: # CATCH: BAD UNIVERSE INIT
                if LOG_MSG: log.warning(f'SELF.SACN_TX[{univ}] ACTIVE, BAD <UNIVERSE=SELF.SACN_TX[{univ}]>')
        else: # CATCH: INACTIVE UNIVERSE
            if LOG_MSG: log.error(f'UNIV:{univ} NOT ACTIVE, IGNORING UPDATE')


    
def test():
    with sACNCtrlr(name = '- PYTHON sACNCTRLR -') as ctrlr:
        pass