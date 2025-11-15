
#? LOGGING CLASS BLOCK

import logging
from colorlog import ColoredFormatter
from pathlib import Path

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
    logging.CRITICAL: "  ⛌ ⛌ ⛌  ",
    logging.INFO: "🛈",
    WATCHDOG: "⛨",
    SUCCESS: "☀",
    BORDER: ' ⌞ ___ 𓃵 ___ ⌝  ',
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
path_log = Path("util.log")

class ColorLog:
    def __init__(self, name=__name__, level=BORDER):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)

            console_formatter = ColoredFormatter(
                "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
                log_colors=log_colors
            )
            console_handler.setFormatter(console_formatter)

            file_handler = logging.FileHandler(path_log)
            file_handler.setLevel(level)

            file_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def debug(self, message): self.logger.debug(f"{Emoji_Map[logging.DEBUG]} {message} {Emoji_Map[logging.DEBUG]}")
    def info(self, message): self.logger.info(f"{Emoji_Map[logging.INFO]} {message} {Emoji_Map[logging.INFO]}")
    def warning(self, message): self.logger.warning(f"{Emoji_Map[logging.WARNING]} {message} {Emoji_Map[logging.WARNING]}")
    def error(self, message): self.logger.error(f"{Emoji_Map[logging.ERROR]} {message} {Emoji_Map[logging.ERROR]}")
    def critical(self, message): self.logger.critical(f"{Emoji_Map[logging.CRITICAL]} {message} {Emoji_Map[logging.CRITICAL]}")
    
    def success(self, message): self.logger.log(SUCCESS, f"{Emoji_Map[SUCCESS]} {message} {Emoji_Map[SUCCESS]}")
    def watchdog(self, message): self.logger.log(WATCHDOG, f"{Emoji_Map[WATCHDOG]} {message} {Emoji_Map[WATCHDOG]}")
    def border(self, message): self.logger.log(BORDER, f"{Emoji_Map[BORDER]} {message} {Emoji_Map[BORDER]}")


#^ LOGGING CLASS BLOCK 



#? TESTING BLOCK
#logger = ColorLog(__name__, level=BORDER)
#
#logger.debug("This is a debug message.")
#logger.info("This is an info message.")
#logger.success("This is a success message.")
#logger.warning("This is a warning message.")
#logger.error("This is an error message.")
#logger.critical("This is a critical message.")
#logger.watchdog("This is a watchdog message.")
#
#logger.border("This is a border message.")
#^ TESTING BLOCK
