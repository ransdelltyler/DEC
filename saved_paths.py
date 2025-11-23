
#* ======================================================== *#
#*                    FILE DESCRIPTION                   
#* 
#* SAVED PATH INFORMATION:
#* - SYSTEM:  NEEDED FOR BASIC FUNCTION
#* - LIBRARY: DYNAMICALLY ACCESSED AT RUNTIME | EXTERNAL SOURCES
#* - USER:    USER CREATED CONTENT / DB MIRRORS | USER SOURCES
#* 
#* 
#* SYSTEM FILE STRUCTURE:
#* - ROOT FOLDER
#* -    [SYS] FOLDER
#* -        - [JOHNS] 
#* -        - [SETTINGS] 
#* -        - [DATA_MODELS] 
#* -        - [UTIL_CLASSES] 
#* -        - [FACTORY] 
#* -        - [FACTORY] 
#* -    [] FOLDER

#* 
#* ======================================================== *#

import os
root_path = os.getcwd()

#* HOLDS LAST KNOWN-GOOD ROOT_PATH
#TODO: - UPDATED BY  
last_known_root = None


SYS_PATHS = {
    'root' : root_path,
    'settings' : '',

}

LIB_PATHS = {
    'root_db' : '',
    'excel_db' : '',
    'datasheet_db' : '',
    'html_db' : '',
    'image_db' : '',
    'model3D_db' : '',
    'pdf_db' : '',
    
}

USER_PATHS = {
    'root_user': '',
    'excel_user': '',
    'image_user': '',
    'model3D_user': '',
    'pdf_user': '',
    'url_user': '',

}