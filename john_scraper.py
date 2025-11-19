'''source /workspaces/DeerEatChain/.venv_dec/bin/activate
URL SCRAPER MODULE
- USES BEAUTIFULSOUP TO SCRAPE WEBPAGES
- USES REQUESTS TO FETCH WEBPAGE CONTENT
- 
'''

 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#
 # TODO: EXCEL URL LIST
 # TODO: CONNECT TO XLSM DATABASE OF EXISTING PRODUCTS:
    #^ - CHECK FOR EXISTING PRODUCTS TO AVOID DUPLICATES BY URL LIST
    #^ -    CHECK TIMESTAMPS AND DECIDE IF UPDATE IS NEEDED
    #^ - IF UPDATE NEEDED, SCRAPE NEW DATA AND OVERWRITE EXISTING ENTRY
    #^ - USE DATABASE OF EXISTING ENTRIES & BASIC_KEYS FOR KEYWORD MATCHING:
    #^ -    START WITH PRODUCTS WITH MATCHING BASE URL / DOMAIN
    #^ -        THEN CHECK FOR SIMILARITY USING RAPIDFUZZ ON PRODUCT NAMES / TITLES
    #^ -    IF DOMAIN IS NEW, USE ALL EXISTING ENTRIES FIRST, THEN BASIC_KEYS
    #^ - POST-RAPIDFUZZ:   
    #^ -    ASK USER FOR ANY MISSING KEYWORD-VALUE PAIRS
    #^ -    PRESENT DATA IN FILLABLE FORM:
    #^ -        ANY MATCHES ABOVE 80% SIMILARITY ARE PREFILLED SUGGESTIONS IN GREEN
    #^ -        MATCHES 50%-80% ARE PREFILLED SUGGESTIONS IN RED (USER MUST CONFIRM)
    #^ -        BELOW 50% ARE LEFT BLANK FOR USER INPUT
    #^ -    ON USER CONFIRMATION, SAVE NEW/UPDATED ENTRY TO XMLX DATABASE

    # TODO: CHECK CERTIFICATION IDS AGAINST DATABASES FOR ACTIVE STATUS
    #^ -    UL
    #^ -    ETL
    #^ -    CETL





import os
import time
import urllib.robotparser
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from util_classes import *

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from util_classes import ColorLog 
from dataclasses import dataclass, field
from typing import Literal

from rapidfuzz import process, fuzz

from keywords import FIXT_FUZZ_KEYS, CTRLR_FUZZ_KEYS, EQUIP_FUZZ_KEYS, GENERIC_KEYWORDS
from data_models import EQCategory

# CUSTOM LOGGING CLASS
# - log.debug(str)
# - log.info(str)
# - log.warning(str)
# - log.critical(str)
# - log.success(str)
# - log.watchdog(str)
# - log.border()
import logging
log = ColorLog('scrape_log', level=1)

#& ======================================================== &#
#&                      HELPER FUNCTIONS                    &#
#& ======================================================== &#
# RETURN TEXT AS LOWERCASE WITH NO SPACES
def norm_text(text : str):
    return ''.join(text.lower().split())

#^ FUZZ KEYWORD CATEGORY MAP
CATEGORY_MAP = {
    EQCategory.CTRLR : CTRLR_FUZZ_KEYS,
    EQCategory.FIXT : FIXT_FUZZ_KEYS,
    EQCategory.EQUIP : EQUIP_FUZZ_KEYS,
}

#* TAKES A LABEL:STR AND USES A DEF OR GIVEN KEYWORD DICT-
#* -TO FIND BEST MATCH 
#* RETURNS:(LABEL/VALUE)
def match_label(label : str, category:EQCategory|dict):
    # CAN BE PASSED AS KEYWORD DICTIONARY: {str,[str]}
    # OR SET BY PASSING EQCategory.<type>
    fuzz_keys = (
        category if isinstance(category,dict)
        else CATEGORY_MAP.get(category, GENERIC_KEYWORDS)
    )
    # NORMALIZE THE TEXT FOR COMPARISSON
    label_norm = norm_text(label)
    
    best_key = None
    best_score = 0
    for key, key_map in fuzz_keys.items():
        result = process.extractOne(
            label_norm,
            [norm_text(p) for p in key_map],
            scorer=fuzz.token_sort_ratio)
        
        if not result:
            continue
        
        match, score, _ = result
        if score > best_score:
            best_key = key
            best_score = score

    return best_key, best_score

