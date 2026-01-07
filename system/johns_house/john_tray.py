
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
TREE = [str(p) for p in Path(__file__).resolve().parents]
ROOT = 'DEEREATCHAIN'  #? ROOT FOLDER TO LOOK FOR
for path in TREE:
    if Path(path).name == ROOT:
        if path not in sys.path:
            print(f'ADDING {ROOT} TO SYSTEM PATHS')
            sys.path.insert(0, path)

from system.gen import settings
import time
import threading
import pystray
from PIL import Image, ImageDraw

# IP CHANGER IMPORTS
import subprocess
import psutil
import socket
import ipaddress
from scapy.layers.l2 import ARP, Ether
from scapy.all import srp
import random

DEF_ICON = 'PUDU1k.png'
DEF_NIC_NAME = 'Ethernet'

import ctypes

from system.utils.util_classes import ColorLog
from system.gen.settings import LOG_MSG
log = ColorLog('JOHN_TRAY')

from enum import Enum
class SUBMASK_LVL(Enum):
    SM8  = 8
    SM16 = 16
    SM24 = 24
    SM30 = 30
    SM32 = 32

DEF_SUBNET_MASK = SUBMASK_LVL.SM16.value


#~ ======================================================== ~#
#~                    CLASS DEFINITION                      ~#
#~ ======================================================== ~#
class JohnTray:
    def __init__(self) -> None:
        self.name = 'JOHN_TRAY'
        self.icon_img = Image.open(DEF_ICON).resize((64,64))
        
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
        
        #* NETWORK VARIABLES
        self.lighting_nic = DEF_NIC_NAME
        self.system_nics = psutil.net_if_addrs()
        
        #* RUNNING IP CONFIGS
        #? LIST OF TUPLES (INTERFACE NAME, IP, SUBNET-MASK)
        self.active_configs = self.get_ip_config()
        #* IP SETTING CONFIGURATIONS
        #? DICT OF CONFIG_NAME : TUPLE (INTERFACE NAME, IP, SUBNET-MASK)
        self.saved_configs = {}
        #* BASIC LIGHTING CONFIGS FOR RANDOM ADDRESS ASSIGNMENT
        #? DICT OF CONFIG_NAME : TUPLE (IP, SUBNET-MASK)
        self.basic_configs = {
            'ETC' : (
                '10.101.10.1',
                '255.255.0.0'
            ),
            'PATHWAY' : (
                '100.0.0.0',
                '255.255.0.0'
            ),
            'CUESERVER' : (
                '1.1.1.1',
                '255.0.0.0'
            )
        }
        
        #* SUBNET MASK LEVEL FOR IP GEN
        self.subnet_mask = DEF_SUBNET_MASK
        # TODO: IP PING WATCHDOG
        
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
            for label, content in menu_data:
                if isinstance(content, list):
                    submenu = (mk_menu_items(content))
                    menu_items.append(pystray.Menu(label, submenu))
                else:
                    action = lambda icon, itm, callback=content: callback()
                    menu_items.append(pystray.MenuItem(label,action))
            menu_items.append(pystray.MenuItem('EXIT', self.quit))
            return menu_items
    
    
    
    # START & QUIT - TRAY ICON SYSTEM
    def start(self):
        self.icon.run()
    
    def quit(self, icon, item):
        self.icon.stop()


