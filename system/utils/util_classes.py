
#* ======================================================== *#
'''                    FILE DESCRIPTION                   






'''

import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# GLOBAL VARIABLES IMPORT
from system.gen import settings




#~ ======================================================== ~#
#~                COLOR-LOG CLASS DEFINITION                ~#
#~ ======================================================== ~#

import logging
from colorlog import ColoredFormatter
from pathlib import Path

#? MAXIMUM ONE-LINE MSG CHARS
MAX_CHARS = 150
#? 

#? MULTI-LINE NESTED INDENT SPACES
DEF_INDENT = 4
#? FILLER CHAR(2)
FILLER = ' -'

#* CUSTOM LOG STATUSES
SUCCESS = 25
WATCHDOG = 100
BORDER = 1
logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(WATCHDOG, 'WATCHDOG')
logging.addLevelName(BORDER, 'BORDER')


#* EMOJI MAP FOR LOG STATUSES
Emoji_Map = {
    logging.DEBUG: "⚕",
    logging.WARNING: "⚠",
    logging.ERROR: "⚠⚠",
    logging.CRITICAL: "X",
    logging.INFO: "🛈",
    WATCHDOG: "⛨",
    SUCCESS: "☀",
    BORDER: '𓃵 | ___ 𓃵 ___ |',
}

#* LOG COLOR CONFIGURATION
log_colors={
    "DEBUG":        "light_cyan",
    "INFO":         "white",
    "WARNING":      "yellow",
    "ERROR":        "light_red",
    "CRITICAL":     "bg_red",
    "SUCCESS":      "bold_green",
    "WATCHDOG":     "blue",
    "BORDER":       "light_black",
}

#* LOG FILE PATH
class ColorLog:
    def __init__(self, name=__name__, level=BORDER, path="main.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.name = name
        
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            console_formatter = ColoredFormatter(
                "%(log_color)s %(levelname)s %(msg)s",
                log_colors=log_colors
            )
            console_handler.setFormatter(console_formatter)

            file_handler = logging.FileHandler(path)
            file_handler.setLevel(level)

            file_formatter = logging.Formatter(
                "%(levelname)s %(msg)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            
    
    #? CHECKS MSG LENGTH TO MAX_CHAR
    #? CUT OFF OR FILL TO END -> STR (SINGLE-LINE)
    def cut_or_fill(self, msg : str) -> str:
        #? CALCULATE NUMBER OF FILLER STR TO ADD
        fillmult = (MAX_CHARS - len(msg)) - len(FILLER)
        
        #? CUT OVER-LENGTH MSG
        if len(msg) > MAX_CHARS:
            output = msg[:MAX_CHARS-2] + ' |'
        #? FILL UNDER-LENGTH MSG
        else:
            output = msg + (FILLER*fillmult)
        return output
    
    
    #? CLEANS OR REJECTS MSG INPUT
    def clean_msg(self, msg: str | list[str] | list[tuple]) -> str:
        #? STRING MSG
        if isinstance(msg, str):
            clean_msg = self.cut_or_fill(msg=msg)
            return clean_msg
        
        #? LIST MSG
        elif isinstance(msg, list):
            output = ''
            for text in msg:
                if isinstance(text, str):
                    clean_msg = self.clean_msg(msg=text)
                    clean_msg += clean_msg + '\n'
                    
                #? LIST OF TUPLES
                elif isinstance(text, tuple):
                    clean_msg = self.cut_or_fill(msg=text[1])
                    if text[0] == 'BORDER':
                        clean_msg += clean_msg + '\n'
            return output
    
    
    
    def debug(self, msg):
        
        self.logger.debug(f"---- {Emoji_Map[logging.DEBUG]} | {self.name} | {msg}")

    def info(self, msg):
        
        self.logger.info(f"----- {Emoji_Map[logging.INFO]} | {self.name} | {msg}")

    def warning(self, msg):
        
        self.logger.warning(f"-- {Emoji_Map[logging.WARNING]} | {self.name} | {msg}")

    def error(self, msg):
        
        self.logger.error(f"--- {Emoji_Map[logging.ERROR]} | {self.name} | {msg}")

    def critical(self, msg):
        
        self.logger.critical(f"- {Emoji_Map[logging.CRITICAL]} | {self.name} | {msg}")

    
    def success(self, msg):
        
        self.logger.log(SUCCESS, f"-- {Emoji_Map[SUCCESS]} | {self.name} | {msg}")

    def watchdog(self, msg):
        
        self.logger.log(WATCHDOG, f"- {Emoji_Map[WATCHDOG]} | {self.name} | {msg}")

    def border(self, msg : str | None=None):
        
        self.logger.log(BORDER, f"--- {Emoji_Map[BORDER]} | {self.name} | [{msg}]")



#^ ======================================================== ^#
#^               COLORLOG TESTING / EXAMPLES                ^#
#^ ======================================================== ^#
def test():
    logger = ColorLog('UTIL_CLOG', level=BORDER)

    logger.debug("This is a debug msg.")
    logger.info("This is an info msg.")
    logger.success("This is a success msg.")
    logger.warning("This is a warning msg.")
    logger.error("This is an error msg.")
    logger.critical("This is a critical msg.")
    logger.watchdog("This is a watchdog msg.")
    logger.border()

#test()



