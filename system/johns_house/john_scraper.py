

 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
'''
Docstring for DEEREATCHAIN.system.johns_house.john_scraper



'''
 #* ======================================================== *#

 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#
from pprint import pprint
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
    
from urllib.parse import urlparse

from system.modules.bs4_files.envir_bs4 import DOMAIN_RULES
from system.modules.html_retriever import HTMLRetriever
from system.gen.settings import LOG_MSG





# GLOBAL VARIABLES IMPORT
from DEEREATCHAIN.system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

log = ColorLog('JOHN_SCRAPER')

 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

class JohnScraper:
    def __init__(self, url: str):
        self.data = self.scrape_url(url)
        
        if not self.data:
            if LOG_MSG: log.debug(f'NO DATA SCRAPED FROM URL: {url}')
        else:
            if LOG_MSG:
                log.success(f'SUCCESSFULLY SCRAPED DATA FROM URL: {url}')
                log.info(f'ATTEMPTING FUZZ MATCHING')
            self.fuzz_match_fields()
        pass

     #^ CONTEXT MANAGER FUNCTIONS
    #? RETURN SCRAPER INSTANCE FOR USE IN WITH STATEMENTS
    def __enter__(self):
        return self

    #? GUARANTEED SELENIUM CLEANUP @ EXIT 
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#

    #* "WWW.HOST-DOMAIN.COM/1/2/3" -> HOST-DOMAIN.COM
    def get_host(self, url: str) -> str:
        return (urlparse(url).hostname or 'unkown_domain').replace("www.", "") #!EXIT!
    
    
    
    #* SCRAPE URL USING DOMAIN RULES
    def scrape_url(self, url: str) -> dict | None:
        with HTMLRetriever() as retriever:
            soup = retriever.retrieve_url(url)
            
        if not soup: 
            log.debug(f'FAILED TO LOAD PAGE: {url}')
            return None #!EXIT!
        
        url_host = self.get_host(url)
        domain = url_host.lower()
        if domain not in DOMAIN_RULES:
            if LOG_MSG : log.debug(f'NO SCRAPING RULES FOR DOMAIN: {domain}')
            return None #!EXIT!
        rules = DOMAIN_RULES[domain]
        
        result = {}
        for field_name, extractor_list in rules.items():
            if field_name == 'preprocess':
                continue
            
            result[field_name] = []
            for extractor in extractor_list:
                #if LOG_MSG: log.watchdog(f'ATTEMPTING TO EXTRACT: {field_name}')
                try:
                    result[field_name].append(extractor(soup))
                    #if LOG_MSG: log.debug(f'RESULT: {result[field_name]}')
                except Exception as e:
                    if LOG_MSG: log.warning(f'EXTRACTOR FAILED ON: {field_name}:{e}')
                    result[field_name].append(None)
        return result #!EXIT!

 #? ======================================================== ?#
 #?                   EXTERNAL FUNCTIONS                     ?#
 #? ======================================================== ?#

    def fuzz_match_fields(self):
        pass


    
 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#

def test():
    url = 'https://www.environmentallights.com/21217-rgba65k-5050-60-24v-5m-gp.html'
    with JohnScraper(url) as scraper:
        if scraper.data is not None: 
            if LOG_MSG: log.success(f'SCRAPED DATA: {scraper.data}')
        else:
            if LOG_MSG: log.error(f'FAILED TO SCRAPE URL: {url}')
            pprint(scraper.data)

test()
 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#