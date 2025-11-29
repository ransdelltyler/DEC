
#* ======================================================== *#
'''                    FILE DESCRIPTION                   






'''
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#


#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#

import variables as gvar
from util_classes import ColorLog
log = ColorLog('JOHN_KEYB')

import keyboard
import pystray
from PIL import Image, ImageDraw

DEFAULT_ICON = 'DEEREATCHAIN/assets/icons/icon_tray_raven.png'
DEF_SCRIPT_LIST = {
    'script' : [],  #[lambda functions]
    
}

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
class JohnKeyboard:
    def __init__(self) -> None:
        #? CONSTANT VARIABLES
        self.name = 'DEC-UTILS'
        self.icon_img = Image.open(DEFAULT_ICON).resize((64,64))
        self.scripts = [] #[(delay_time, functions)]
        self.active_scripts = [tuple]
        
        
    #& CONTEXT MANAGER 1/2
    def __enter__(self):
        if gvar.LOG_MSG:
            log.border()
            log.watchdog(' STARTING ')
        return self
    #& CONTEXT MANAGER 2/2
    def __exit__(self, exc_type, exc_val, exc_tb):
        if gvar.LOG_MSG:
            log.watchdog(' SHUTTING DOWN ')
            log.border()
        return False

    
    
#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#

    def activate_script(self, script_name: str, script_list=DEF_SCRIPT_LIST):
        if script_name in script_list:
            func_list = script_list.get(script_name)






#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#


