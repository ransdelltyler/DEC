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
 # TODO:==================================================== ~#

 #* IMPORTS
import os



 #~ ======================================================== ~#
 #~                    FILE MANAGER CLASS                    ~#
 #~ ======================================================== ~#
class FileManager:
    def __init__(self, path=os.getcwd):
        
        cur_path = path

        
        
        pass
    

 #? ======================================================== ?#
 #?                     HELPER FUNCTIONS                     ?#
 #? ======================================================== ?#
    def _overwrite(self):
        pass
    
    def _update_FMdir(self):
        pass

    def _update_path_file(self):
        pass
    
    def _load_path_file(self):
        pass

    def _update_cur_path(self):
        pass

    def _update_timestamp(self):
        pass
 #? ======================================================== ?#
 #?                    EXTERNAL FUNCTIONS                    ?#
 #? ======================================================== ?#

    def save_file(self, docstring: str, extension: str):
        pass

    def create_folder(self,):
        pass
    


 #^ ======================================================== ^#
 #^                    TESTING / EXAMPLES                    ^#
 #^ ======================================================== ^#

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#