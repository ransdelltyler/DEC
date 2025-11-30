 #* =============================================================================== *#
 #*                             [CLASS] - HTML RETRIEVER                 
 #* REQUESTS + SELENIUM MINI-MODULE
 #* -       
 #*
 #* =============================================================================== *#

import os
from time import sleep
import urllib.robotparser
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from util_classes import *

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

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
log = ColorLog('HTML_RETR')

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
    
    #* "WWW.HOST-DOMAIN.COM/1/2/3" -> HOST-DOMAIN
    def _get_host(self, url: str) -> str:
        return (urlparse(url).hostname or 'unkown_domain').replace("www.", "") #!EXIT!
    
    #* "WWW.HOST-DOMAIN.COM/1/2/3" -> "HTTP(S)://WWW.HOST-DOMAIN.COM"
    def _get_origin(self, url: str) -> str:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}" #!EXIT!
    
    #* CHECK ROBOTS.TXT FOR SCRAPING PERMISSIONS
    def _check_robots(self, target_url : str) -> bool:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self._get_origin(target_url))
        rp.read()
        
        if rp.can_fetch("*", target_url):
            if LOG_MSG: log.success(f"Allowed to scrape : {target_url} as per robots.txt")
            return True #!EXIT!
        else:
            if LOG_MSG: log.error(f"Target URL: {target_url}, blocked by robots.txt")
            return False #!EXIT!


    #* LOOK FOR EXISTING SAVED HTML FILE:
    #* - IF FOUND, LOAD FROM FILE
    #* - IF NOT FOUND, RETRIEVE FROM WEB AND SAVE TO FILE 
    #*  - SELENIUM FOR DYNAMIC CONTENT
    #*  - REQUESTS FOR CHECKING ROBOTS.TXT
    #* RETURNS: BEAUTIFULSOUP OBJECT FOR PARSING 
    def retrieve_url(self, url:str) -> BeautifulSoup | None:
        if self._check_robots(url):            
            self.driver.get(url)
            
            # GET DOMAIN NAME FOR FOLDER
            full_host = str(urlparse(url).hostname).replace("www.","")
            folder = full_host.replace('.','_')
            # CREATES FOLDER PATH(s)
            os.makedirs(folder, exist_ok=True)
            
            filename = os.path.join(folder, self.driver.title)        
            
            if os.path.exists(filename):
                html = self.load_html(filename)
            else:
                html = self.driver.page_source
                self.save_html(html,filename=filename)

            return BeautifulSoup(html, 'lxml') #!EXIT!
        else:
            if LOG_MSG: log.critical(f'ROBOTS BLOCKED ACCESS') 
            return #!EXIT!

    #* STORE THE RETURNED PAGE IN FILES
    def save_html(self, html, filename: str) -> None:
        with open (filename, 'w', encoding='utf-8') as f:
            f.write(html)
        if LOG_MSG: log.info(f'WRITING FILE {filename}')

    #* LOAD A SAVED HTML FILE
    def load_html(self, filename : str) -> str:
        with open (filename, 'r', encoding='utf-8') as f:
            html = f.read()
            if LOG_MSG: log.info(f'OPENING FILE {filename}')
            return html #!EXIT!

 
    #* SAVE SCREENSHOT OF THE PAGE
    def save_image(self, filename: str) -> None:
        if self.driver is None:
            if LOG_MSG: log.warning('WebDriver not available. Cannot save screenshot.')
            return #!EXIT!
        else:
            try:
                self.driver.save_screenshot(f'{filename}.png')
                if LOG_MSG: log.info(f'Saved screenshot: {filename}.png')
            except Exception as e:
                if LOG_MSG: log.warning(f'Failed to save screenshot for {filename}: {e}')
    
    
    

 