
#* ======================================================== *#
 #*                    FILE DESCRIPTION                   
 #* EXCEL DATABASE MANIPULATION SCRIPT
 #*  - USES OPENPYXL TO READ/WRITE XLSM EXCEL FILES
 #*  - USES KEYWORDS.PY TO MAP VARIABLE NAMES TO EXCEL COLUMN NAMES
 #*  - FUNCTIONS:
 #*      - ensure_keywords_module() : Ensures keywords.py is loaded
 #*      - safe_get_sheet() : Safely get a worksheet by name
 #*      - build_column_map() : Build a map of column names to indexes
 #*      - build_keyvar_map() : Build a map of keyword variable names to column indexes
 #*      - update_first_match() : Update first row matching a value in a column
 #*      - update_all_match() : Update all rows matching a value in a column
 #*      - update_first_by_name() : Update first row matching a value in a named column
 #*  - DEPENDENCIES:
 #*      - openpyxl
 #*      - keywords.py
 #*
 #*
 #*
 #* ======================================================== *#


'''- STANDARD MODULE IMPORTS -'''
import os, sys, importlib.util
# ^ END STANDARD MODULES ^ #

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

'''- CUSTOM MODULE IMPORTS -'''
from system.utils.util_classes import *
from system.utils.data_models import Equipment

'''- 3RD PARTY MODULE IMPORTS -'''
#* IMPORT BEAUTIFULSOUP FOR HTML PARSING
from bs4 import BeautifulSoup 
#* IMPORT REQUESTS FOR HTTP REQUESTS
import requests
#* IMPORT RESPONSES FOR MOCKING REQUESTS IN TESTS
import responses
#* IMPORT PYPERCLIP FOR CLIPBOARD HANDLING
import pyperclip
#* IMPORT OPENPYXL FOR EXCEL XLSX/XLSM HANDLING
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
# ^^^ 3RD PARTY MODULE IMPORTS ^^^ #

#* - PRINT CURRENT WORKING DIR + SYS.PATH - #
import sys, os
print("Current Working Dir:", os.getcwd())
print("Sys Path:", sys.path)



 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#
log = ColorLog('JOHN_EQUI', level=1)

