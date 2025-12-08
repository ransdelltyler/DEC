
#* ======================================================== *#
#*  ENVIRONMENTALLIGHTS.COM | BEAUTIFULSOUP4 RULESET MODULE                   
'''
BEAUTIFULSOUP4 RULESET MODULE FOR ENVIRIONMENTALLIGHTS.COM
- DEFINES EXTRACTION RULES FOR HTMLRETRIEVER CLASS
- USES bs4 TO PARSE HTML PAGES
- FUNCTIONS:
    - scrape_url(url:str) -> dict : Scrapes the given URL and returns a dictionary
      = { 'title': str, 'description': str, 'image_url': str, 'url': str,
          'product_info': List[str], 'product_specs': List[dict],
          'related_products': List[dict], 'documents': List[dict] }
'''
#* ======================================================== *#



import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[4])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import pprint

from DEEREATCHAIN.system.modules.html_retriever import HTMLRetriever
from DEEREATCHAIN.system.utils.util_classes import ColorLog
from DEEREATCHAIN.system.gen.settings import LOG_MSG
log = ColorLog('ENVIR_BS4')



#? ======================================================== ?#
#?                  INTERNAL FUNCTIONS                      ?#
#? ======================================================== ?#

#? RETURNS A LIST OF TEXT REPRESENTING LIST ITEMS
def _extract_list(selector):
    return lambda soup: [list_item.text for list_item in soup.select(selector)]

#? RETURN A LIST OF { 'PARAM' : VALUE }
def _extract_specs(selector):
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

      return output #!EXIT!
   return extractor #!EXIT!


#? RETURN A LIST OF RELATED PRODUCTS
def _extract_related(selector):
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

      return output #!EXIT!
   return extractor #!EXIT!


#? RETURN A LIST OF { DOCUMENT_NAME : URL_STRING }
def _extract_docs(selector):
   def extractor(soup):
      docs = soup.select(selector)
      output = []
      
      for doc in docs:
         name = doc.get('download') or doc.get_text(strip=True)
         url = doc.get('href')
         if name and url:
            output.append({name : url})

      return output #!EXIT!
   return extractor #!EXIT!


#~ ======================================================== ~#
#~                    RULES DEFINITION                      ~#
#~ ======================================================== ~#
#* ENVIRIONMENTAL LIGHTS SCRAPING PROFILES
DOMAIN_RULES = {
   "environmentallights.com": {
      "title": [
         lambda soup: soup.select_one("meta[property='og:title']").get("content"),
      ],
      
      "part_number": [
         lambda soup: soup.select_one("dd.product-number-value").text,
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
         _extract_list("#product-feature-content ul li"),
      ],

      "product_specs": [
         _extract_specs("#product-specifications-content tbody tr")
      ],

      "related_products": [
         _extract_related("ol.product-items li.product-item")
      ],

      "documents": [
         _extract_docs("ul.product-detail-download-list li a.download-document-link")
      ],
    }
}






#* ======================================================== *#
#*                   IMPLEMENTED INSIDE                     *#
#* ======================================================== *#

# TODO: TRANSFORM TO MULTIPLE DOMAIN RULESETS

#* JOHN_SCRAPER