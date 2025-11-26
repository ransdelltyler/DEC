 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
 #* GENERAL MANAGER
 #*
 #*
 #*
 #*
 #* ======================================================== *#


 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#
 
 # TODO: TAG MANAGER

 # TODO: FILE HANDLER [john_files.py]
    #^ - CREATE FOLDER STRUCTURE FOR SAVED HTML / IMAGES
    #^ - HOLDS MAP OF NAME : FOLDER PATHS 
    #^ -    USED TO ROUTE FILES I/O FROM SUB-SYSTEMS 
    #^ - LOAD / SAVE: 
    #^ -    EXCEL DATABASE
    #^ -    SCRAPED HTML / IMAGES
    #^ -    LOG FILES
    #^ -    SETTINGS
    #^ -    PROJECT FILES 
    #^ - LOGGING   
 # TODO: EXCEL DATABASE HANDLER [john_equipment.py]
    #^ - ADD, DELETE, UPDATE EQUIPMENT ENTRIES
    #^ - BACKUP / RESTORE DB
    #^ - READ / WRITE DATA_OBJS TO DB
    #^ - LOGGING
 # TODO: SCRAPER HANDLER [john_scraper.py]
    #^ - RUN 1 SHOT URL SCRAPING SESSIONS 
    #^ - LOAD / SAVE SCRAPED HTML / IMAGES
    #^ - SCRAPE URLS BASED ON DB ENTRIES
    #^ - LOGGING
 # TODO: PROJECT HANDLER [john_projects.py]
    #^ - BUILDS EQUIPMENT OBJECTS AS NEEDED WITH DB -> DATA_OBJS 
    #^ - CREATE / LOAD / SAVE PROJECTS
    #^ - MANAGE PROJECT EQUIPMENT LISTS
    #^ - LOGGING
 # TODO: USER INTERACTION FOR:
    #^ - DATABASE MANAGEMENT
    #^ - PROJECT MANAGEMENT
    #^ - BUILDER INTERFACE (CLI / GUI)
    #^ -
 # TODO: PROJECT OBJECTS
    #^ - ANCHOR
    #^ - ROOM
    #^ - SCENE / INSTALLATION
    #^ - EQUIPMENT INSTANCE
    #^ -


from util_classes import ColorLog
log = ColorLog('JOHN_JOHN')

class GenManager:
   def __init__(self):
      pass

   def start_subsystems(self):
      pass
   def stop_subsystems(self):
      pass
   def restart_subsystems(self):
      pass

 #* DATABASE HANDLER METHODS
   def load_db(self):
      pass
   def save_db(self):
      pass
   def backup_db(self):
      pass
   def restore_db(self):
      pass
   def archive_db(self):
      pass
   def add_db_entry(self):
      pass
   def delete_db_entry(self):
      pass
   def update_db_entry(self):
      pass
   def query_db(self):
      pass

 #* SCRAPER HANDLER METHODS
   def scrape_url(self):
      pass




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