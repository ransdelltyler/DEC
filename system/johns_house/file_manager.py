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
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# GLOBAL VARIABLES IMPORT
from system.gen import gvars
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_FILE')



#* STANDARD IMPORTS
import time
from pathlib import Path


# TODO: DYNAMICALLY MAPPED FOLDER TREE
# TODO: VERIFY FILE EXISTS

 #~ ======================================================== ~#
 #~                    FILE MANAGER CLASS                    ~#
 #~ ======================================================== ~#
class FileManager:
    def __init__(self, path=os.getcwd, file_map=None, masterlog_path=None, settings=None):
        
        #* [ROOT] APPLICATION PATH
        self.root_path = Path(path)

        #* [JOHN FILES] FILE MANIPULATION VARIABLES
        self.cur_path = Path(path)
        self.sel_path = Path(path)

        #* [FILE MAP] PATH
        self.file_map_path = file_map or self._create_if_missing('file_map.txt')
        self.file_map_path = Path(self.file_map_path)

        #* [MASTER LOG] COLLECTOR PATH
        self.masterlog_path = masterlog_path or self._create_if_missing('master_log.txt')
        self.masterlog_path = Path(self.masterlog_path)
        
        #* [SETTINGS] PATH
        self.settings_path = settings or self._create_if_missing('settings.txt')
        self.settings_path = Path(self.settings_path)
        

    #& CONTEXT MANAGER 1/2
    def __enter__(self):
        if gvars.LOG_MSG:
            log.border()
            log.watchdog(' STARTING ')
        return self
    #& CONTEXT MANAGER 2/2
    def __exit__(self, exc_type, exc_val, exc_tb):
        if gvars.LOG_MSG:
            log.watchdog(' SHUTTING DOWN ')
            log.border()
        return False
            

    #? SAVE OR CREATE FILE WITH OPTIONAL OVERWRITTING PERMISSION
    def _save_file(self,doc_name: str, doc_string: str | None=None, overwrite=False):
        
        # OVERWRITES OR ENFORCES SINGLE COPY
        write_mode = 'w' if True else 'x'
        if gvars.LOG_MSG: log.debug(f'WRITE MODE:{write_mode}') #^DEBUG
        
        try: # CREATE FILE
            with open(doc_name, write_mode, encoding='utf-8')as f:
                if doc_string is not None: # WRITE DOC_STRING TO FILE
                    if gvars.LOG_MSG: log.watchdog(f'WRITING DOCSTRING: {doc_name}') #^DEBUG
                    f.write(doc_string)
                    f.close()
                else: # ADD TIMESTAMP TO TOP OF EMPTY FILE AND CLOSE
                    f.write(f'#DOCUMENT CREATED BY SYSTEM: {time.time()}')
                    f.close()
        except FileExistsError:
            if gvars.LOG_MSG: log.warning(f'FILE ALREADY EXISTS: {doc_name}!') #^DEBUG

    #? CREATE A NEW FOLDER OR FOLDER TREE FROM PATH
    def _create_folder(self, folder_path: str,exist_ok=True):
        os.makedirs(folder_path, exist_ok=exist_ok)
        if gvars.LOG_MSG: log.watchdog(f'CREATED NEW FOLDER PATH: {folder_path}')

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
            if gvars.LOG_MSG:
                log.info(f'EXISTING FILE FOUND: {new_path}')
            return str(new_path) #!EXIT!

        # SEARCH RECURSIVELY
        if gvars.LOG_MSG: log.warning(f'{new_path} NOT FOUND; SEARCHING {root}.')
        for file in root.rglob(fname):
            if file.is_file():
                if gvars.LOG_MSG: log.debug(f'FOUND FILE: {file}') #^DEBUG
                return str(file) #!EXIT!
        
        # STILL NOT FOUND; CREATE NEW
        if gvars.LOG_MSG: log.warning(f'{new_path}: STILL NOT FOUND, CREATING...') #^DEBUG
        try:
            new_path.write_text(f"{fname} | CREATED: {time.time()}", encoding='utf-8')
        except FileExistsError:
            if gvars.LOG_MSG: log.critical(f'{fname} FOUND AT: {new_path}') #^DEBUG
        return str(new_path) #!EXIT!    


    #? UPDATE PATH ATTRIBUTES
    def __setattr__(self, name: str, value: str) -> None:
        if 'path' in name:
            new_path = Path(value)
            _ = self.__getattribute__(name)
            self._create_if_missing(value)
            super().__setattr__(name, new_path)
            if gvars.LOG_MSG: log.info(f'UPDATING {name} -> {value}') #^DEBUG


    #? SEARCH FOR <FILE-NAME> STARTING IN ROOT FOLDER
    def cur_find_file(self, filename:str) -> str | None:
        root = self.root_path
        
        if gvars.LOG_MSG: log.warning(f'SEARCHING {root} for {filename}')
        # RETURN ALL ITEMS LOWER THAN <ROOT> THAT MATCH <FILENAME>
        for file in root.rglob(filename):
            if file.is_file():
                if gvars.LOG_MSG: log.debug(f'FOUND FILE: {file}') #^DEBUG
                return str(file) #!EXIT!
        
        # FAILED TO FIND
        if gvars.LOG_MSG: log.error(f'{filename} could not be found.')
        return None #!EXIT!

            
    #? SAVE SELECTED <FILE OR FOLDER> TO NEW (<NAME> OR <LOCATION>)
    def save_sel_as(self, new_name: str, new_path: str | Path):
        src = self.sel_path
        dest = Path(new_path) if isinstance(new_path, str) else new_path
        new_path = dest / new_name
        src.rename(new_path)

    def get_subdirs(self, start_dir='.'):
        pass

#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#

def test():
    with FileManager() as fm:
        pass        
 