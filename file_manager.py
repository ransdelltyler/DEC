 #* ======================================================== *#
 #*                      FILE MANAGER                        
 #*
 #*
 #*
 #*
 #* ======================================================== *#

 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     
 # TODO: Create folder structures
 # TODO: Save files
 # TODO: Handle overwriting files
 # TODO: Track current directory position
 # TODO: Change path pointer
 # TODO: Save paths to local file paths.txt
# TODO: DEBUG MODE
# TODO: 
 # TODO:==================================================== ~#

#* STANDARD IMPORTS
import os
import time
from pathlib import Path


#* 3RD PARTY IMPORTS


#* CUSTOM CLASS IMPORTS
from util_classes import ColorLog
log = ColorLog('john_files', level=1)



# TODO: DYNAMICALLY MAPPED FOLDER TREE
# TODO: VERIFY FILE EXISTS

 #~ ======================================================== ~#
 #~                    FILE MANAGER CLASS                    ~#
 #~ ======================================================== ~#
class FileManager:
    def __init__(self, path=os.getcwd, file_map=None, masterlog_path=None, settings=None):
        
        #* [ROOT] APPLICATION PATH
        self.root_path = path

        #* [JOHN FILES] FILE MANIPULATION VARIABLES
        self.cur_path = path
        self.selected_file = None

        #* [FILE MAP] PATH
        self.file_map_path = file_map or self._create_if_missing('file_map.txt')

        #* [MASTER LOG] COLLECTOR PATH
        self.masterlog_path = masterlog_path or self._create_if_missing('master_log.txt')

        #* [SETTINGS] PATH
        self.settings = settings or self._create_if_missing('settings.txt')

        #* [COLORLOG] ENABLE / DISABLE
        self.show_logs = False
        

    #? SAVE OR CREATE FILE WITH OPTIONAL OVERWRITTING PERMISSION
    def _save_file(self,doc_name: str, doc_string: str | None=None,
                  overwrite=False):
        
        # OVERWRITES OR ENFORCES SINGLE COPY
        if overwrite: write_mode = 'w'
        else: write_mode = 'x'  
        if self.show_logs: log.debug(f'WRITE MODE:{write_mode}') #^DEBUG
        
        try: # CREATE FILE
            with open(doc_name, write_mode, encoding='utf-8')as f:
                if doc_string is not None: # WRITE DOC_STRING TO FILE
                    if self.show_logs: log.watchdog(f'WRITING DOCSTRING: {doc_name}') #^DEBUG
                    f.write(doc_string)
                    f.close()
                else: # ADD TIMESTAMP TO TOP OF EMPTY FILE AND CLOSE
                    f.write(f'#DOCUMENT CREATED BY SYSTEM: {time.time()}')
                    f.close()
        except FileExistsError:
            log.warning(f'FILE ALREADY EXISTS: {doc_name}!')

    #? CREATE A NEW FOLDER OR FOLDER TREE FROM PATH
    def _create_folder(self, folder_path: str,exist_ok=True):
        os.makedirs(folder_path, exist_ok=exist_ok)
        if self.show_logs: log.watchdog(f'CREATED NEW FOLDER PATH: {folder_path}')

    #& SETUP FUNCTIONS
    #? TRY TO FIND <FILE>, IF NOT FOUND CREATE EMPTY TEXT FILE
    def _create_if_missing(self, fname, path=None) -> str:
        # CREATE PATH OBJECT FOR RECURSIVE OPERATIONS
        root = Path(self.root_path)

        # SET INTEDED NEW_PATH (IF PROVIDED)
        if path is None:
            new_path = root / fname
        else:
            new_path = Path(path)
        
        # CHECK IF NEW_PATH EXISTS
        if new_path.exists():
            if self.show_logs:
                log.info(f'EXISTING FILE FOUND: {new_path}')
            return str(new_path) #!EXIT!

        # SEARCH RECURSIVELY
        if self.show_logs: log.warning(f'{new_path} NOT FOUND; SEARCHING {root}.')
        for file in root.rglob(fname):
            if file.is_file():
                if self.show_logs:
                    log.debug(f'FOUND FILE: {file}')
                return str(file) #!EXIT!
        
        # STILL NOT FOUND; CREATE NEW
        if self.show_logs: log.warning(f'{new_path}: STILL NOT FOUND, CREATING...')
        try:
            new_path.write_text(f"{fname}.txt | CREATED: {time.time()}", encoding='utf-8')
        except FileExistsError:
            log.critical(f'{fname} FOUND AT: {new_path}')
        
        return str(new_path) #!EXIT!    

    #? UPDATE PATH ATTRIBUTES
    def _set_path(self, attr:str, new_value=None, log_msg=None):
        if new_value is not None:
            setattr(self, attr, new_value)
            if log_msg and self.show_logs:
                log.watchdog(log_msg.format(new_value))
            return getattr(self, attr)
        
    #* GET/UPDATE /ROOT_DIR <PATH> 
    def _root_path(self, new_path=None):
        return self._set_path(F'root_path', new_path,'FILE MANAGER - [ROOT] PATH UPDATED TO : {}')

    #* GET/UPDATE MASTER_LOG.TXT <PATH> 
    def _logs_path(self, new_path=None):
        return self._set_path(F'root_path', new_path,'FILE MANAGER - [MASTER LOG] PATH UPDATED TO : {}')

    #* GET/UPDATE FILE_MAP.TXT <PATH>
    def _file_map(self, new_path=None):
        return self._set_path(F'root_path', new_path,'FILE MANAGER - [FILE MAP] PATH UPDATED TO : {}')

    #* GET/UPDATE SETTINGS.TXT <PATH>
    def _load_saved_settings(self, new_path=None):
        return self._set_path(F'settings', new_path, 'FILE MANAGER - [SETTINGS] PATH UPDATED TO : {}')

    #* GET/UPDATE CURRENT POINTER PATH
    def _cur_path(self, new_path=None):
        return self._set_path(F'cur_path', new_path, 'FILE MANAGER - [CUR_PATH] UPDATED TO {}')




    #? SEARCH FOR <FILE-NAME> STARTING IN ROOT FOLDER
    def cur_find_file(self, filename:str) -> str | None:
        root = self.root_path
        
        if self.show_logs: log.warning(f'SEARCHING {root} for {filename}')
        # RETURN ALL ITEMS LOWER THAN <ROOT> THAT MATCH <FILENAME>
        for file in root.rglob(filename):
            if file.is_file():
                if self.show_logs:
                    log.debug(f'FOUND FILE: {file}')
                return str(file) #!EXIT!
        
        # FAILED TO FIND
        if self.show_logs: log.error(f'{filename} could not be found.')
        return None #!EXIT!

            
    #? SAVE SELECTED <FILE OR FOLDER> TO NEW (<NAME> OR <LOCATION>)
    def cur_save_as(self, new_name:str, new_path:str):
        




 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#