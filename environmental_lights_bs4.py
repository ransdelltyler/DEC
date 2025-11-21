
#* ======================================================== *#
#*  ENVIRONMENTALLIGHTS.COM | BEAUTIFULSOUP4 RULESET MODULE                   
#* 
#*
#*
#* ======================================================== *#
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#


#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#




#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#
#? RETURNS A LIST OF TEXT REPRESENTING LIST ITEMS
def extract_list(selector):
    return lambda soup: [list_item.text for list_item in soup.select(selector)]

#? RETURN A LIST OF { 'PARAM' : VALUE }
def extract_specs(selector):
   def extractor(soup):
      params = soup.select(selector)
      spec_list = []

      for p in params:
         th = p.select_one('th')
         td = p.select_one('td')

         if not td:
            continue

         label = None
         if th:
            label = th.get_text(strip=True)
         else: # BACKUP LABEL NAME
            label = td.get('data-th')
         
         value = td.get_text(strip=True)

         if label and value:
            spec_list.append({ label : value })

      return spec_list
   return extractor


#? RETURN A LIST OF RELATED PRODUCTS
def extract_related(selector):
   def extractor(soup):
      items = soup.select(selector)
      related = []

      for prod in items:
         name_tag = prod.select_one('a.product-item-link')
         pn_tag = prod.select_one('dd.product-item-number-value')

         name = name_tag.get('title') or name_tag.get_text(strip=True)
         url = name_tag.get('href')
         pn = pn_tag.get_text(strip=True) if pn_tag else None

         related.append({
            'name' : name,
            'url' : url,
            'pn' : pn,
         })

      return related
   return extractor


#? RETURN A LIST OF { DOCUMENT_NAME : URL_STRING }
def extract_docs(selector):
   def extractor(soup):
      docs = soup.select(selector)

      doc_list = []
      
      for doc in docs:
         file = doc.select_one('a.download-document-link')
         if file:
            name = file.get('download') or file.get_text(strip=True)
            url = file.get('href')

            if name and url:
               doc_list.append({name : url})

      return doc_list  
   return extractor


#~ ======================================================== ~#
#~                    RULES DEFINITION                      ~#
#~ ======================================================== ~#
#* ENVIRIONMENTAL LIGHTS SCRAPING PROFILES
DOMAIN_RULES = {
   ".environmentallights.com": {
      "title": [
         lambda soup: soup.select_one("meta[property='og:title']").get("content"),
      ],

      "description": [
         lambda soup: soup.select_one("meta[property='description']").get("content"),
      ],

      "image_url": [
         lambda soup: soup.select_one("meta[property]='og:image']").get("content"),
      ],

      "url": [
         lambda soup: soup.select_one("meta[property]='og:url'").get("content"),
      ],

      "product_info": [
         lambda soup: [ p.text for p in soup.select_one("ul.product-detail-content p")],
         extract_list("ul.product-feature-content li"),
      ],

      "product_specs": [
         extract_specs("table.product-specs tr")
      ],

      "related_products": [
         extract_related("ol.product-items li.product-item")
      ],

      "documents": [
         extract_docs("ul.product-documents li")
      ],
    }
}
