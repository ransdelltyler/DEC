

 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
'''
    SYSTEM SCRAPER MODULE
    - USES BEAUTIFULSOUP TO SCRAPE HTML PAGES
    - USES DOMAIN RULES TO EXTRACT DATA FIELDS
    - FUNCTIONS:
        - __init__(url: str) : Initialize scraper and scrape URL
        - get_host(url: str) : Extract host domain from URL
        - scrape_url(url: str) : Scrape URL using domain rules
        - find_type() : Determine type of product from scraped data
        - find_EQProto() : Find equivalent protocol from scraped data
        - find_ctrl_type() : Find controller type from scraped data
        - find_ullisted(specs) : Determine if product is UL listed
        - find_cri(specs) : Find CRI value from scraped data
        - find_shape() : Determine shape of product from scraped data
        - find_dict_val(key: str, datalist: list[dict]) : Find value for key in list of dictionaries
        - volt_to_enum(volt_str: str) : Convert voltage string to Voltage enum
        - fuzz_match_fields() : Fuzzy match fields (placeholder)
        - build_led() : Create LED product object from scraped data
        - build_psu() : Create Power Supply product object from scraped data
        - build_ctrlr() : Create Controller product object from scraped data
    - DEPENDENCIES:
        - beautifulsoup4
        - openpyxl
        - system.modules.html_retriever
        - system.utils.data_models
        - system.utils.factory


'''
#*             IMPLEMENTED INSIDE JOHN_EQUIPMENT            *#
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
from system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog

log = ColorLog('JOHN_SCRAPER')

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#

