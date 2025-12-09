


#* ======================================================== *#
#*                    FILE DESCRIPTION                   
'''



'''
 #* ======================================================== *#


import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
     
from dataclasses import dataclass
from enum import Enum
from typing import List
from system.utils.data_models import (BaseID, EQCategory, GenDescr, CTRLType, Voltage,
                                      LEDProtocol, Shape, FinishColor, Diffusion,
                                      BendDir, Equipment)

 
@dataclass(kw_only=True)
class Fixture(BaseID):
    prod_uuid    : str
    name         : str
    manuf        : str
    partnum      : str
    vin          : Voltage
    length_mm    : float
    width_mm     : float
    height_mm    : float
    # TODO: LINKABLE UP-TO LENGTH
    watts        : float
    colors       : str # TODO: CHANGE TO LIST
    m_roll       : float
    cutlen_mm    : float
    pixpitch_mm  : float
    shape        : Shape
    diffusion    : Diffusion
    view_angle   : float
    bend_dir     : BendDir
    protocol     : LEDProtocol
    wire_code    : str
    finish_color : FinishColor
    lumens_m     : float


@dataclass(kw_only=True)
class Controller(BaseID):
    prod_uuid    : str
    name         : str
    manuf        : str
    partnum      : str
    ctrl_type    : CTRLType
    max_channels : int
    w_per_ch     : float
    voltage      : Voltage
    protocol     : LEDProtocol
    iprating     : str
    
@dataclass(kw_only=True)
class PowerSupply(BaseID):
    prod_uuid    : str
    name         : str
    manuf        : str
    partnum      : str
    voltage_out  : Voltage
    max_watts    : float
    iprating     : str
    