class JohnEquipDB:
    def __init(self):
        # TODO: ADD DYNAMICALLY CREATED DICTIONARY OF:
        # TODO:  - WORKBOOKS
        # TODO:  - WORKSHEETS
        # TODO:  - (COLUMN , INDEX MAP)
        # TODO:  - 
        pass


 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#
 
 #* SAFELY LOAD WORKBOOK
    def _load_workbook_safe(self, path : str) -> Workbook | None:
        try:
            wb = load_workbook(path, keep_vba=True)
            log.success(f" Workbook '{path}' loaded successfully.")
            
            # PRINT CHECK - WORKBOOK SHEET NAMES | [NAME]
            log.info(f" Workbook Sheet Names : {wb.sheetnames}")

            return wb
        
        except Exception as e:
            log.critical(f" ERROR loading workbook '{path}': {e}")
            return None

 #* SAFELY GET SHEETS
    def _safe_get_sheet(self, wb : Workbook, sheet_name : str):
        all_found = True
        if sheet_name not in wb.sheetnames:
            all_found = False
            log.error(f" Sheet '{sheet_name}' not found in workbook.")
            return None
        if all_found : log.success(f" Found All Sheets")
        return wb[sheet_name]

 #* FINDS AND RETURNS A MAP OF LOWER CASE COLUMN {NAME : INDEX}
    def _build_column_map(self, ws : Worksheet):
        return {
            str(cell.value).strip().lower():cell.column
            for cell in ws[1]
            # IGNORE BLANKS
            if cell.value
        }

 #* BUILD AND RETURN A MAP OF MATCHED {KEYWORD VARIABLE : COLUMN INDEX}
    def _build_keyvar_map(self, ws : Worksheet, keyword_dict : dict):
        col_map = self._build_column_map(ws)
        keyvar_map = {}
        for key, header_name in keyword_dict.items():
            header_name_lc = header_name.lower()
            if header_name_lc in col_map:
                keyvar_map[key.lower()] = col_map[header_name_lc]
            else:
                log.warning(f" Header '{header_name}' not found in sheet '{ws.title}'")
        log.success(f" All Headers in Sheet: '{ws.title}' were found!")
        return keyvar_map

 #* QUERY THE DATABASE FOR _____ | SET FUZZY TO FALSE FOR EXACT MATCHES ONLY
    def _query_database(self, target, fuzzy = True):
        pass

 #* ADD / UPDATE TIMESTAMP FOR LATEST UPDATE
    def _timestamp_row(self):
        pass

 #* LOOK AT TIMESTAMPS AND RECCOMMEND UPDATES
    def _suggest_updates(self):
        pass

 #* CHECK CERTIFICATION STATUSES
    def _run_cert_checks(self):
        pass

 #* QUICKLY CHECKS FOR EXISTING URL IN DB
    def _quickcheck(self):
        pass

 #* CREATES AN EQUIPMENT OBJECT WHEN DB SELECTION MADE
    def _build_equip(self):
        pass

 
 #? ======================================================== ?#
 #?                   EXTERNAL FUNCTIONS                     ?#
 #? ======================================================== ?#
 #* LOADS A NEW DATABASE FILE FROM GIVEN PATH
    def load_new_xlsm(self, path):
        # TODO: ADD LAST KNOWN PATH VARIABLE
        pass



 #* UPDATE 1 CELL IN ALL ROWS THAT MATCH_COL VALUE = MATCH_VAL
    def update_all_match(self, ws : Worksheet, match_col, match_val, update_col, new_val):
        # HOLD COUNT OF ROWS CHANGED
        count = 0
        for row in ws.iter_rows(min_row=2, values_only=False):
            if row[match_col-1].value == match_val:
                ws.cell(row=row[match_col-1].row, column=update_col, value=new_val)
                count += 1

        log.info(f" Updated {count} rows; Where {match_col} = {match_val}")


 #* UPDATES ALL ROWS BY: UPDATE_COL_NAME WITH NEW_VALUE IF MATCH_VALUE IN MATCH_COL_NAME 
    def update_first_by_name(self, ws, key_map, match_col_name, match_value, update_col_name, new_value):
        # NORMALIZE CASE FOR INPUT COL NAMES
        match_col_name = match_col_name.lower()
        update_col_name = update_col_name.lower()

        # CATCH NO MATCHING COLUMN NAMES FOUND
        if match_col_name not in key_map or update_col_name not in key_map:
            log.warning(f" Column not found in key_map: '{match_col_name}' or '{update_col_name}'")
            return False
        
        # GET INDEXES OF COL NAMES
        match_col = key_map[match_col_name]
        update_col = key_map[update_col_name]
        
        # UPDATE FIRST ROW FOUND w/ MATCH_VALUE IN MATCH_COL_NAME | NEW_VALUE 
        for row in ws.iter_rows(min_row=2, values_only=False):
            cell = row[match_col-1]
            if str(cell.value).strip().lower() == str(match_value).strip().lower():
                ws.cell(row=cell.row, column=update_col, value=new_value)
                log.info(f" Updated Row {cell.row} : '{update_col_name}' to '{new_value}'")
                return True
        
        log.warning(f" Value '{match_value}' not found in column '{match_col_name}'")



 #* BASIC EQUIPMENT DATABASE FUNCTIONS
    def add_equipm(self):
        pass
    
    def remove_equipm(self):
        pass
 #* SELECT EQUIPMENT ENTRY AND RETURNS EQUIPMENT OBJ.
    def use_equipm(self):
        pass

    def edit_equipm(self):
        pass

    def get_url_matches(self):
        pass
    
    def get_name_matches(self):
        pass

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#


 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#