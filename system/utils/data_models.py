
from __future__ import annotations
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# GLOBAL VARIABLES IMPORT
from system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog


from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List





#~ ======================================================== ~#
#~                  DATA OBJ. FUNCTIONS                     ~#
#~ ======================================================== ~#
#* CONVERTS LENGTH/UNITS BETWEEN STANDARDS
def convert_len(val:float, unit_in:str, unit_out:str) -> float:
    adapter = {'mm':0.001,
               'cm':0.01,
               'm':1.0,
               'in':0.0254,
               'ft':0.3048,
               }
    return val * (adapter[unit_in]/adapter[unit_out])


#^ ======================================================== ^#
#^                    DATACLASS ENUMS                       ^#
#^ ======================================================== ^#
from enum import Enum, auto
class EQCategory(Enum):
    UNKWN = 'UNKWN'
    GENERIC = 'GENERIC'
    CTRLR = 'CONTROLLER'
    LEDTAPE = 'LEDTape'
    PSU = 'PSU'
    FIXT = 'FIXTURE'
    NETSW = 'NETSWITCH'
    EQUIP = 'EQUIPMENT'

class GenDescr(Enum):
    UNKWN = 'UNKWN'
    YES = 'YES'
    NO = 'NO'

class CTRLType(Enum):
    UNKWN = auto()
    PIXEL = auto()
    PWM = auto()
    DMX = auto()
    Z_T = auto()

class Voltage(Enum):
    UNKWN = 0
    V05 = 5
    V12 = 12
    V24 = 24
    VPOE = 52
    V120 = 120

class LEDProtocol(Enum):
    UNKWN = auto()
    DMX512 = auto()
    WS2811 = auto()
    WS2812 = auto()
    WS2812B = auto()
    WS2813 = auto()
    WS2814 = auto()
    WS2815 = auto()
    UCS1903 = auto()
    UCS2903 = auto()
    UCS2904 = auto()
    GS8208B = auto()
    UCS8903 = auto()
    UCS8904 = auto()
    SK6812 = auto()

class Fuse(Enum):
    UNKWN = auto()
    AMP1 = 1
    AMP1_5 = 1.5
    AMP2 = 2
    AMP2_5 = 2.5
    AMP3 = 3
    AMP3_5 = 3.5
    AMP4 = 4
    AMP4_5 = 4.5
    AMP5 = 5
    AMP5_5 = 5.5
    AMP6 = 6
    AMP6_5 = 6.5
    AMP7 = 7
    AMP7_5 = 7.5
    AMP8 = 8
    AMP8_5 = 8.5
    AMP9 = 9
    AMP9_5 = 9.5
    AMP10 = 10
    AMP10_5 = 10.5

class Shape(Enum):
    UNKWN = auto()
    STANDARD = auto()
    WIDE_TOP = auto()
    DOMED = auto()
    SQUARE = auto()
    FLEX360 = auto()

class Diffusion(Enum):
    UNKWN = auto()
    NONE = auto()
    FROSTED = auto()
    MILK = auto()
    BLACK = auto()
    HEAVY = auto()
    LIGHT = auto()
    SHAPING = auto()

class BendDir(Enum):
    UNKWN = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    ANY = auto()

class EQProto(Enum):
    UNKWN = auto()
    NETWORK = auto()
    SACN = auto()
    DMX = auto()
    SPI = auto()
    I2C = auto()
    UART = auto()
    UDP = auto()
    TCPIP = auto()

class IPRating(Enum):
    UNKWN = auto()
    INDOOR = auto()
    OUTDOOR = auto()
    IP20 = auto()
    IP44 = auto()
    IP65 = auto()
    IP66 = auto()
    IP67 = auto()
    IP68 = auto()

class FinishColor(Enum):
    UNKWN = auto()
    BLACK = auto()
    WHITE = auto()
    BEIGE = auto()
    CLEAR = auto()
    CUSTOM = auto()

class ConnDir(Enum):
    UNKWN = auto()
    INPUT = auto()
    OUTPUT = auto()
    BI_DIR =  auto()

class ConnType(Enum):
    UNKWN = auto()
    BARE_LEAD = auto()
    EDISON = auto()
    DMX5P =  auto()
    DMX4P = auto()
    DMX3P = auto()
    RJ45 = auto()
    SCREWT = auto()
    IDC = auto()

class WireSize(Enum):
    UNKWN = auto()
    AWG12 = auto()
    AWG14 = auto()
    AWG16 = auto()
    AWG18 = auto()
    AWG20 = auto()
    AWG22 = auto()
    AWG24 = auto()
    AWG26 = auto()

class CableType(Enum):
    UNKWN = auto()
    CATNET = auto()
    HV120 = auto()
    LV48 = auto()



#? ======================================================== ?#
#?                    ROOT ID DATACLASS                     ?#
#? ======================================================== ?#
#& BASE IDENTITY FOR ALL DATACLASSES
@dataclass(slots=True, kw_only=True)
class BaseID:
    name: str
    description: str
    id_base: UUID = field(default_factory=uuid4)
    comments: List[str] = field(default_factory=list)


#? ======================================================== ?#
#?                  EQUIPMENT SCRAPE OBJS                   ?#
#? ======================================================== ?#
#& EQUIPMENT
@dataclass(slots=True, kw_only=True)
class Equipment(BaseID):
    manuf : str
    model : str
    partnum : str
    vin : int
    vout : int
    fuse : Fuse
    l_mm : int
    w_mm : int
    h_mm : int
    rated_watts : int
    actual_watts : int
    url : str
    datasheet : str
    ul_list : GenDescr
    ul_recog : GenDescr
    cert_url : str
    iprating : IPRating
    finish : FinishColor
    price : float
    eqproto : EQProto
    eq_category : EQCategory
    related_pns : List[str] = field(default_factory=list)
    terminals : List[Terminal] = field(default_factory=list)


#& ENCLOSURE
@dataclass(slots=True, kw_only=True)
class Enclosure(Equipment):
    ckts : List[BaseID] = field(default_factory=list)
    nets : List[BaseID] = field(default_factory=list)
    equipment : List[Equipment] = field(default_factory=list)


#& CTRLR
@dataclass(slots=True, kw_only=True)
class Ctrlr(Equipment):
    ip: str
    subn_mask : str
    ctrl_type : CTRLType
    outputs : List[Terminal] = field(default_factory=list)


#& LED_Prod
@dataclass(slots=True, kw_only=True)
class LEDProd(Equipment):
    colors : str
    watt_m : float
    watt_ft : float
    m_roll : float
    cutLen_mm : float
    cutLen_in : float
    pixPitch_m : int
    shape : Shape
    diffusion : Diffusion
    viewAngle : int
    bendDir : BendDir
    cri : int
    cct : int
    wireCode : str
    lumens_m : str
    lumens_ft : str
    max_length_m : float

    
#& POWER SUPPLY
@dataclass(slots=True,kw_only=True)
class PSU(Equipment):
    amps_port : float
    p_class : str
    efficiency : str
    dimming : str
    current_share : bool
    
#& ACCESSORY
@dataclass(slots=True, kw_only=True)
class Accessory(Equipment):
    acc_type : str
    spec_url : str

#& TERMINAL
@dataclass(slots=True, kw_only=True)
class Terminal(BaseID): 
    conn_dir : ConnDir
    conn_type : ConnType
    
    
#& RELATED EQUIPMENT
@dataclass(slots=True, kw_only=True)
class SubPN(BaseID):
    type_desc : str