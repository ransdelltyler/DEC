# IF VENV DIDN'T START, ACTIVATE IT WITH:
# source /workspaces/DeerEatChain/.venv/bin/activate

#? KEYWORDS USED TO FIND COLUMN INDEXES | VAR : COLUMN_NAME
#* LED EQUIPMENT        | ENVI_ELUXTRA_NEON_WTP_RGB30K {...}
#*  PATTERN             | MANUFACTURER_MODEL_TYPE_SUBTYPE_COLORS

#* PSU EQUIPMENT        | MEANWELL_HLG240 {...}
#*  PATTERN             | MANUFACTURER_MODEL

#* CONTROLLER EQUIPMENT | ADVATEK_R1FS {...}
#*  PATTERN             | MANUFACTURER_MODEL

#* GENERIC EQUIPMENT    | GEN_RECEPTACLE {...}, GEN_WIRE {...}, GEN_BUTTON {...}
#*  PATTERN             | MANUFACTURER_MODEL

'''
# =======FILE-README=======

FILE TITLE:
 - MAIN DESCRIPTION
 - BASIC FUNCTIONALITY
 - DEPENDENCIES:
    - utilclasses.py
    - requests

FUNCTIONS:
#^  function_1(var=str)                          - FUNCTION DESCRIPTION
#^  function_2(var=str,[objects])                - FUNCTION DESCRIPTION
#^  function_2(var=str,[objects],*args,**kwargs) - FUNCTION DESCRIPTION

'''


#* ======================================================== *#
'''                    FILE DESCRIPTION                   






'''
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#
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

#* CLASS / FUNCTION TITLE 

#^ DEBUG TESTS / EXAMPLES

#! ===[START MAIN BLOCK]=== !#
from util_classes import *
log = ColorLog('scrape_log', level=logging.DEBUG)
log.info('STAGE NAME / EVENT DESCRIPTION')
log.warning('NON CRITICAL ISSUE')
log.error('MAJOR ISSUE')
log.critical('CRITICAL ISSUE')
log.debug('POSSIBLE SOLUTION TO ERROR')
log.success('STAGE COMPLETE / OPERATION SUCCESSFUL')
log.watchdog('MONITORING ALERT / WATCHDOG EVENT')
#! ________________________ !#

#* [START FUNCTION BLOCK] *#
#& FUNCTION X DESCRIPTION 
#~ ________________________
#& FUNCTION Y DESCRIPTION
#~ ________________________
#& FUNCTION Z DESCRIPTION
#~ ________________________
#* ________________________ *#

