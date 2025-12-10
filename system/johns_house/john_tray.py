
#* ======================================================== *#
'''                    FILE DESCRIPTION                   






'''
# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#


#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from system.gen import settings
import time
import threading
import pystray
from PIL import Image, ImageDraw


DEFAULT_ICON = Path(ROOT)/'assets/icons/icon_tray_raven.png'

DEFAULT_KBOARD_NAME = '-KBOARD-'

import ctypes

from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_KEYB')

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
class JohnTray:
    def __init__(self) -> None:
        self.name = 'JOHN_KEYB'
        self.icon_img = Image.open(DEFAULT_ICON).resize((64,64))
        
        #* MENU TREE
        self.tree = [
            'APPS', ([
                ('SYSTEM DESIGNER', lambda: log.success('SYS_D')),  
                ('SCRAPE URL', lambda: log.success('SCRAPE')),  
            ]),
            'MACROS', ([
                ('MACRO 1', lambda: log.success('m1')),
                ('MACRO 2', lambda: log.success('m2')),
            ]),
            'SCRIPTS', ([
                ('AUTO IP CHANGE', lambda: log.success('ip_chg')),
                ('EMPTY', lambda: log.success('MT')),
                
            ]),
            'LAUNCHERS', ([
                ('CTRL PANEL', lambda: log.success('ctrlp')),
                ('NETW-ADAPTS', lambda: log.success('new_adpt')),
                
            ]),
            'SETTINGS', ([
                ('NEW APP', lambda: log.success('add_L')),
                ('NEW MACRO', lambda: log.success('add_L')),
                ('NEW LAUNCHER', lambda: log.success('add_L')),
                ('NEW SCRIPTS', lambda: log.success('add_L')),
            ]),
        ]
        
        self.icon = pystray.Icon('DEC', self.icon_img,
                                '[DEER-EAT-CHAIN UTILS]',
                                menu=self.setup_menus())
    

        
    # CONTEXT MANAGER
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.icon.stop()
        return False


    
    # BUILDS TRAY ICON MENU TREE
    def setup_menus(self,):
        
        def mk_menu_items(menu_data):
            menu_items = []
            for label, content in menu_items:
                if isinstance(content, list):
                    submenu = (*mk_menu_items(content))
                    menu_items.append(pystray.Menu(label, submenu))
                else:
                    action = lambda icon, itm, callback=content: callback()
                    new_menu.append(pystray.MenuItem(label,action))
            new_menu.append(pystray.MenuItem('EXIT', self.quit))
            return new_menu
    
    
    
    # START & QUIT - TRAY ICON SYSTEM
    def start(self):
        self.icon.run()
    
    def quit(self, icon, item):
        self.icon.stop()



#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#

#! ONLY RUNNABLE BY CMD
#! py "C:\Users\ransd\DEER_EAT_CHAIN\DEC\DEEREATCHAIN\system\johns_house\john_tray.py"
def test():
    with JohnTray() as tray:
        tray.start()
        
test()