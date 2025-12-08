

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
from system.utils.data_models import EQCategory, LEDProd, Ctrlr, PSU, EQProto, GenDescr
from system.utils.factory import * 


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
            self.type = self.find_type()
            if LOG_MSG:
                log.success(f'SUCCESSFULLY SCRAPED DATA FROM URL: {url}')
                log.info(f'ATTEMPTING FUZZ MATCHING')
            


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
                if LOG_MSG: log.watchdog(f'ATTEMPTING TO EXTRACT: {field_name}')
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

    def find_type(self):
        if self.data:
            if 'strip light' in self.data['title']:
                return 'LED'
            if 'power supply' in self.data['title']:
                return 'POWER SUPPLY'
            if 'controller' in self.data['title']:
                return 'CONTROLLER'
            return 'UNKNOWN'
        return 'NO DATA'

    def find_EQProto(self):
        if self.data is not None:
            for _ in self.data['related_products']:
                if 'Pixel' or 'SPI' in _['name']:
                    return EQProto.SPI
                if 'DMX' in _['name']:
                    return EQProto.DMX
        return EQProto.UNKWN
    
    def find_ullisted(self):
        if self.data is not None:
            rating = self.data['product_specs'].get('Rating', '').lower()
            if 'ul' in rating:
                return GenDescr.YES
        return GenDescr.NO
    
    def find_cri(self):
        if self.data is not None:
            cri = self.data['product_specs'].get('CRI', 'Unknown CRI')
            return cri
        return 'DATA NOT SET'
            
    
    def fuzz_match_fields(self):
        pass
    
    
#    def build_led(self):
#        if not self.data:
#            if LOG_MSG: log.error('NO DATA TO BUILD LED PRODUCT FROM')
#            return None
#        else:
#            new_prod = new_ledprod(
#                name = self.data.get('title', 'Unknown LED Name')[0],
#                manuf = self.data['product_specs'].get('manufacturer', 'Unknown Manufacturer')[0],
#                vin = self.data['product_specs'].get('Input Voltage', 'Unknown Voltage')[0],
#                fixt_l_mm = self.data['product_specs'].get('Length (Metric)', 'Unknown Length')[0],
#                fixt_w_mm = self.data['product_specs'].get('Width (Metric)', 'Unknown Width')[0],
#                fixt_h_mm = self.data['product_specs'].get('Height (Metric)', 'Unknown Height')[0],
#                watt_ft = self.data['product_specs'].get('Power (Watts/ft)', 'Unknown Watt/ft')[0],
#                watt_m = self.data['product_specs'].get('Power (Watts/m)', 'Unknown Watt/ft')[0],
#                colors = self.data['product_specs'].get('Light Color', 'Unknown Colors')[0],
#                model = self.data.get('model', ['Unknown Model'])[0], #TODO: FIX THIS
#                partnum = self.data.get('part_number', ['Unknown Part Number'])[0], #TODO: FIX THIS
#                url = self.data.get('url', 'No URL Provided')[0],
#                m_roll = self.data['product_specs'].get('Power (Watts)', 'Unknown Meters/Roll')[0],
#                price = self.data.get('price', [0.0])[0], # TODO: FIX THIS
#                cutLen_in = self.data['product_specs'].get('Min. Cutting Increment (English)', 'Unknown Cut Length (in)')[0],
#                cutLen_mm = self.data['product_specs'].get('Min. Cutting Increment (Metric)', 'Unknown Cut Length (mm)')[0],
#                pixPitch_m = self.data['product_specs'].get('LED Density', 'Unknown LEDs per Meter')[0],
#                sub_pns = self.data.get('related_products', []),
#                shape = Shape.UNKWN, # TODO: FIX THIS
#                diffusion = Diffusion.UNKWN, # TODO: FIX THIS
#                viewAngle = self.data['product_specs'].get('Beam Angle', 'Unknown View Angle')[0],
#                cri = self.find_cri(), 
#                cct = self.data['product_specs'].get('CCT', 'Unknown CCT')[0], 
#                eqproto = self.find_EQProto(),
#                wireCode = '', # TODO: FIX THIS
#                datasheet = self.data['documents'].get('**Spec', 'No Datasheet Provided')[0],
#                ul_list = self.find_ullisted(), 
#                ul_recog = GenDescr.NO, # TODO: FIX THIS
#                cert_url = self.data['documents'].get('**Cert', 'No Certification URL Provided')[0], 
#                ip_rating = self.data['product_specs'].get('IP Rating', 'Unknown IP Rating')[0], 
#                finish = FinishColor.UNKWN, # TODO: FIX THIS
#                lumens_m = self.data['product_specs'].get('Brightness', 'Unknown Lumens/m')[0], 
#                lumens_ft = '' # TODO: FIX THIS
#            )

    
    def build_psu(self):
        pass
    
    def build_ctrlr(self):
        pass
    
 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#

def test():
    url = 'https://www.environmentallights.com/20910-pln-pf-rgb30k-10m.html'
    with JohnScraper(url) as scraper:
        if scraper.data is not None: 
            if LOG_MSG: log.success(f'SCRAPED DATA:')
            pprint(scraper.data)
        else:
            if LOG_MSG: log.error(f'FAILED TO SCRAPE URL: {url}')
            pprint(scraper.data)

test()
 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#