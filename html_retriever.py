 #* =============================================================================== *#
 #*                             [CLASS] - HTML RETRIEVER                 
 #* REQUESTS + SELENIUM MINI-MODULE
 #* - retrieve_url( url:str , wait_for_element:tuple) -> BeautifulSoup 
 #* -   [JOHN FILES] QUERY AND RETRIEVE EXISTING SAVED HTML
 #* -   IF NEW, CHECK ROBOTS.TXT, AND IF ALLOWED, RETRIEVE HTML
 #* -       [JOHN_FILES] SAVE NEW HTML, IMAGES, AND FILES TO ARCHIVE
 #* -       
 #*
 #* =============================================================================== *#

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
from variables import LOG_MSG
from util_classes import ColorLog 
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
#*                    HTMLRETRIEVER CLASS                   *#
#* ======================================================== *#
class HTMLRetriever:
    def __init__(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # SET CUSTOM HEADERS FOR REQUESTS
        self.headers = {'User-Agent': 'SimpleSpec1Shot/1.0 (contact: DeerEatChain@gmail.com)'}
        
        # CREATES REQUESTS SESSION FOR CHECKING ROBOTS.TXT
        if LOG_MSG: log.info('Starting requests session for Robots.txt')
        self.robot_session = requests.Session()
        self.robot_session.headers.update(self.headers)
        
        # SELENIUM FOR RETRIEVING FULL HTML W/ HEADLESS CHROME
        if LOG_MSG: log.info('Starting Selenium')
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f"user-agent={self.headers['User-Agent']}")
        # Anti-detection
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        self.driver = webdriver.Chrome(options=options)

    #^ CONTEXT MANAGER FUNCTIONS
    #? RETURN SCRAPER INSTANCE FOR USE IN WITH STATEMENTS
    def __enter__(self):
        return self    

    #? GUARANTEED SELENIUM CLEANUP @ EXIT 
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.driver.quit()
        except:
            pass
    
 #? ======================================================== ?#
 #?               SETUP / PRE-SCRAPE FUNCTIONS.              ?#
 #? ======================================================== ?#
    
    def _get_host(self, url: str) -> str:
        return (urlparse(url).hostname or 'unkown_domain').replace("www.", "")
    
    def _get_origin(self, url: str) -> str:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}"
    
    #* CHECK ROBOTS.TXT FOR SCRAPING PERMISSIONS
    def _check_robots(self, robots_url : str, target_url : str) -> bool:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        if rp.can_fetch("*", target_url):
            if LOG_MSG: log.success(f"Allowed to scrape : {target_url} as per robots.txt")
            return True
        else:
            if LOG_MSG: log.error(f"Target URL: {target_url}, blocked by robots.txt")
            return False


    #* SIMPLE FETCH URL
    def _fetch_url(self, url, wait_for: tuple | None, wait_time: int=10) -> str | None:
        if not self.driver:
            if LOG_MSG: log.critical('Webdriver not available. Cannot fetch URL')
            return None

        try:
            self.driver.get(url)
            
            if wait_for:
                if LOG_MSG: log.debug(f'Waiting for element: {wait_for}...')
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located(wait_for)
                )
            else:
                if LOG_MSG: log.warning(f'No wait time provided. Using default: {wait_time}sec')
                wait_time = 2
                time.sleep(2)

            self.cur_driver_title = self.driver.title.replace(' ', '_').replace('/', '_')
            if LOG_MSG: log.info(f'Fetched URL: {url} | Page Title: {self.cur_driver_title}')
            return self.driver.page_source

        except WebDriverException as e:
            if LOG_MSG: log.warning(f'WebDriver error during _fetch_url({url})')
            return None


    #* RETRIEVE URL CONTENT SAFELY AND CHECK ROBOTS.TXT 
    #* CALLS: self._check_robots(), self._fetch_url() | RETURNS: HTML TEXT STRING
    def _safe_retrieve(self, url : str, wait_for : tuple) -> str | None:
        try:
            self.driver.get(url)
            by, selector = wait_for
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((by,selector))
                )

            self.cur_driver_title = self.driver.title.replace(" ", "_")
            return self.driver.page_source
        except Exception as e:
            if LOG_MSG: log.warning(f'WEBDRIVER ERROR DURING FETCH: {e}')
            return None


    #* LOOK FOR EXISTING SAVED HTML FILE:
    #* - IF FOUND, LOAD FROM FILE
    #* - IF NOT FOUND, RETRIEVE FROM WEB AND SAVE TO FILE 
    #*  - SELENIUM FOR DYNAMIC CONTENT
    #*  - REQUESTS FOR CHECKING ROBOTS.TXT
    #* RETURNS: BEAUTIFULSOUP OBJECT FOR PARSING 
    def retrieve_url(self, url:str , wait_for: tuple) -> BeautifulSoup | None:
        
        self.driver.get(url)
        # GET DOMAIN NAME FOR FOLDER
        full_host = str(urlparse(url).hostname).replace("www.","")
        folder = full_host.replace('.','_')
        # CREATES FOLDER PATH(s)
        os.makedirs(folder, exist_ok=True)
        
        import envir_bs4 
        # LOAD DOMAIN RULESET
        domain_rules = envir_bs4.DOMAIN_RULES.get(full_host,{})
        # RUN PREPROCESSING FUNCTION FOR JS CONTENT
        pre_fn = domain_rules.get('preprocess')
        if callable(pre_fn):
            
            time.sleep(1.5)
            if LOG_MSG: log.watchdog('PREFUNCTION RAN')
        html = self.driver.page_source
        
        filename = os.path.join(folder, self.driver.title)        
        self.save_html(html,filename=filename)

        return BeautifulSoup(html, 'lxml')
        #return None

    #* STORE THE RETURNED PAGE IN FILES
    def save_html(self, html, filename: str) -> None:
        with open (filename, 'w', encoding='utf-8') as f:
            f.write(html)
        if LOG_MSG: log.info(f'WRITING FILE {filename}')

    #* LOAD A SAVED HTML FILE
    def load_html(self, filename : str) -> str | None:
        try:
            with open (filename, 'r', encoding='utf-8') as f:
                html = f.read()
                if LOG_MSG: log.info(f'OPENING FILE {filename}')
                return html
        except FileNotFoundError:
            if LOG_MSG: log.warning(f'FILE NOT FOUND: {filename}')
            return None

    # TODO: INTEGRATE WITH FILE MANAGER
    #* CREATE FOLDER FOR SAVED HTML FILES
    def create_db_folder(self, folder_name: str = 'html_db') -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            if LOG_MSG: log.info(f'CREATED FOLDER: {folder_name}')
        return folder_name


 
    #* SAVE SCREENSHOT OF THE PAGE
    def save_image(self, filename: str) -> None:
        if self.driver is None:
            if LOG_MSG: log.warning('WebDriver not available. Cannot save screenshot.')
            return
        else:
            try:
                self.driver.save_screenshot(f'{filename}.png')
                if LOG_MSG: log.info(f'Saved screenshot: {filename}.png')
            except Exception as e:
                if LOG_MSG: log.warning(f'Failed to save screenshot for {filename}: {e}')
    
    
    

 