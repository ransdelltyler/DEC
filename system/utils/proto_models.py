
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# GLOBAL VARIABLES IMPORT
from system.gen import gvars
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog


from typing import Any
import sacn
import uuid
from time import sleep
from dataclasses import dataclass, field

from util_classes import ColorLog
log = ColorLog('SACN_SEND', path='dmx_log.txt')

@dataclass
class Buffer512:
    data : bytearray = field(default_factory=lambda:bytearray(512))
    prio : bytearray = field(default_factory=lambda:bytearray(512))
    
    # CONVERT INT, LIST, TUPLE, DICT -> BYTEARRAY(512)
    def to_bytearray(self, input_: int | list | dict | tuple) -> bytearray:
        if isinstance(input_, dict):
            return bytearray(input_.values()) #!EXIT!#
        # INT | LIST | TUPLE
        return bytearray(input_) #!EXIT!#
    
    
    # ONLY ACCEPTS INPUTS OF LENGTH:512 AND SET ATTRIBUTES SAFELY 
    def __setattr__(self, name: str, value: list | tuple | dict | bytearray) -> None:
        if len(value) == 512:
            if name == 'data':
                if not isinstance(value, bytearray):
                    super().__setattr__(name, self.to_bytearray(value)) #!EXIT!#
            if name == 'prio':
                if not isinstance(value, bytearray):
                    super().__setattr__(name, self.to_bytearray(value)) #!EXIT!#
            else:
                super().__setattr__(name, value) #!EXIT!#
        else:
            if gvars.LOG_MSG: log.debug(f'SETATTR:{name} - LEN:{len(value)} FAILED.')


@dataclass
class Layer(Buffer512):
    name: str = ''
    
    
    
    

    
    
#~ ======================================================== ~#
#~                   DMX-CONTROLLER CLASS                   ~#
#~ ======================================================== ~#
CID_BYTES = uuid.UUID('1ACAA578-60C3-22D4-AA6F-577E7724B769').bytes
DEF_NAME = 'OCTAVO'
ADVATEK_IP = '10.101.33.33'
VIRT_NIC = '10.101.33.142'
DEF_UNIV = 1420

#~ SACN -> DMX-CONTROLLER HANDLER | OUTPUT ONLY
class DMX_CTRLR:
    def __init__(self, univ=DEF_UNIV, name=DEF_NAME, cid=tuple(CID_BYTES), destination=VIRT_NIC) -> None:
        self.dmx = Buffer512() # THE FINAL OUTPUT DMX -> SACN-SENDER
        self.layers = {}       # {LAYER : BUFFER512()}
        self.univ = univ       # SET UNIVERSE NUMBER
        self.sender = sacn.sACNsender(source_name=name, cid=cid)
        self.sender.start()    # STARTS THE SENDER (CAN HOLD MULTIPLE UNIVERSES)
        sleep(1)               # GIVE SENDER TIME TO START
        self.sender.activate_output(univ) # ADDS <UNIV> TO ACTIVE OUTPUTS (NO DMX OUTPUT)
        self.out = self.sender[self.univ] # HOLDS THE <DMX_DATA> PARAMETER FOR <SENDER><UNIV>
        assert self.out is not None, log.success(f'UNIV:{self.univ} STARTED')
        self.out.multicast = False
        self.out.destination = destination # RECIEVER IP 
        if gvars.LOG_MSG: log.success(f'DMX-CTRLR INIT')
        
        
    #& CONTEXT MANAGER 1/2
    def __enter__(self):
        if gvars.LOG_MSG: 
            log.border()
            log.watchdog(' DMX-CTRLR STARTING ')
        return self
    
    #& CONTEXT MANAGER 2/2
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sender.stop()
        if gvars.LOG_MSG:
            log.watchdog(f' DMX-CTRLR SHUTTING DOWN ')
            log.border()
        return False
    

    #? ACTIVATE NEW:<univ> OR EXISTING:<None> UNIVERSE OUTPUT 
    def start_univ(self, univ: int | None=None):
        if univ is None: 
            if univ not in self.sender.get_active_outputs():
                self.sender.activate_output(self.univ)
                if gvars.LOG_MSG:
                    log.success(f'ACTIVATED OUTPUT: {self.univ}')
                    log.debug(f'OUTPUTS ACTIVE: {self.sender.get_active_outputs()}')
        else:
            self.sender.move_universe(self.univ, univ)
    
    #? STOP UNIVERSE:<univ>        
    def stop_univ(self, univ: int | None):
        if univ is None: univ = self.univ
        self.sender.deactivate_output(univ)
    
    
    #? ADD LAYER 
    def addlayer(self, name: str, values):
        pass

#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#\
def test():
    from pprint import pprint # PRETTY PRINT
    
    # AUTOMATIC CLEANUP INSTANCE
    with DMX_CTRLR() as ctrlr:
        # SET AND START UNIVERSE (NO OUTPUT)
        ctrlr.start_univ(1)
        # SIMPLE DMX DATA
        data = bytearray(512)
        # FILL START:END WITH LEVEL:255
        data[:] = [255]*512
        ctrlr.dmx.data = data
        
        # ALL CURRENT ACTIVE OUTPUTS
        pprint(ctrlr.sender.get_active_outputs())
        # CTRLR CURRENT DMX VALUES
        pprint(ctrlr.dmx.data)
        
        sleep(20)
    

test()