 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
 #* PROJECT MANAGER
 #*
 #*
 #*
 #*
 #* ======================================================== *#

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from typing import Any, List, Tuple
from dataclasses import is_dataclass, fields

# GLOBAL VARIABLES IMPORT
from DEEREATCHAIN.system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

# GLOBAL VARIABLES IMPORT
from DEEREATCHAIN.system.gen.settings import *
from DEEREATCHAIN.system.utils.data_models import *
from DEEREATCHAIN.system.utils.factory import *
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

log = ColorLog('JOHN_PROJ')

 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

class JohnPM:
    def __init__(self, proj_path):
        
        #? TEMPORARY HOLDER FOR NEW PROJECTS
        self.temp_proj = []
        #? ACTIVE LOADED PROJECT
        self.cur_proj = Project
        self.cur_proj_path = proj_path
        #? PREVIOUS OPENED PROJECT PATH
        self.last_proj = Path
        
        #? WORKING PROJ-ELEMENT DICTIONARY
        self.working = {
            'anchors' : [],
            'rooms' : [],
            'installs' : [],
            'equipment' : [],
            'enclosures' : [],
            'ctrlrs' : [],
            'ledprods' : [],
            'terminals' : [],
            'cables' : [],
            'path3d' : [],
            'ledbranches' : [],
            'ledsegs' : [],
        }
        
        #? DELETED / RESTORABLE 
        self.trash = []




        
    #? MERGE { WORKING } -> { CURRENT }
    def working_proj_merge(self):
        self.working['']
        # TODO: MERGE LOGIC FOR COMMITTING WORKING -> PROJECTS


#? ======================================================== ?#
#?                  PROJECT OBJECT BUILDERS                 ?#
#? ======================================================== ?#
    
    #? CREATE NEW PROJECT
    def build_new_project(self, name:str,):
        self.temp_proj.append(new_project(name=name))
        # TODO: GET BASIC PROJ INFO & BUILD
    
    #? PROJ-OBJECT CREATION -> { WORKING }
    def create_anchor(self, name: str,): self.working['anchors'].append(new_anchor(name=name))
    def create_room(self, name: str,): self.working['rooms'].append(new_room(name=name))
    def create_install(self, name: str,): self.working['installs'].append(new_install(name=name))
    def create_equipment(self, name: str,): self.working['equipment'].append(new_equipment(name=name))
    def create_enclosure(self, name: str,): self.working['enclosures'].append(new_enclosure(name=name))
    def create_ctrlr(self, name: str,): self.working['ctrlrs'].append(new_ctrlr(name=name))
    def create_terminal(self, name: str,): self.working['terminals'].append(new_terminal(name=name))
    def create_ledprod(self, name: str,): self.working['ledprods'].append(new_ledprod(name=name))
    def create_branch(self, name: str,): self.working['branches'].append(new_ledbranch(name=name))
    def create_segment(self, name: str,): self.working['segments'].append(new_ledsegment(name=name))
    def create_path3d(self, name: str,): self.working['path3ds'].append(new_path3d(name=name))
    def create_cable(self, name: str,): self.working['cables'].append(new_cable(name=name))


#? ======================================================== ?#
#?                  PROJECT FILE OPERATIONS                 ?#
#? ======================================================== ?#
    
    def _save_project(self, name: str, path: str):
        pass 
    def _load_project(self, name: str, path: str):
        pass
    def _save_state(self, path:str):
        pass
    
    
#? ======================================================== ?#
#?                     HELPER FUNCTIONS                     ?#
#? ======================================================== ?#
    
    #? FIND <ATTR> W/ <VALUE> RECURSIVELY IN PROJ OBJ
    def find_in_proj(self, obj: Any, attr: str, value: str) -> list:
        output = []

        def _walk(o, path: str ):
            if not is_dataclass(o):
                return #!EXIT!#

            if hasattr(o, attr) and getattr(o, attr) == value:
                output.append((path,o)) 
            
            for f in fields(o):
                child = getattr(o, f.name)
                child_path = f'{path}.{f.name}'
                
                if is_dataclass(child):
                    _walk(child, child_path)
                
                elif isinstance(child, (list,tuple,set)):
                    for id_,item_ in enumerate(child):
                        if is_dataclass(item_):
                            _walk(item_,f'{child_path}[{id_}]')
                
                elif isinstance(child, dict):
                    for key, item in child.items():
                        if is_dataclass(item):
                            _walk(item,f"{child_path}['{key}']")

        _walk(obj, obj.__class__.__name__)
        return output #!EXIT!#
    
    #? FIND OBJS W/ <ATTR> = <VALUE> IN { WORKING }
    def find_in_working(self, attr:str, value: str):
        pass
    
    #? DEL OBJ IN { WORKING } BY <NAME> <OBJ_TYPE>
    def del_working_obj(self, name:str, type_:str):
        pass
    
    
#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#




#! ======================================================== !#
#!                       MAIN BLOCK                         !#
#! ======================================================== !#