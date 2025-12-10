
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
from pprint import pprint
import os, sys, importlib.util
# ^ END STANDARD MODULES ^ #

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

'''- CUSTOM MODULE IMPORTS -'''
from system.utils.design_models import Controller, PowerSupply
from system.gen.settings import LOG_MSG
from john_scraper import JohnScraper
from system.utils.util_classes import *
from system.utils.data_models import Equipment, LEDProd

'''- 3RD PARTY MODULE IMPORTS -'''
#* IMPORT BEAUTIFULSOUP FOR HTML PARSING
from bs4 import BeautifulSoup 
#* IMPORT OPENPYXL FOR EXCEL XLSX/XLSM HANDLING
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
#* EQUIPMENT DATABASE MANAGER CLASS
class EquipDB:
    def __init__(self, wb_path:str):
        # TODO: ADD DYNAMICALLY CREATED DICTIONARY OF:
        # TODO:  - WORKBOOKS
        # TODO:  - WORKSHEETS
        # TODO:  - (COLUMN , INDEX MAP)
        # TODO:  - 
        self.wb = load_workbook(wb_path, keep_vba=True)
        if LOG_MSG and self.wb:
            log.success(f" Workbook '{wb_path}' loaded successfully.")
            log.info(f'Workbook Sheets: {self.wb.sheetnames}')
        else:
            log.error(f" Failed to load Workbook '{wb_path}'.")
        
        #* CHECK FOR REQUIRED SHEETS AND STORE REFERENCES
        self.db_led_ws, self.db_psu_ws, self.db_ctrlr_ws = self._sheet_setup()



#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#
    #* SETUP AND RETURN REQUIRED SHEETS FOR DATABASE OPERATIONS
    def _sheet_setup(self) -> list[Worksheet]:
        if LOG_MSG: log.info('CHECKING FOR REQUIRED PY_DB SHEETS...')
        
        led_db_ws = self.find_sheet(self.wb, 'led_py_db')
        psu_db_ws = self.find_sheet(self.wb, 'psu_py_db')
        ctrlr_db_ws = self.find_sheet(self.wb, 'ctrlr_py_db')
        
        if not led_db_ws or not psu_db_ws or not ctrlr_db_ws:
            log.error(' ONE OR MORE REQUIRED SHEETS MISSING FROM WORKBOOK!')
            return [] #!EXIT!#
        else:
            if LOG_MSG: log.success(' ALL REQUIRED SHEETS FOUND IN WORKBOOK!')
            return [led_db_ws, psu_db_ws, ctrlr_db_ws] #!EXIT!#
        

    #* SAFELY GET SHEETS
    def find_sheet(self, wb : Workbook, sheet_name : str):
        if sheet_name not in wb.sheetnames:
            log.error(f" Sheet '{sheet_name}' not found in workbook.")
            return None #!EXIT!#
        return wb[sheet_name] #!EXIT!#

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
                if LOG_MSG: log.warning(f" Header '{header_name}' not found in sheet '{ws.title}'")
        if LOG_MSG: log.success(f" All Headers in Sheet: '{ws.title}' were found!")
        return keyvar_map #!EXIT!#


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


    #* CHECKS FOR EXISTING URL IN DB
    def url_check(self, url: str):
        pass
    

    #* CHECKS FOR EXISTING NAME IN DB
    def name_check(self, name: str):
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
            return False #!EXIT!#
        
        # GET INDEXES OF COL NAMES
        match_col = key_map[match_col_name]
        update_col = key_map[update_col_name]
        
        # UPDATE FIRST ROW FOUND w/ MATCH_VALUE IN MATCH_COL_NAME | NEW_VALUE 
        for row in ws.iter_rows(min_row=2, values_only=False):
            cell = row[match_col-1]
            if str(cell.value).strip().lower() == str(match_value).strip().lower():
                ws.cell(row=cell.row, column=update_col, value=new_value)
                log.info(f" Updated Row {cell.row} : '{update_col_name}' to '{new_value}'")
                return True #!EXIT!#
        
        log.warning(f" Value '{match_value}' not found in column '{match_col_name}'")



    
    #* CHECK IF URL EXISTS IN DATABASE
    #* YES: SCRAPE AGAIN, CHECK FOR UPDATES
    #* NO: SCRAPE AND ADD NEW ENTRY
    def scrape_new_url(self, url:str):
        #url = 'https://www.environmentallights.com/19072-px-spi-v2.html'    # LED TAPE
        #url = 'https://www.environmentallights.com/17125-dmx-4-8a.html'     # CONTROLLER
        #url = 'https://www.environmentallights.com/17152-hlg-600h-24a.html' # POWER SUPPLY
        if True: #self.url_check(url):
            if LOG_MSG:
                log.warning(f'URL ALREADY EXISTS IN DATABASE: {url}')
                log.info(f'SCRAPING FOR UPDATES: {url}')
            with JohnScraper(url) as scraper:
                if scraper.data is not None: 
                    if LOG_MSG:
                        #log.success(f'SCRAPED DATA: {scraper.data}')
                        log.info(f'ADDING NEW EQUIPMENT TO DATABASE...')
                    self.add_equipm(scraper.new_equipment) #!ADD TO DB
                    self.wb.save('DEEREATCHAIN/assets/PYDB.xlsm')
                else:
                    if LOG_MSG: log.error(f'FAILED TO SCRAPE URL: {url}')
                    return None #!EXIT!#


    #* ADD NEW EQUIPMENT OBJECT TO RESPECTIVE DATABASE (AUTO@POST-SCRAPE)
    def add_equipm(self, equipm) -> bool:
        if equipm is None:
            if LOG_MSG: log.error('ADD_EQUIPM() WAS GIVEN NONE!')
            return False #!EXIT!#
        if isinstance(equipm, LEDProd):
            if LOG_MSG: log.info('ADDING NEW LED EQUIPMENT TO DATABASE...')
            self.db_led_ws.append([getattr(equipm, attr) for attr in equipm.__slots__])
        elif isinstance(equipm, PowerSupply):
            if LOG_MSG: log.info('ADDING NEW POWER SUPPLY TO DATABASE...')
            self.db_psu_ws.append([getattr(equipm, attr) for attr in equipm.__slots__])
        elif isinstance(equipm, Controller):
            if LOG_MSG: log.info('ADDING NEW CONTROLLER TO DATABASE...')
            self.db_ctrlr_ws.append([getattr(equipm, attr) for attr in equipm.__slots__])
        return True #!EXIT!#


    #* REMOVE EQUIPMENT ENTRY FROM DATABASE
    def remove_equipm(self):
        pass
    
    
    #* SELECT EQUIPMENT ENTRY AND RETURNS EQUIPMENT OBJ.
    def pull_equipm(self):
        pass
    

    #* LOAD AND EDIT EQUIPMENT ENTRY
    def edit_equipm(self, equipm: Equipment):
        pass 
    


 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#
 
def test():
    db_path = 'DEEREATCHAIN/assets/ENCL.xlsm'
    equip_db = EquipDB(db_path)
     
    # TEST SCRAPING AND ADDING NEW EQUIPMENT
    test_url = 'https://www.environmentallights.com/20914-plnw-pf-rgb30k-10m.html'
    equip_db.scrape_new_url(test_url)
    log.info('TEST COMPLETE.')
    
test()