#? ======================================================== ?#

    #* IP CHANGER SCRIPT
    def auto_ip_changer(self, config: tuple):
        # Set a Static IP
        subprocess.run(["nmcli", "con", "mod", config[0], "ipv4.addresses", config[1]])
        subprocess.run(["nmcli", "con", "mod", config[0], "ipv4.gateway", config[2]])
        subprocess.run(["nmcli", "con", "mod", config[0], "ipv4.method", "manual"]) 
        # Apply the changes (Restart the connection)
        subprocess.run(["nmcli", "con", "down", config[0]])
        subprocess.run(["nmcli", "con", "up", config[0]])
    
    #* UPDATE CURRENT(RUNNING) IP CONFIGS    
    def get_ip_config(self,) -> tuple | None:
        sys_nics = psutil.net_if_addrs()
        
        for nic, addrs in sys_nics.items():
            nic_name = nic
            nic_addr = ''
            nic_mask = ''
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    nic_addr = addr.address
                    nic_mask = addr.netmask
            
            return (nic_name, nic_addr, nic_mask)
        else:
            if LOG_MSG: log.critical(f'get_ip_config() - FOUND 0 NICS')
    
    
    #* START SAVED CONFIG
    def activate_saved_config(self, config_name: str):
        config = self.saved_configs[config_name]
        if config is None: 
            if LOG_MSG: # CATCH: INVALID PASSED CONFIG NAME
                log.warning(f'NO SAVED CONFIGS WITH NAME: {config_name}')
                log.debug(f'{self.saved_configs}')
        else: 
            # SET NIC VARIABLES
            subprocess.run(["nmcli", "con", "mod", self.lighting_nic, "ipv4.addresses", config[1]])
            subprocess.run(["nmcli", "con", "mod", self.lighting_nic, "ipv4.gateway", config[2]])
            subprocess.run(["nmcli", "con", "mod", self.lighting_nic, "ipv4.method", "manual"]) 
            # APPLY AND RESTART NIC
            subprocess.run(["nmcli", "con", "down", self.lighting_nic])
            subprocess.run(["nmcli", "con", "up", self.lighting_nic])
    
    
    #* START BASIC CONFIG
    def start_basic_config(self, config_name : str):
        if config_name not in self.basic_configs:
            if LOG_MSG: log.critical(f'start_basic_config() CANT FIND: {config_name}')
        else:
            config = self.basic_configs[config_name]
            # SET NIC VARIABLES
            subprocess.run(["nmcli", "con", "mod", self.lighting_nic, "ipv4.addresses", '1'])
            # APPLY AND RESTART NIC
            subprocess.run(["nmcli", "con", "down", self.lighting_nic])
            subprocess.run(["nmcli", "con", "up", self.lighting_nic])

    
    #* UPDATE LIGHTING NIC VARIABLE
    def set_lighting_nic(self, target_nic : str):
        for nic in self.system_nics:
            if nic[0] == target_nic:
                self.lighting_nic = target_nic
                
                
    #* GENERATE IP IN RANGE
    def gen_ip(self, ip, mask = DEF_SUBNET_MASK) -> str:
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict = False)
        # GET ALL HOSTS IN NETWORK RANGE
        all_hosts = list(network.hosts())
        # PICK RANDOM HOST
        rand_ip = str(random.choice(all_hosts))

        if LOG_MSG: log.debug(f'GENERATED IP:{rand_ip} IN RANGE:{network}')

        return rand_ip

        
    #* SCAN NETWORK FOR EXISTING IPs
    def scan_net(self, ip_range : str):
        arp = ARP(pdst=ip_range)
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')
        packet = ether/arp
        # TRY TO SEND A PACKET AND RETURN ALL RESPONDING(ACTIVE) IP ADDRESSES
        result = srp(packet, timeout=2, verbose=False)[0]
        return [recieved.psrc for sent, recieved in result]
    
    #* CHECK IF GIVEN IP IS ALREADY IN USE
    def find_open_ip(self, ip : str):
        found_ips = self.scan_net(ip)
        if ip in found_ips:
            if LOG_MSG: log.debug(f'IP:{ip} ALREADY IN USE GENERATING ALT')
            new_ip = self.gen_ip(ip)
            self.find_open_ip(new_ip)
        else: 
            return True
    
    #* CHECK IF IP IS: IN VALID RANGE, MASK (TARGET IS ACCESSABLE)
    def is_valid_ip(self, target_ip, current_ip, mask) -> bool:
        network = ipaddress.IPv4Network(f'{current_ip}/{mask}', strict = False)
        return ipaddress.IPv4Address(target_ip) in network
        
        
        
        
#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#

#! ONLY RUNNABLE BY CMD
#! py "C:\Users\ransd\DEER_EAT_CHAIN\DEC\DEEREATCHAIN\system\johns_house\john_tray.py"
def test():
    with JohnTray() as tray:
        tray.start()
        
test()