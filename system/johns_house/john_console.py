

#* ======================================================== *#
'''                    FILE DESCRIPTION                   

TERMINAL INTERPRETER MODULE
- BASE FOR SIMPLE/SHORTHAND LANGUAGE INTERPRETATION
- LOADS A MAP OF KEYWORD : ACTION GROUPS 


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

# GLOBAL VARIABLES IMPORT
from system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_CONSOLE')


#* ======================================================== *#
#*                 DEFAULT CONSOLE COMMANDS                 *#
#* ======================================================== *#
from enum import Enum, auto

class SYS_CMDS(Enum):
    HELP    = 'help'
    EXIT    = 'exit'
    QUIT    = 'quit'
    LIST    = 'list'
    LOAD    = 'load'
    SAVE    = 'save'
    UNDO    = 'undo'
    REDO    = 'redo'
    RUN     = 'run'
    STATUS  = 'status'
    CLEAR   = 'clear'
    RESET   = 'reset'
    TRIGGER = 'trigger'
    CONFIG  = 'config'
    SET     = 'set'
    GET     = 'get'
    DELETE  = 'delete'
    ADD     = 'add'
    EXPORT  = 'export'
    IMPORT  = 'import'
    LOG     = 'log'
    
class FILE_CMDS(Enum):
    NEW_FILE    = 'new_f'
    LOAD_FILE   = 'load_f'
    SAVE_FILE   = 'save_f'
    CLOSE_FILE  = 'close_f'
    LIST_FILES  = 'list_fs'
    DELETE_FILE = 'delete_f'
    EXPORT_FILE = 'export_f'
    IMPORT_FILE = 'import_f'
    MERGE_FILE  = 'merge_f'
    
class PLBK_CMDS(Enum):
    PLAYBACK_NEW     = 'plbk_new'
    PLAYBACK_START   = 'plbk_start'
    PLAYBACK_STOP    = 'plbk_stop'
    PLAYBACK_PAUSE   = 'plbk_pause'
    PLAYBACK_RESUME  = 'plbk_resume'
    PLAYBACK_ADD     = 'plbk_add'
    PLAYBACK_STATUS  = 'plbk_status'
    PLAYBACK_CONFIG  = 'plbk_config'
    PLAYBACK_SET     = 'plbk_set'
    PLAYBACK_GET     = 'plbk_get'
    PLAYBACK_DELETE  = 'plbk_delete'
    PLAYBACK_EXPORT  = 'plbk_export'
    PLAYBACK_IMPORT  = 'plbk_import'
    PLAYBACK_MERGE   = 'plbk_merge'

class DEV_CMDS(Enum):
    DEVICE_NEW     = 'dev_new'
    DEVICE_LOAD    = 'dev_load'
    DEVICE_SAVE    = 'dev_save'
    DEVICE_CLOSE   = 'dev_close'
    DEVICE_LIST    = 'dev_list'
    DEVICE_DELETE  = 'dev_delete'
    DEVICE_EXPORT  = 'dev_export'
    DEVICE_IMPORT  = 'dev_import'
    DEVICE_MERGE   = 'dev_merge'

class FIXT_CMDS(Enum):
    FIXTURE_NEW     = 'fixt_new'
    FIXTURE_LOAD    = 'fixt_load'
    FIXTURE_SAVE    = 'fixt_save'
    FIXTURE_CLOSE   = 'fixt_close'
    FIXTURE_LIST    = 'fixt_list'
    FIXTURE_DELETE  = 'fixt_delete'
    FIXTURE_EXPORT  = 'fixt_export'
    FIXTURE_IMPORT  = 'fixt_import'
    FIXTURE_GROUP   = 'fixt_group'

class SEL_CMDS(Enum):
    SELECT_ALL      = 'sel_all'
    SELECT_NONE     = 'sel_none'
    SELECT_INVERT   = 'sel_invert'
    SELECT_BY_TYPE  = 'sel_type'
    SELECT_BY_NAME  = 'sel_name'
    SELECT_BY_ID    = 'sel_id'
    SELECT_EVEN     = 'sel_even'
    SELECT_ODD      = 'sel_odd'
    SELECT_OFFSET   = 'sel_offset'
    SELECT_RANGE    = 'sel_range'
    
class ACT_CMDS(Enum):
    ACTION_RUN        = 'act_run'
    ACTION_STOP       = 'act_stop'
    ACTION_PAUSE      = 'act_pause'
    ACTION_RESUME     = 'act_resume'
    ACTION_ADD        = 'act_add'
    ACTION_DELETE     = 'act_delete'
    ACTION_CONFIG     = 'act_config'
    ACTION_SET        = 'act_set'
    ACTION_GET        = 'act_get'
    ACTION_EXPORT     = 'act_export'
    ACTION_IMPORT     = 'act_import'
    ACTION_MERGE      = 'act_merge'
    
class LVL_CMDS(Enum):
    LEVEL_SET         = 'lvl_set'
    LEVEL_GET         = 'lvl_get'
    LEVEL_INCREASE    = 'lvl_increase'
    LEVEL_DECREASE    = 'lvl_decrease'
    LEVEL_MAX         = 'lvl_max'
    LEVEL_MIN         = 'lvl_min'
    LEVEL_FADE        = 'lvl_fade'
    LEVEL_STROBE      = 'lvl_strobe'
    LEVEL_FULL        = 'lvl_full'
    LEVEL_OFF         = 'lvl_off'
    
#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#

class Console:
    def __init__(self):
        
        self.



#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#

    def start(self):
        pass
    
    def stop(self):
        pass
    
    def load_commands(self):
        pass
    
    def list_commands(self):
        pass
    
    def execute_command(self, command):
        pass
    
    def parse_input(self, user_input):
        pass
    
    def live_interpret(self):
        pass
    
    def undo_last(self):
        pass
    
    




#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#






#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#






#! ======================================================== !#
#!                       MAIN BLOCK                         !#
#! ======================================================== !#