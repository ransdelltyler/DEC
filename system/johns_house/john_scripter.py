

#* ======================================================== *#
'''                    FILE DESCRIPTION                   






'''


#~ ======================================================== ~#
#~                       SCRIPT CLASS
#~ - MODULES -> SEQUENCE PACKS / FUNCTION GROUPS
#~     - SEQUENCES -> ORDERED MULTI-SCRIPT CALLS W/ TIMING
#~          - SCRIPT -> SINGLE CALLABLE FUNCTION
#~ ======================================================== ~#
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

log = ColorLog('_SCRIPT_', path='./logs/util_classes.txt')

from uuid import UUID, uuid4
from time import sleep
from dataclasses import dataclass, field
from typing import Callable, Dict, List
from enum import Enum

from pprint import pprint

# TODO: FUZZ-MATCH NAME SEARCH
DEF_SCRIPT_NAME = 'DEF_SCRIPT_NAME'
@dataclass
class Script:
    id : UUID = field(default_factory=uuid4)
    name: str = DEF_SCRIPT_NAME
    # SCRIPT FIELDS
    runs: int = 0
    params: dict = field(default_factory=dict)
    rtime_opt: dict = field(default_factory=dict)
    func: Callable = lambda: log.warning(f'SCRIPT.FUNC() NOT SET')


DEF_SEQ_NAME = 'DEF_SEQ_NAME'
@dataclass
class Sequence:
    id: UUID = field(default_factory=uuid4)
    name: str = DEF_SEQ_NAME
    # SEQUENCE FIELDS
    runs: int = 0
    params: dict = field(default_factory=dict)
    rtime_opt: dict = field(default_factory=dict)
    scripts: List[Script] = field(default_factory=list)
    # [ (SCRIPT_NAME, PRE_WAIT_MS, POST_WAIT_MS, **KWARGS) ]
    sequence: List[tuple] = field(default_factory=list)

    def run(self):
        pass

DEF_MODULE_NAME = 'DEF_MODULE_NAME'
@dataclass
class Module:
    id: UUID = field(default_factory=uuid4)
    name: str = DEF_MODULE_NAME
    
    # MODULE FIELDS
    scripts: List[Script] = field(default_factory=list)
    sequences: List[Sequence] = field(default_factory=list)
    
    def run(self):
        pass


#^ SCRIPT-TYPE ENUM FOR SEARCHING
class ScriptType(Enum):
    SCRIPT = 'script' or 'spt'
    SEQUENCE = 'sequence' or 'seq'
    MODULE = 'module' or 'mods' or 'mod'




#TODO: GET MODULES FROM SCRIPTS FOLDER
class ScriptManager:
    def __init__(self, name: str, ) -> None:
        self.uuid = uuid4()
        self.name = name or 'Script-Manager'
        
        # LOADED MODULES, SEQUENCES, SCRIPTS
        self.modules = []
        self.sequences = []
        self.scripts = []
        self.active = []

        
    #& CONTEXT MANAGER 1/2
    def __enter__(self):
        if gvars.LOG_MSG:
            log.border()
            log.watchdog(' STARTING ')
        return self
    #& CONTEXT MANAGER 2/2
    def __exit__(self, exc_type, exc_val, exc_tb):
        if gvars.LOG_MSG:
            log.watchdog(' SHUTTING DOWN ')
            log.border()
        return False

#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#

    #? ADD SCRIPT TO MANAGER
    def add_script(self, script: Script):
        self.scripts.append(script)
    #? ADD SEQUENCE OF SCRIPTS W/ DELAYS,PARAMS TO MANAGER
    def add_sequence(self, sequence):
        self.sequences.append(sequence)
    #? ADD MODULE OF SCRIPTS AND SEQUENCES TO MANAGER
    def add_module(self, module: Module):
        self.modules.append(module)

    # TODO: LINK WITH JOHN_FILES
    #? SAVE TO NEW FILE OR REGENERATE EXISTING
    def export_script(self):
        pass
    def export_sequence(self):
        pass
    def export_module(self):
        pass
    
    #? SAVE TO FILE
    def save_script(self):
        pass
    def save_sequence(self):
        pass
    def save_module(self):
        pass
    
    #? RUN THE PROVIDED TEST FUNCTION IN GIVEN SCRIPT|SEQUENCE|MODULE
    def run_test(self, item: Script | Sequence | Module):
        pass
    
    
    #TODO: ADD UUID BACKUP CHECK
    
    #? RUN SCRIPT - SINGLE SHOT
    def run_script(self, name: str):
        _ = [scr for scr in self.scripts if scr.name == name]
        if len(_) > 1:
            if gvars.LOG_MSG: log.error(f'FOUND {len(_)} MATCHING {name}')
            return #!EXIT!#
        else:
            _[0].run() # EXECUTE SCRIPT
    #? RUN MODULE - SINGLE SHOT
    def run_seq(self, name: str):
        _ = [seq for seq in self.sequences if seq.name == name]
        if 0 > len(_) > 1:
            if gvars.LOG_MSG: log.error(f'FOUND {len(_)} MATCHING {name}')
            return
        else:
            _[0].run()
            self.active.append(_)
            
    #? ADD SCRIPT TO ACTIVE LIST | OPTIONAL: RUN IMMEDIATELY
    def start_script(self, name: str, run_now=False):
        _ = [scr for scr in self.scripts if scr.name == name]
        if len(_) > 1:
            if gvars.LOG_MSG: log.error(f'FOUND {len(_)} MATCHING {name}; CANCELLING')
            return #!EXIT!#
        else:
            if run_now: _[0].run() # EXECUTE SCRIPT
            self.active.append(_)
    #? ADD SEQUENCE TO ACTIVE LIST | OPTIONAL: RUN IMMEDIATELY
    def start_sequence(self, name: str, run_now=False):
        _ = [seq for seq in self.sequences if seq.name == name]
        if len(_) > 1:
            if gvars.LOG_MSG: log.error(f'FOUND {len(_)} MATCHING {name}; CANCELLING')
            return #!EXIT!#
        else:
            if run_now: _[0].run() # EXECUTE SEQUENCE
            self.active.append(_) 
    
    #? LIST LOADED MEMBERS
    def list_modules(self):
        pprint(self.modules)
    #? ----------------------
    def list_sequences(self):
        pprint(self.sequences)
    #? ----------------------
    def list_scripts(self):
        pprint(self.scripts)
    #? ----------------------
    def list_all(self):
        self.list_scripts()
        self.list_sequences()
        self.list_modules()
    #? ----------------------

        
    #? FINDS AND RETURNS {SCRIPTS:[]/SEQUENCES:[]/MODULES:[]} THAT MATCH NAME
    def find_by_name(self, name: str):
        matches = { 'scripts' : [], 'sequences' : [], 'modules' : [] }
        for _ in self.scripts:
            if _.name == name: matches['scripts'].append(_)
        for _ in self.sequences:
            if _.name == name: matches['sequences'].append(_)
        for _ in self.modules:
            if _.name == name: matches['modules'].append(_)
        return matches                 
    
        
#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#
