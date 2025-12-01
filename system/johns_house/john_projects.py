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

# GLOBAL VARIABLES IMPORT
from system.gen import gvars
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

log = ColorLog('JOHN_PROJ')

 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

class JohnProjects:
    def __init__(self):
        pass


 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#
    def _save(self):
        pass
    def _load(self):
        pass
    def _restore(self):
        pass
    def _new(self):
        pass
    def _set(self):
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