#* ======================================================== *#
#*                     SPEC-SCRAPER CLASS                   *#
#* ======================================================== *#
class JohnScraper:
    def __init__(self):
        
        # SET CUSTOM HEADERS FOR REQUESTS
        self.headers = {'User-Agent': 'SimpleSpec1Shot/1.0 (contact: DeerEatChain@gmail.com)'}
        
        # CREATES REQUESTS SESSION FOR CHECKING ROBOTS.TXT
        log.info('Starting requests session for Robots.txt')
        self.robot_session = requests.Session()
        self.robot_session.headers.update(self.headers)
        
        # SELENIUM FOR RETRIEVING FULL HTML W/ HEADLESS CHROME
        log.info('Starting Selenium')
        selenium_user_agent = self.headers['User-Agent']
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument(f'user-agent={selenium_user_agent}')

        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except WebDriverException as e:
            log.debug(f'WebDriverException: {e}') 
            self.driver = None

        self.cur_driver_title = 'INVALID_TITLE'

 #? ======================================================== ?#
 #?               SETUP / PRE-SCRAPE FUNCTIONS.              ?#
 #? ======================================================== ?#
    #* CLOSE SELENIUM DRIVER
    def close_selenium(self):
        if self.driver:
            log.info('Shutting down Selenium WebDriver')
            self.driver.quit()
            self.driver = None


    #* RETURN SCRAPER INSTANCE FOR USE IN WITH STATEMENTS
    def __enter__(self):
        return self    


    #* GUARANTEED SELENIUM CLEANUP @ EXIT 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_selenium()
        return False


    #* EXTRACT BASE URL FOR ROBOTS.TXT CHECK
    def _get_base_url(self, url):
        parsed_url = urlparse(url)
        return urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
    

    #* CHECK ROBOTS.TXT FOR SCRAPING PERMISSIONS
    def _check_robots(self, robots_url : str, target_url : str) -> bool:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        if rp.can_fetch("*", target_url):
            log.success(f"Allowed to scrape : {target_url} as per robots.txt")
            return True
        else:
            log.error(f"Target URL: {target_url}, blocked by robots.txt")
            return False


    #* SIMPLE FETCH URL
    def _fetch_url(self, url, wait_for: tuple | None, wait_time: int=10) -> str | None:
        if not self.driver:
            log.critical('Webdriver not available. Cannot fetch URL')
            return None

        try:
            self.driver.get(url)
            
            if wait_for:
                log.debug(f'Waiting for element: {wait_for}...')
                
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located(wait_for)
                )
            else:
                wait_time = 2
                time.sleep(2)
                log.warning(f'No wait time provided. Using default: {wait_time}sec')

            self.cur_driver_title = self.driver.title.replace(' ', '_').replace('/', '_')
            log.info(f'Fetched URL: {url} | Page Title: {self.cur_driver_title}')
            return self.driver.page_source

        except WebDriverException as e:
            log.warning(f'WebDriver error during _fetch_url({url})')
            return None


    #* RETRIEVE URL CONTENT SAFELY AND CHECK ROBOTS.TXT 
    #* CALLS: self._check_robots(), self._fetch_url() | RETURNS: HTML TEXT STRING
    def _safe_retrieve(self, url : str, wait_for : tuple | None, ignore_robots=False, **kwargs) -> str | None:
        
        # EXTRACT BASE URL FOR ROBOTS.TXT CHECK
        base_url = self._get_base_url(url)
        robots_url = base_url + '/robots.txt'
        

        # IF ALLOWED BY ROBOTS.TXT OR IGNORE_ROBOTS = TRUE, PROCEED TO FETCH
        if not ignore_robots and not self._check_robots(robots_url, url):
            log.error(f"Scraping blocked by robots.txt for URL: {url}")
            log.debug(f"TRY TO FETCH ANYWAY BY ADDING ignore_robots=True to retrieve_url()")
            log.border('')
            return None
        
        log.debug(f'Wait for element parameter: {wait_for}')
        
        try:
            if wait_for is None:
                log.debug('No wait_for_element provided, using default sleep.')
                return self._fetch_url(url, wait_for=None, **kwargs)
            if isinstance(wait_for, tuple):
                log.debug(f'Using wait_for_element: {wait_for}')
                return self._fetch_url(url, wait_for=wait_for, **kwargs)
        except Exception as e:
            log.warning(f"Failed to retrieve URL: {url} | {e}")
            return None   




    #* LOOK FOR EXISTING SAVED HTML FILE:
    #* - IF FOUND, LOAD FROM FILE
    #* - IF NOT FOUND, RETRIEVE FROM WEB AND SAVE TO FILE 
    #*  - SELENIUM FOR DYNAMIC CONTENT
    #*  - REQUESTS FOR CHECKING ROBOTS.TXT
    #* RETURNS: BEAUTIFULSOUP OBJECT FOR PARSING 
    def retrieve_url(self, url:str , wait_for: tuple) -> BeautifulSoup | None:

        folder_name = self._get_base_url(url).split('.')[1] # GET DOMAIN NAME FOR FOLDER
        
        self.create_db_folder(folder_name) # CREATES FOLDER IF NOT EXISTS
        
        # RETRIEVE HTML CONTENT SO TITLE IS UPDATED
        html = self._safe_retrieve(url, wait_for=wait_for, ignore_robots=False)

        if html is None:
            log.warning(f'Initial HTML retrieval failed for URL: {url}')
            log.border('')
            return None


        filename = os.path.join(folder_name, self.cur_driver_title)
        
        if not os.path.exists(filename):
            log.info(f'Saving HTML to file : {filename}')
            self.save_html(html=html, filename=filename)
        else:
            log.info(f'Found saved HTML file: {filename}, loading from file')
            html = self.load_html(filename=filename)
                        
        if html is not None:
            return BeautifulSoup(html, 'lxml')
        else:
            log.error(f'Failed to load HTML content for URL: {url}')
            return None



    #* STORE THE RETURNED PAGE IN FILES
    def save_html(self, html, filename: str) -> None:
        try:
            with open (filename, 'x', encoding='utf-8') as f:
                f.write(html)
                f.close()
        except FileExistsError:
            # TODO: ADD OVERWRITE OPTION
            # TODO: ADD TIMESTAMP * VERSIONING
            # TODO: ADD CHECK FOR UPDATES
            # TODO: ADD TIMED UPDATE
            log.warning(f'File already exists: {filename}, not overwriting')


    #* LOAD A SAVED HTML FILE
    def load_html(self, filename : str) -> str | None:
        try:
            with open (filename, 'r', encoding='utf-8') as f:
                html = f.read()
                f.close()
                return html
        except FileNotFoundError:
            log.warning(f'File not found: {filename}')
            return None


    #* CREATE FOLDER FOR SAVED HTML FILES
    def create_db_folder(self, folder_name: str = 'html_db') -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            log.info(f'Created folder: {folder_name}')
        return folder_name


 
    #* SAVE SCREENSHOT OF THE PAGE
    def save_image(self, filename: str) -> None:
        if self.driver is None:
            log.warning('WebDriver not available. Cannot save screenshot.')
            return
        else:
            try:
                self.driver.save_screenshot(f'{filename}.png')
                log.info(f'Saved screenshot: {filename}.png')
            except Exception as e:
                log.warning(f'Failed to save screenshot for {filename}: {e}')
    

 #? ======================================================== ?#
 #?                   SCRAPING FUNCTIONS                     ?#
 #? ======================================================== ?#
    #* SCRAPE HTML FOR KEYWORD VALUE PAIRS
    def scrape_html(self, html):
        pass
    
    
    

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#

# URL TO SCRAPE
url = 'https://www.environmentallights.com/19072-px-spi-v2.html'

WAIT_FOR_ELEMENT = (By.CLASS_NAME, 'product-detail-content')

#* INIT URL SCRAPER + DESTROY WHEN FINISHED
with JohnScraper() as scraper:
    soup = scraper.retrieve_url(url, wait_for=WAIT_FOR_ELEMENT)
    if soup:
        text = soup.get_text(separator='/n', strip=True)
        log.success(f'Scraping succeeded on : {soup.title}')



    else:  
        log.error(f'Scraping failed on : {soup}')


log.success('Shutdown Success - Exiting Script')

 