


#* ======================================================== *#
'''                    FILE DESCRIPTION                   

SUB-SYSTEM DESIGNER MODULE
    - BUILDS SYSTEM ELEMENTS AND FIXTURE ASSEMBLIES
    - MANAGES DESIGN LOGIC
    - 



'''
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#

from uuid import uuid4, UUID
from ast import Dict
from dataclasses import field
from typing import ClassVar
from system.gen.settings import LOG_MSG
from system.utils.data_models import PSU, Accessory, Enclosure, Terminal
from system.utils.design_models import Cable, Controller, Fixture

from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_DSGN')


class JohnDesigner:
    def __init__(self):
        
        self.current_project = None
        
        self.selection = None
        self.previous_selection = None
        
        #? HOLDS FULL OBJECTS RETRIEVED FROM DATABASE
        #? ONLY ELEMENTS USED IN THE CURRENT PROJECT
        self.base_elements = dict = field(default_factory=lambda: {
            'fixtures' : [],
            'controllers' : [],
            'enclosures' : [],
            'accessories' : [],
            'psus' : [],
            'cables' : [],
            'terminals' : [],
        })
        
        
        #* HOLDS ALL ELEMENTS ADDED TO THE CURRENT PROJECT
        #? DUPLICATES, VARIANTS, CUSTOMIZED INSTANCES, ETC.
        #? USED FOR STORING UNORGANIZED LISTS OF ELEMENTS
        #? e.g. BEFORE BEING SORTED INTO PROJECT ELEMENTS
        self.elements = dict = field(default_factory=lambda: {
            'fixtures' : [],
            'controllers' : [],
            'enclosures' : [],
            'accessories' : [],
            'psus' : [],
            'cables' : [],
            'terminals' : [],
        })
        
        #? HOLDS LISTS OF UNIQUE PROJECT ELEMENT IDS
        #? USED FOR QUICK ACCESS TO ELEMENTS
        self.project_elements = dict = field(default_factory=lambda: {
            'fixtures' : [],
            'controllers' : [],
            'enclosures' : [],
            'accessories' : [],
            'psus' : [],
            'cables' : [],
            'terminals' : [],
        })
        
        #? TYPE MAP FOR ELEMENT LISTS        
        self.type_maps = dict = field(default_factory=lambda: {
            Fixture : 'fixtures',
            Controller : 'controllers',
            Enclosure : 'enclosures',
            Accessory : 'accessories',
            PSU : 'psus',
            Cable : 'cables',
            Terminal : 'terminals',
        })
        
        #? ELEMENT_ID MAP IN SEQUENCE OF CONNECTIONS
        #? |-       BRANCH 1            -| |-  BRANCH 1B  -|-  BRANCH 2A   -|
        #? [[element_id, element_id, ...], [element_id,...],[element_id,...]]
        self.maps = field(default_factory= list[dict])
    
    
    

    

#? ======================================================== ?#
#?                  MANAGEMENT FUNCTIONS                    ?#
#? ======================================================== ?#
    #? RAW DATABASE ELEMENT MANAGEMENT
    #? HOLDS ELEMENTS W/ BASE SPECS FROM DB
    def add_base_element(self, element: 
            Fixture | Controller | Enclosure | 
            Accessory | PSU | Cable | Terminal):
        
        target_key = self.type_maps.get(type(element))
        
        if target_key:
            self.base_elements[target_key].append(element)
        else:
            if LOG_MSG: log.error(f'Element type {type(element)} not recognized.')
    
    
    #? PROJECT ELEMENT MANAGEMENT
    #? ADD / EDIT / REMOVE ELEMENTS FROM PROJECT
    #? BASE ELEMENTS RETRIEVED FROM DATABASE AND STORED IN: { BASE_ELEMENTS }:
    def add_element(self, element: 
            Fixture | Controller | Enclosure | 
            Accessory | PSU | Cable | Terminal):
        target_key = self.type_maps.get(type(element))
        
        if target_key:
            self.project_elements[target_key].append(element)
        else:
            if LOG_MSG: log.error(f'Element type {type(element)} not recognized.')
    
    
    #? UPDATE MUTABLE ELEMENT PARAMETERS
    #? E.G. PROJ UNIQUE NAME, COMMENTS, RATED_WATTS, ETC.
    def edit_element(self, element_id: UUID, **kwargs):
        element = self.find_in_proj(element_id)
        
        valid_fields = {field.name for field in fields(element)}
        
        for key, value in kwargs.items():
            if key in valid_fields: setattr(element, key, value)
            elif: LOG_MSG: log.warning(f'PARAMETER {key}:{value} MISSING FROM ELEM.')
            
    
 
    
    #? REMOVE ELEMENT FROM PROJECT
    #? 
    def rem_projID(self, element_id: UUID | str):
        target_id = element_id if isinstance(element_id, UUID) else UUID(element_id)

        for key, elements in self.project_elements.items():
            for element in elements:
                if element.id_base == target_id:
                    elements.remove(element)
                    if LOG_MSG: log.info(f'Removed element {element.name} ({element.id_base}) from project.')
                    return  #!EXIT!#
        if LOG_MSG: log.warning(f'Element ID {element_id} not found in project elements.')

    
    #~ NOT SURE IF I NEED THIS
    def find_in_proj(self, element_id: UUID):
        target_id = element_id if isinstance(element_id, UUID) else UUID(element_id)
        
        for key, elements in self.project_elements.items():
            for element in elements:
                if element.id_base == target_id:
                    if LOG_MSG: log.info(f'Found element {element.name} ({element.id_base}) in project.')
                    return element
        if LOG_MSG: log.warning(f'Element ID {element_id} not found in project elements.')
        return None


#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#



#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#






#! ======================================================== !#
#!                       MAIN BLOCK                         !#
#! ======================================================== !#