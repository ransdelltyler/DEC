
#* ======================================================== *#
#*  ENVIRONMENTALLIGHTS.COM | BEAUTIFULSOUP4 RULESET MODULE                   
#* 
#*
#*
#* ======================================================== *#
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#

from selenium.webdriver.common.by import By
import pprint
from time import sleep

from html_retriever import HTMLRetriever
from util_classes import ColorLog
from variables import LOG_MSG
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#? ======================================================== ?#
#?                   PRE-PROCESS FUNCTION                   ?#
#? ======================================================== ?#
def preprocess_envirn(driver):
   if LOG_MSG: log.watchdog(f'RUNNING PREPROCESSOR w/ : {driver}')
   # Wait for the initial page load
   sleep(2)
      
   # Using "." instead of "text()" matches text inside nested spans (common in Magento)
   TAB_MAP = [
      '//*[@id="maincontent"]/div[4]/div/div[1]/section/div[1]',
      '//*[@id="maincontent"]/div[4]/div/div[1]/section/div[3]',
      '//*[@id="product-specifications-tab"]',
      '//*[@id="maincontent"]/div[4]/div/div[1]/section/div[7]'
   ]

   for xpath in TAB_MAP:
      try:
         # 1. Wait for PRESENCE (in the DOM), not "Clickable" (visible). 
         # This prevents timeouts if the element is off-screen or covered.
         button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath))
               )

         # 2. Force Scroll (Centers element to avoid sticky headers)
         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
         sleep(0.2) 
            
         # 3. JavaScript Click (Bypasses "element intercepted" errors)
         driver.execute_script("arguments[0].click();", button)
           
         print(f"Successfully clicked: {xpath}")
         sleep(1) 
            
      except Exception as e:
         # Log but don't crash; not all products have all tabs
         if LOG_MSG: log.warning(f"Tab not found or clickable: {xpath}")

   return driver.page_source
#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#
#? RETURNS A LIST OF TEXT REPRESENTING LIST ITEMS
def extract_list(selector):
    return lambda soup: [list_item.text for list_item in soup.select(selector)]

#? RETURN A LIST OF { 'PARAM' : VALUE }
def extract_specs(selector):
   def extractor(soup):
      rows = soup.select(selector)
      output = []
      
      for row in rows:
         th = row.select_one('th')
         td = row.select_one('td')

         if not td:
            continue

         label = th.get_text(strip=True) if th else td.get('data-th')
         value = td.get_text(strip=True)

         if label and value:
            output.append({ label : value })

      return output
   return extractor


#? RETURN A LIST OF RELATED PRODUCTS
def extract_related(selector):
   def extractor(soup):
      items = soup.select(selector)
      output = []
      
      for prod in items:
         name_tag = prod.select_one('a.product-item-link')
         pn_tag = prod.select_one('dd.product-item-number-value')

         name = name_tag.get('title') or name_tag.get_text(strip=True)
         url = name_tag.get('href')
         pn = pn_tag.get_text(strip=True) if pn_tag else None

         output.append({
            'name' : name,
            'url' : url,
            'pn' : pn,
         })

      return output
   return extractor


#? RETURN A LIST OF { DOCUMENT_NAME : URL_STRING }
def extract_docs(selector):
   def extractor(soup):
      docs = soup.select(selector)
      output = []
      
      for doc in docs:
         name = doc.get('download') or doc.get_text(strip=True)
         url = doc.get('href')
         if name and url:
            output.append({name : url})

      return output  
   return extractor


#~ ======================================================== ~#
#~                    RULES DEFINITION                      ~#
#~ ======================================================== ~#
#* ENVIRIONMENTAL LIGHTS SCRAPING PROFILES
DOMAIN_RULES = {
   "environmentallights.com": {
      "preprocess": preprocess_envirn, 
      "title": [
         lambda soup: soup.select_one("meta[property='og:title']").get("content"),
      ],

      "description": [
         lambda soup: soup.select_one("meta[name='description']").get("content"),
      ],

      "image_url": [
         lambda soup: soup.select_one("meta[property='og:image']").get("content"),
      ],

      "url": [
         lambda soup: soup.select_one("meta[property='og:url']").get("content"),
      ],

      "product_info": [
         # Select paragraphs specifically inside the "Product Features" ID
         lambda soup: [p.get_text(strip=True) for p in soup.select("#product-feature-content p") if p.get_text(strip=True)],
         
         # Select list items specifically inside the "Product Features" ID
         extract_list("#product-feature-content ul li"),
      ],

      "product_specs": [
         extract_specs("#product-specifications-content tbody tr")
      ],

      "related_products": [
         extract_related("ol.product-items li.product-item")
      ],

      "documents": [
         extract_docs("ul.product-detail-download-list li a.download-document-link")
      ],
    }
}

#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#

log = ColorLog('ENV_BS4', level=1)


def scrape_url(url):
   WAIT_FOR = (By.TAG_NAME, "body")
    
   with HTMLRetriever() as retriever:
      soup = retriever.retrieve_url(url, wait_for=WAIT_FOR)
      
   if not soup: 
      log.debug(f'FAILED TO LOAD PAGE: {url}')
      return None
   
   # TODO: DOMAIN SELECTION
   domain = "environmentallights.com"
   rules = DOMAIN_RULES[domain]
   
   result = {}
   for field_name, extractor_list in rules.items():
      if field_name == 'preprocess':
         continue
      
      result[field_name] = []
      for extractor in extractor_list:
         if LOG_MSG: log.watchdog(f'ATTEMPTING TO EXTRACT: {extractor}')
         sleep(0.5)
         try:
            result[field_name].append(extractor(soup))
            if LOG_MSG: log.debug(f'RESULT: {result[field_name]}')
         except Exception as e:
            if LOG_MSG: log.warning(f'EXTRACTOR FAILED ON: {field_name}:{e}')
            result[field_name].append(None)
   return result


def main():
   url = 'https://www.environmentallights.com/20910-pln-pf-rgb30k-10m.html'
   data = scrape_url(url)
   #pprint.pprint(data)


if __name__ == '__main__':
   main()