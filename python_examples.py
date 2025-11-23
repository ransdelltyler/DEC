

#* ======================================================== *#
#*                     USEFUL SNIP-ITS                      *#
#* ======================================================== *#

#* GET CURRENT TIME
import time
time.time()

#* LAMBDA FUNCTIONS

#* DATACLASSES
from dataclasses import dataclass, field
#? SLOTS = MEMORY ENHANCEMENT / NO NEW ATTRIBUTES
#? KW_ONLY = FIELDS MUST BE ASSIGNED BY KEYWORD !LOCATION
@dataclass(slots=True, kw_only=True)
class Deer():
    deer: str
    eat: int
    chain: int
    
#* *ARGS, **KWARGS, AND * ---------------------------------  #
#? CAN BE PASSED KEYWORD ARGUMENTS THROUGH NESTED FUNCTION CALLS
def func1(d, e, c): pass
def func2(*, deer, eat, chain):
    return 
#TODO: ^^^^^^

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
#* RETURN CLASS INSTANCE FOR WITH STATEMENTS (REQUIRES __exit__)
def __enter__(self):
    return self
#* EXIT DUNDER
def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_selenium()
        return False

#? ======================================================== ?#
#?                     UTIL FUNCTIONS                       ?#
#? ======================================================== ?#

#* EXTRACT BASE URL FOR ROBOTS.TXT CHECK ------------------  #
from urllib.parse import urlparse, urlunparse
def base_url(url):
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))

from util_classes import ColorLog
log = ColorLog('PYTHON EXAMPLES')




#? ======================================================== ?#
#?                      FILE OPERATIONS                     ?#
#? ======================================================== ?#

#* WRITE/OVERWRITE/READ FILE ------------------------------  #
file_data = 'NEW FILE CREATED'
file_path = 'DEEREATCHAIN/test.py'
# 'X'= ENFORCE NO OVERWRITE, 'W'= WRITE, 'R'= READ
with open(file_path, 'x', encoding='utf-8') as f:
                f.write(file_data)
                f.close()

#* CREATE FOLDER / TREE -----------------------------------  #
import os
folder_name = '/workspaces/DEC/DEEREATCHAIN'
if not os.path.exists(folder_name):
            os.makedirs(folder_name)

#* SEARCH FOR <FILE-NAME> STARTING IN ROOT FOLDER ---------  #
def cur_find_file(self, filename:str) -> str | None:
    root = self.root_path
    # RETURN ALL ITEMS LOWER THAN <ROOT> THAT MATCH <FILENAME>
    for file in root.rglob(filename):
        if file.is_file():
            return str(file) #!EXIT!
    return None  #!EXIT! FAILED TO FIND


#* [OPENPYXEL] - EXCEL FILE EDITING -----------------------  #
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
#? LOAD WORKBOOK / XLSM FILE
wb = load_workbook(file_path, keep_vba=True)
worksheets = wb.sheetnames
#? GET WORKSHEET    
ws = wb['worksheet']
#? UPDATE CELL IN WORKSHEET
ws.cell(row=1,column=1, value=0)
#? CREATE HEADER {COLUMN : INDEX} MAP 
def build_column_map(ws : Worksheet) -> dict:
        return {
            str(cell.value).strip().lower():cell.column
            for cell in ws[1]
            # IGNORE BLANKS
            if cell.value
        }


#^ ======================================================== ^#
#^                    SIMPLE MINI-MODULES                   ^#
#^ ======================================================== ^#

#* RETURN TEXT AS LOWERCASE WITH NO SPACES
def normalize_text(text : str):
    return ''.join(text.lower().split())