class JohnScraper:
    def __init__(self, url: str):
        self.data = self.scrape_url(url)
        self.new_equipment = None
        if not self.data:
            if LOG_MSG: log.debug(f'NO DATA SCRAPED FROM URL: {url}')
        else:
            if LOG_MSG:
                log.success(f'SUCCESSFULLY SCRAPED DATA FROM URL: {url}')
            
            # SET PRODUCT TYPE AND BUILD EQUIPMENT OBJECT
            self.type = self.find_type()
            log.debug(f'PRODUCT TYPE IDENTIFIED AS: {self.type}')
            if self.type == 'LED':
                self.new_equipment = self.build_led()
            elif self.type == 'POWER SUPPLY':
                self.new_equipment = self.build_psu()
            elif self.type == 'CONTROLLER':
                self.new_equipment = self.build_ctrlr()

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

    
    #? FIND TYPE OF PRODUCT
    def find_type(self):
        if self.data:
            if 'strip light' or 'reel' in self.data['title']:
                return 'LED'
            if 'power supply' in self.data['title']:
                return 'POWER SUPPLY'
            if 'controller' in self.data['title']:
                return 'CONTROLLER'
            return 'UNKNOWN'
        return 'NO DATA'

    
    #? FIND EQUIVALENT PROTOCOL
    def find_EQProto(self):
        if self.data is not None:
            for _ in self.data['related_products']:
                if 'Pixel' or 'SPI' in _['name']:
                    return EQProto.SPI
                if 'DMX' in _['name']:
                    return EQProto.DMX
        return EQProto.UNKWN
    
    
    #? FIND CONTROLLER TYPE
    def find_ctrl_type(self):
        if self.data is not None:
            for _ in self.data['product_specs']:
                if 'Pixel' or 'SPI' in _['name']:
                    return CTRLType.PIXEL
                if 'DMX' in _['name']:
                    return CTRLType.DMX
        return CTRLType.UNKWN
    
    #? UL LISTED
    def find_ullisted(self, specs) -> GenDescr:
        if self.data is not None:
            rating = self.find_dict_val('Rating', specs) or ''
            if 'ul' in rating.lower():
                return GenDescr.YES
        return GenDescr.NO
    
    #? FIND CRI OF PRODUCT
    def find_cri(self, specs) -> str:
        if self.data is not None:
            cri = self.find_dict_val('CRI', specs) or ''
            return cri
        return 'DATA NOT SET'
    
    #? FIND SHAPE OF PRODUCT
    def find_shape(self) -> Shape:
        if self.data is not None:
            shape = None
            if shape is not None:
                shape = shape.lower()
                if 'round' in shape or 'dome' in shape:
                    return Shape.DOMED
                if 'square' in shape or 'flat' in shape:
                    return Shape.SQUARE
                if '360' in shape:
                    return Shape.FLEX360
        return Shape.UNKWN
    
    
    #? FIND VALUE FOR KEY IN DICTIONARY LIST
    def find_dict_val(self, key: str, datalist: list[dict]) -> str | None:
        if self.data is not None:
            for item in datalist:
                if key in item:
                    print(item[key])
                    return item[key]
        return None
    
    
    
    #? CONVERT STR TO VOLTAGE ENUM
    def volt_to_enum(self, volt_str: str) -> Voltage:
        volt_str = volt_str.lower()
        if '120' in volt_str:
            return Voltage.V120
        if '5' in volt_str:
            return Voltage.V05
        if '12' in volt_str:
            return Voltage.V12
        if '24' in volt_str:
            return Voltage.V24
        if '52' in volt_str or 'poe' in volt_str:
            return Voltage.VPOE
        return Voltage.UNKWN
    
    
    #? FUZZY MATCH FIELDS
    def fuzz_match_fields(self):
        pass
    
    
    #? CREATE LED PRODUCT OBJECT
    def build_led(self):
        if not self.data:
            if LOG_MSG: log.error('NO DATA TO BUILD LED PRODUCT FROM')
            return None
        else:
            specs = self.data.get('product_specs', {})
            specs = specs[0] if isinstance(specs, list) and len(specs) > 0 else specs
            log.info(f'Building LED product with specs: {specs}')
            if len(specs) > 0:
                return new_ledprod(
                    name = self.data.get('title', 'Unknown LED Name')[0],
                    manuf = self.find_dict_val('Manufacturer', specs) or 'Unknown Manufacturer',
                    vin = self.volt_to_enum(self.find_dict_val('Input Voltage', specs) or ''),
                    fixt_l_mm = self.find_dict_val('Length (Metric)', specs) or 'Unknown Length',
                    fixt_w_mm = self.find_dict_val('Width (Metric)', specs) or 'Unknown Width',
                    fixt_h_mm = self.find_dict_val('Height (Metric)', specs) or 'Unknown Height',
                    watt_ft = self.find_dict_val('Power (Watts/ft)', specs) or 'Unknown Power (Watts/ft)',
                    watt_m = self.find_dict_val('Power (Watts/m)', specs) or 'Unknown Power (Watts/m)',
                    colors = self.find_dict_val('Light Color', specs) or 'Unknown Light Color',
                    model = self.data.get('title', 'Unknown Model')[0].split('-',1)[0],
                    partnum = self.data.get('part_number', 'Unknown Part Number')[0],
                    url = self.data.get('url', 'No URL Provided')[0],
                    m_roll = self.find_dict_val('Meters/Roll', specs) or 'Unknown Meters/Roll',
                    price = self.data.get('price', [0.0])[0], # TODO: FIX THIS
                    cutLen_in = self.find_dict_val('Min. Cutting Increment (English)', specs) or 'Unknown Min. Cutting Increment (English)',
                    cutLen_mm = self.find_dict_val('Min. Cutting Increment (Metric)', specs) or 'Unknown Min. Cutting Increment (Metric)',
                    pixPitch_m = self.find_dict_val('LED Density', specs) or 'Unknown LED Density',
                    sub_pns = self.data.get('related_products', []),
                    shape = self.find_shape(),
                    diffusion = Diffusion.UNKWN, # TODO: FIX THIS
                    viewAngle = self.find_dict_val('Beam Angle', specs) or 'Unknown View Angle',
                    cri = self.find_cri(specs), 
                    cct = self.find_dict_val('CCT', specs) or 'Unknown CCT', 
                    eqproto = self.find_EQProto(),
                    wireCode = '', # TODO: FIX THIS
                    datasheet = self.find_dict_val('**Datasheet', self.data.get('documents', {})) or 'No Datasheet Provided',
                    ul_list = self.find_ullisted(specs), 
                    ul_recog = GenDescr.NO, # TODO: FIX THIS
                    cert_url = self.find_dict_val('**Cert', self.data.get('documents', {})) or 'No Certification URL Provided',
                    ip_rating = self.find_dict_val('IP Rating', specs) or 'Unknown IP Rating', 
                    finish = FinishColor.UNKWN, # TODO: FIX THIS
                    lumens_m = self.find_dict_val('Brightness', specs) or 'Unknown Brightness', 
                    lumens_ft = '' # TODO: FIX THIS
                )
    
    #? CREATE POWER SUPPLY PRODUCT OBJECT
    def build_psu(self):
        if not self.data:
            if LOG_MSG: log.error('NO DATA TO BUILD POWER SUPPLY FROM')
            return None
        else:
            specs = self.data.get('product_specs', {})
            specs = specs[0] if isinstance(specs, list) and len(specs) > 0 else specs
            log.info(f'Building power supply with specs: {specs}')
            if specs and len(specs) > 0:
                return new_psu(
                    name = self.data.get('title', 'Unknown PSU Name')[0],
                    manuf = self.find_dict_val('Manufacturer', specs) or 'Unknown Manufacturer',
                    vin = self.volt_to_enum(self.find_dict_val('Input Voltage', specs) or ''),
                    vout = self.volt_to_enum(self.find_dict_val('Output Voltage', specs) or ''), #TODO: FIX
                    l_mm = self.find_dict_val('Length (Metric)', specs) or 'Unknown Length',
                    w_mm = self.find_dict_val('Width (Metric)', specs) or 'Unknown Width',
                    h_mm = self.find_dict_val('Height (Metric)', specs) or 'Unknown Height',
                    rated_watts = self.find_dict_val('Power (Watts)', specs) or 'Unknown Rated Power (Watts)',
                    power_w = self.find_dict_val('Max. Output Power (Watts)', specs) or 'Unknown Max. Output Power (Watts)',
                    model = self.data.get('title', 'Unknown Model')[0].split('-',1)[0],
                    partnum = self.data.get('part_number', ['Unknown Part Number'])[0],
                    url = self.data.get('url', 'No URL Provided')[0],
                    price = self.data.get('price', [0.0])[0], # TODO: FIX THIS
                    documents = self.data.get('documents', {}),
                )


    #? CREATE CONTROLLER PRODUCT OBJECT
    def build_ctrlr(self):
        if not self.data:
            if LOG_MSG: log.error('NO DATA TO BUILD CONTROLLER FROM')
            return None
        else:
            specs = self.data.get('product_specs', {})
            specs = specs[0] if isinstance(specs, list) and len(specs) > 0 else specs
            log.info(f'Building controller with specs: {specs}')
            if specs and len(specs) > 0:
                return new_ctrlr(
                    name = self.data.get('title', 'Unknown Controller Name')[0],
                    manuf = self.find_dict_val('Manufacturer', specs) or 'Unknown Manufacturer',
                    vin = self.volt_to_enum(self.find_dict_val('Input Voltage', specs) or ''),
                    l_mm = self.find_dict_val('Length (Metric)', specs) or 'Unknown Length',
                    w_mm = self.find_dict_val('Width (Metric)', specs) or 'Unknown Width',
                    h_mm = self.find_dict_val('Height (Metric)', specs) or 'Unknown Height',
                    rated_watts = self.find_dict_val('Power (Watts)', specs) or 'Unknown Rated Power (Watts)',
                    ctrl_type = self.find_ctrl_type(),
                    model = self.data.get('title', 'Unknown Model')[0].split('-',1)[0],
                    partnum = self.data.get('part_number', ['Unknown Part Number'])[0],
                    url = self.data.get('url', 'No URL Provided')[0],
                    price = self.data.get('price', [0.0])[0], # TODO: FIX THIS
                )
    

