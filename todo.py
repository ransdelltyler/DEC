
#! TODO LIST:

#? data_objs.py
# TODO: LED Fixture
# TODO: CTRLR
# TODO: 


#? url_scraper.py
# TODO: COLORFUL COMMENTS
# TODO: SCRAPE DATA BASED ON KEYWORDS FROM keywords.pys
# TODO: UPDATE MULTIPLE COLUMNS AT ONCE
# TODO: ADD / DELETE ROWS
# TODO: CLASS
#^ General scraping flow:
# Enter URL
# - Check for existing saved URL
#   - If exists, load saved HTML
#   - If not, check robots.txt
#     - If allowed, use Selenium to fetch dynamic content
#       - Save HTML to local file
#       - Save Image of webpage
#     - If not allowed, log and skip
#   - Parse HTML with BeautifulSoup
#     - Load keyword terms from keywords.py
#     - Search HTML for keyword value pairs
#     - Manually enter missing data
#     - Present complete data for user review
#       - Store results in data_objs.py structures
#       - Save results to excel database
#       - Backup to txt as readable data_objs


#? main.py
# TODO:


#? keywords.py
# TODO:


#? util_classes.py 
# TODO: 





#* DATA SENDER MODULES
#? sacn_sender.py
# TODO: Create class
# TODO: Data streams

#? dmx_ctrlr.py
# TODO: Packet handler

#? led_ctrlr.py
# TODO: Basic LED controller
#* 



