 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
 #* PDF SCRAPING MODULE
 #*
 #*
 #*
 #* ======================================================== *#

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
from DEEREATCHAIN.system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

log = ColorLog('JOHN_PDFS')

 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#

 #? ======================================================== ?#
 #?                   EXTERNAL FUNCTIONS                     ?#
 #? ======================================================== ?#

 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#
