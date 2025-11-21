 #* ======================================================== *#
 #*                    FILE DESCRIPTION                   
 #*
 #*
 #*
 #*
 #* ======================================================== *#

 # TODO:==================================================== ~#
 # TODO:              TODO LIST / DEVLOG                     ~#
 # TODO:==================================================== ~#

#^ IMPORTS


 #~ ======================================================== ~#
 #~                    CLASS DEFINITION                      ~#
 #~ ======================================================== ~#

class John_Files:
    def __init__(self):
        pass



 #? ======================================================== ?#
 #?                    HELPER FUNCTIONS                      ?#
 #? ======================================================== ?#
 #* SETUP FUNCTIONS
    
    #* FINDS ALL REQUIRED FILES AND TRANSLATES TO FILE_MAP.TXT
    def _find_req_files(self):
        pass
    
    #* LOCATE EQUIPMENT DATABASE BY <PATH> OR SEARCH FROM ROOT
    def _equipdb_path(self):
        pass
    
    #* SAVE / UPDATE ROOT PATH
    def _root_path(self):
        pass
    
    #* ADD NEW/EXISTING <LOG_PATH> TO MASTER LOG
    def _logs_path(self):
        pass
    
    #* UPDATE FILE_MAP.TXT WITH 
    def _update_file_map(self):
        pass

    #* LOAD SETTINGS FILES FROM <PATH>
    def _load_saved_settings(self):
        pass


 #* GENERAL FOLDER FUNCTIONS
    #* ADDS FOLDER <PATH> TO FILE_MAP.TXT
    def _add_folder(self, path:str):
        pass

    #* CREATES NEW FOLDER WITH <NAME> AT <PATH>
    def _create_folder(self, path:str, name:str):
        pass
    
    def _(self):
        pass


 #? ======================================================== ?#
 #?                   EXTERNAL FUNCTIONS                     ?#
 #? ======================================================== ?#
    #* SEARCH FOR <FILE NAME> IN FOLDER TREE
    #* -> PATH
    def find_file(self):
        pass
    
    #* SAVE EXISTING <FILE> TO NEW (<NAME> OR <LOCATION>)
    def save_as(self, cur_path:str, name:str, loc:str):
        
        pass
    
    #* CREATE BASIC PROJECT FOLDER / FILE STRUCTURE AT <PATH>
    def create_project(self):
        pass
    
    #* CREATE AND MAP PATH FOR NEW LOG FILE
    def add_log(self):
        pass


 #^ ======================================================== ^#
 #^                   TESTING / EXAMPLES                     ^#
 #^ ======================================================== ^#

 #! ======================================================== !#
 #!                       MAIN BLOCK                         !#
 #! ======================================================== !#