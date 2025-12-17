


#* ======================================================== *#
#*                    FILE DESCRIPTION                   
'''



'''
 #* ======================================================== *#

from __future__ import annotations
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
     
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from system.utils.data_models import (BaseID, ConnDir, ConnType, EQCategory, Enclosure, GenDescr, CTRLType, LEDProd, Voltage,
                                      LEDProtocol, Shape, FinishColor, Diffusion,
                                      BendDir, Equipment, WireSize)
# FOR np.ndarray (Vectors)
import numpy as np
 
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



 
#? ======================================================== ?#
#?                  ABSTRACT PROJECT DATA                   ?#
#? ======================================================== ?#
#! TODO : MOVE TO DESIGN MODELS.PY
#& PROJECT
@dataclass(slots=True, kw_only=True)
class Project(BaseID):
    address : str
    job_id : str
    anchors : List[Anchor] = field(default_factory=list)


#& ANCHOR
@dataclass(slots=True, kw_only=True)
class Anchor(BaseID):
    rooms : List[Room] = field(default_factory=list)


#& ROOM
@dataclass(slots=True, kw_only=True)
class Room(BaseID):
    enclosures : List[Enclosure] = field(default_factory=list)
    installs : List[Install] = field(default_factory=list)

#& INSTALL
@dataclass(slots=True, kw_only=True)
class Install(BaseID):
    rated_watts : int
    actual_watts : int 
    branches : List[LEDBranch] = field(default_factory=list)


#? ======================================================= ?#
#?                     FIXTURE ABSTRACTS                   ?#
#? ======================================================= ?#

#& TERMINAL
@dataclass(slots=True, kw_only=True)
class Terminal(BaseID): 
    conn_dir : ConnDir
    conn_type : ConnType


#& CABLE
@dataclass(slots=True, kw_only=True)
class Cable(BaseID):
    terminals : List[Terminal] = field(default_factory=list)
    gauge : WireSize


#& 3D PATH
@dataclass (slots=True, kw_only=True)
class Path3D(BaseID):
    geometry : List[np.ndarray] = field(default_factory=list)



#& LED BRANCH (HOLDS MULTIPLE SEGMENTS) (HELD BY CONTROLLERS)
@dataclass(slots=True, kw_only=True)
class LEDBranch(BaseID):
    segments : List[Fixture] = field(default_factory=list)
    total_length_mm : float = 0.0
    total_watts : float = 0.0
    total_pix : int = 0
    


