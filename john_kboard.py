
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




#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
class JohnKeyboard:
    def __init__(self) -> None:
        pass
    
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







#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#


