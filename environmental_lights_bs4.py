 #* ======================================================== *#
 #*  ENVIRONMENTALLIGHTS.COM | BEAUTIFULSOUP4 RULESET MODULE                   
 #* 
 #*
 #*
 #* ======================================================== *#

 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#

 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#

 #? ======================================================== ?#
 #?                   EXTERNAL FUNCTIONS                     ?#
 #? ======================================================== ?#

 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#



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



 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#

 # TODO: DETERMINE PRODUCT TYPE

 
 
 
 #* --------- IMPLEMENTED 11/16 ---------
 #* ENVIRONMENTALLIGHTS.COM BS4 MINI-MODULE
 #! - UNTESTED 11/16
  # TODO: PAGE TYPE 
    #^ - soup.product
 # TODO: PAGE TITLE
    #^ - soup.title
 # TODO: MAIN IMAGE / GIF
    #^ - soup.image
 # TODO: DESCRIPTION
    #^ - soup.description
 # TODO: URL
    #^ - soup.url
 # TODO: PRODUCT INFO MAIN DESCRIPTION
    #^ - prod_features = soup.find('div', class_='product-detail-content')
    #^ - main_desc = prod_features.find('p')
    #^ - key_features = prod_features.find_all('li')
    #^ - key_features_list = field.factory(default_factory=list)
    #^ - for feature in key_features:
    #^ -    key_features_list.append(feature.get_text(strip=True))
 # TODO: PRODUCT SPECS TABLE
    #^ - spec_dict = field.factory(default_factory=dict)
    #^ - spec_table = soup.find('table', id='product-specs')
    #^ - rows = spec_table.find('tbody').find_all('tr')
    #^ - for row in rows: 
    #^     label = row.find('th', class_='label').get_text(strip=True)
    #^     value = row.find('td', class_='value').get_text(strip=True)
    #^     spec_dict[label] = value
 # TODO: RELATED PRODUCTS
    #^ - related_section = soup.find('ol', 'class_=products list items product-items')
    #^ - related_items = related_section.find_all(li, class_='item product product-item')
    #^ - related_list = field.factory(default_factory=list)
    #^ - for item in related_items:
    #^ -    related_dict = field.factory(default_factory=dict)
    #^ -    related_name = item.find('a', class_='product-item-link').get_text(strip=True)
    #^ -    related_url = item.find('a', class_='product photo product-item-photo').get('href')
    #^ -    related_image = item.find()
    #^ -    related_part_num = item.find('dd', class_='product-item-number-value').get_text(strip=True)
    #^ -    related_dict['name'] = related_name
    #^ -    related_dict['url'] = related_url
    #^ -    related_dict['part_number'] = related_part_num
    #^ -    related_dict['image'] = related_image
    #^ -    related_list.append(related_dict)
 # TODO: DOCUMENTATION DOWNLOADS
    #^ - docs_section = soup.find('ul', id='product-documents')
    #^ - docs_items = docs_section.find_all('a', class_='document-download-link')
    #^ - docs_list = field.factory(default_factory=list)
    #^ - for doc in docs_items:
    #^ -    doc_dict = field.factory(default_factory=dict)
    #^ -    doc_name = doc.get('download')
    #^ -    doc_url = doc.get('href')
