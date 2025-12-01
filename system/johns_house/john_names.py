
#* ======================================================== *#
#*                   - FILE DESCRIPTION -
#*
#*  JOHN-NAMES : RANDOM NAME GENERATOR MODULE
#*  - USES NAME_BUCKET FOR POSSIBLE WORDS SPLIT BY CATEGORY
#* 
#*  FUNCTIONS: (RETURNS NONE IF GENERATION FAILED)
#?  - get_set( setname:str ) 
#*      -> [str] of setname
#?  - rand_word( setname:str ) 
#*      -> str of setname 
#?  - first_last( ) 
#*      -> str (FirstName_LastName)
#?  - person_title( prefix:bool, suffix:bool ) 
#*      -> str (Prefix_Firstname_LastName_Suffix)
#?  - name_thing( name:str, aura:Enum )
#*      -> str (Aura_Noun)
#*  
#* ======================================================== *#


# GLOBAL DEFAULT STRINGS
NAME_BUCKET = {
    #? FIRST NAMES - CANNOT BE JOHN
    'fname'  : ['',

        
    ],
    
    #? LAST NAMES - CANNOT BE JOHN
    'lname' : ['',
        
        
    ],
    
    #? TITLES
    'title' : ['',
        
        
    ],
    
    #? FAMOUS FIRST NAME
    'ffame' : ['',

        
    ],
    
    #? FAMOUS LAST NAME
    'lfame' : ['',

        
    ],

    #? PHYSICAL OBJECT
    'thing'  : ['',

        
    ],
    
    #? NON-PHYSICAL IDEA / CONCEPT
    'idea'  : ['',
        
        
    ],
    
    #? ADJECTIVE DESCRIPTOR
    'adjtv' : ['',

        
    ],

    #? LOCATION
    'place' : ['',

        
    ],
}
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
log = ColorLog('JOHN_KEYB')

import random

#~ ======================================================== ~#
#~                   NAME-GENERATOR CLASS                   ~#
#~ ======================================================== ~#
class JohnNames:
    def __init__(self) -> None:
        if gvars.LOG_MSG: log.info('STARTING JOHN-NAMES')

    
    
    #& WITH CONTEXT MANAGER 1/2
    def __enter__(self):
        return self
    
    #& WITH CONTEXT MANAGER 2/2
    def __exit__(self, exc_type, exc_val, exc_tb):
        if gvars.LOG_MSG:
            log.watchdog(f' DMX-CTRLR SHUTTING DOWN ')
            log.border()
        return False
        
    
    #? RETRIEVE SET FROM <NAME> INPUT
    def get_set(self, name: str,) -> list | None:
        if name in NAME_BUCKET:
            return NAME_BUCKET.get(name)
        else:
            if gvars.LOG_MSG: log.error(f'COULD NOT FIND: {name}')
            return None
    
    #? RETURN A RANDOM WORD OF <SET> or DEFAULT
    def rand_word(self, sel_set: str) -> str | None:
        word_set = self.get_set(sel_set)
        if word_set:
            return random.choice(word_set)
        else:
            if gvars.LOG_MSG: log.error(f'rand_word() - FAILED')
            return None
    
    # TODO: ADD DUPLICATE CHOICE CATCH
    #? GENERATE RANDOM FIRST-NAME_LAST-NAME
    def first_last(self) -> str | None:
        fname_set = self.get_set('fname') # FIRST NAME
        lname_set = self.get_set('lname') # LAST NAME 

        if fname_set and lname_set:
            return random.choice(fname_set) + '_' + random.choice(lname_set) #!EXIT!#
        else:
            log.warning('rand_flname() - FAILED') # CATCH MISSING SETS
            return None
        
        
    def name_title(self, mod):
        # TODO: MOD -> CHANGES TITLE COMPLEXITY
        pass
    
    
    def name_thing(self, mod, aura):
        # TODO: MOD -> CHANGES NAME TYPE
        # TODO: AURA -> CHANGES POSITIVE / NEGATIVE
        pass
    
    
    