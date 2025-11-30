
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

from system.gen import gvars
import cursor
import time
import threading
import pystray
from pynput import keyboard
from PIL import Image, ImageDraw

DEFAULT_ICON = 'DEEREATCHAIN/assets/icons/icon_tray_raven.png'

DEFAULT_KBOARD_NAME = '-KBOARD-'

import ctypes

from system.utils.util_classes import ColorLog
log = ColorLog('JOHN_KEYB')

#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
class JohnKeyboard:
    def __init__(self) -> None:
        self.name = 'JOHN_KEYB'
        self.icon_img = Image.open(DEFAULT_ICON).resize((64,64))
        self.icon = pystray.Icon('DEC', self.icon_img,
                                 '[DEER-EAT-CHAIN UTILS]',
                                 menu=self.build_tray_menu())
        
        # cursor hide system
        self.auto_cur_hide_en = False
        self.cursor_hidden = False        # <-- FIXED
        self.last_activity = time.time()

        # keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # background thread
        self.auto_cur_hide = threading.Thread(target=self.ach_monitor, daemon=True)
        self.auto_cur_hide.start()        # <-- FIXED

    # CONTEXT MANAGER
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cursor.show()
        return False

    # TRAY MENU
    def build_tray_menu(self):
        return pystray.Menu(
            pystray.MenuItem(
                'DEC-Scripts',
                pystray.Menu(
                    pystray.MenuItem(
                        'AutoCursorHide',
                        pystray.Menu(
                            pystray.MenuItem('ON', self.enable_ach),
                            pystray.MenuItem('OFF', self.disable_ach)
                        )
                    ),
                    pystray.MenuItem('QUIT', self.quit),
                ),
            ),
        )

    # KEYBOARD ACTIVITY
    def on_key_press(self, key):
        self.last_activity = time.time()
        if self.auto_cur_hide_en:
            if not self.cursor_hidden:
                cursor.hide()
                print("CURSOR HIDDEN")
                self.cursor_hidden = True

    # TRAY: START & QUIT
    def start(self):
        self.icon.run()

    def quit(self, icon, item):
        cursor.show()
        self.icon.stop()

    # ENABLE/DISABLE AUTO CURSOR HIDE
    def enable_ach(self):
        while ctypes.windll.user32.ShowCursor(False) >= 0:
            pass

    def disable_ach(self):
        while ctypes.windll.user32.ShowCursor(False) >= 0:
            pass

    # BACKGROUND INACTIVITY MONITOR
    def ach_monitor(self):
        while True:
            if self.auto_cur_hide_en:
                # if hidden and 3 seconds passed -> show cursor
                if self.cursor_hidden and (time.time() - self.last_activity > 3):
                    cursor.show()
                    print("CURSOR SHOWN")
                    self.cursor_hidden = False
            time.sleep(0.1)



def test_auto_cur_hide():
    with JohnKeyboard() as jk:
        jk.enable_ach()
        print("Auto-hide enabled")
        jk.start()

test_auto_cur_hide()