from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Literal

# FOR np.ndarray (Vectors)
import numpy as np

#~ ======================================================== ~#
#~                  DATA OBJ. FUNCTIONS                     ~#
#~ ======================================================== ~#
#* CONVERTS LENGTH/UNITS BETWEEN STANDARDS
def convert_len(val:float, unit_in:str, unit_out:str) -> float:
    adapter = {'mm':0.001, 'cm':0.01, 'm':1.0, 'km':1000.0, 'in':39.37, 'ft':3.28084, 'mi': 0.00062}
    return val * (adapter[unit_in]/adapter[unit_out])


#? ======================================================== ?#
#?                    ROOT ID DATACLASS                     ?#
#? ======================================================== ?#
#& BASE IDENTITY FOR ALL DATACLASSES
@dataclass(slots=True, kw_only=True)
class BaseID:
    name: str
    id: UUID = field(default_factory=uuid4)
    comments: list[str] = field(default_factory=list)


 
#? ======================================================== ?#
#?                  ABSTRACT PROJECT DATA                   ?#
#? ======================================================== ?#
#& PROJECT
@dataclass(slots=True, kw_only=True)
class Project(BaseID):
    address : str
    job_id : str
    anchors : list['Anchor'] = field(default_factory=list)


#& ANCHOR
@dataclass(slots=True, kw_only=True)
class Anchor(BaseID):
    anchor_name : str
    rooms : list['Room'] = field(default_factory=list)


#& ROOM
@dataclass(slots=True, kw_only=True)
class Room(BaseID):
    enclosures : list['Enclosure'] = field(default_factory=list)
    installs : list['Install'] = field(default_factory=list)
#~ ________________________


#& INSTALL
@dataclass(slots=True, kw_only=True)
class Install(BaseID):
    rated_watts : int
    actual_watts : int
    branches : list['LEDSeg'] = field(default_factory=list)



#? ======================================================== ?#
#?                  EQUIPMENT AND DEVICES                   ?#
#? ======================================================== ?#
#& EQUIPMENT
@dataclass(slots=True, kw_only=True)
class Equipment(BaseID):
    manuf : str
    vin : int
    vout : int
    fuse : int
    l_mm : int
    w_mm : int
    h_mm : int
    rated_watts : int
    actual_watts : int
    terminals : list[Terminal] = field(default_factory=list)


#& ENCLOSURE
@dataclass(slots=True, kw_only=True)
class Enclosure(Equipment):
    ckts : list['BaseID'] = field(default_factory=list)
    nets : list['BaseID'] = field(default_factory=list)
    equipment : list['Equipment'] = field(default_factory=list)


#& CTRLR
@dataclass(slots=True, kw_only=True)
class Ctrlr(Equipment):
    ip: str
    subn_mask : str
    eq_type : Literal['Pixel', 'PWM', 'DMX', '0-10v','!X!']
    outputs : list['Terminal'] = field(default_factory=list)


#& LED_Prod
@dataclass(slots=True, kw_only=True)
class LEDFixt(Equipment):
    model : str
    colors : str
    partnum : str
    watt_m : float
    watt_ft : float
    m_roll : float
    led_m : float
    price : float
    cutLen_mm : float
    cutLen_in : float
    pixPitch_m : int
    tapeWidth_mm : int
    sub_pns : list[str]
    shape : str
    diffusion : str
    viewAngle : int
    bendDir : str
    cri : int
    cct : int
    fixt_l_mm : float
    fixt_w_mm : float
    fixt_h_mm : float
    protocol : str
    wireCode : str
    url : str
    datasheet : str
    ul_list : bool
    ul_recog : bool
    cert_url : str
    ipRating : str
    finish : str
    lumens_m : list[float] = field(default_factory=list)
    lumens_ft : list[float] = field(default_factory=list)


#& TERMINAL
@dataclass(slots=True, kw_only=True)
class Terminal(BaseID): 
    conn_dir : Literal['INPUT', 'OUTPUT', 'BI-DIR', '!X!']
    conn_type : Literal['BARE-LEAD','EDISON','5PIN','4PIN','3PIN','RJ45','SCREW-TERM','IDC','!X!']


#& CABLE
@dataclass(slots=True, kw_only=True)
class Cable(BaseID):
    terminals : list['Terminal'] = field(default_factory=list)
    gauge : Literal['12G', '14G', '16G', '18G', '20G', '22G', '24G', '!X!']


#& 3D PATH
@dataclass (slots=True, kw_only=True)
class Path3D(BaseID):
    geometry : list[np.ndarray] = field(default_factory=list)



#? ======================================================= ?#
#?                     FIXTURE ABSTRACTS                   ?#
#? ======================================================= ?#
#& LED BRANCH (HOLDS MULTIPLE SEGMENTS) (HELD BY CONTROLLERS)
@dataclass(slots=True, kw_only=True)
class LEDBranch(BaseID):
    segments : list['LEDSeg'] = field(default_factory=list)

#& HOLDS LED SEGMENT DATA FOR BUILDING INSTALL
@dataclass(slots=True, kw_only=True)
class LEDSeg(BaseID):
    led_prod : 'LEDFixt'
    len_m : float
    
    #* RETURN CALCULATED WATTAGE OF SEGMENT
    @property
    def cal_watts(self) -> float:
        return self.len_m * self.led_prod.watt_m
    



#? ======================================================= ?#
#?                     DATA - DATA CLASSES                 ?#
#? ======================================================= ?#

#& DMX PACKET
@dataclass(slots=True, kw_only=True)
class DMX_Packet:
    name : str
    id: UUID = field(default_factory=uuid4)
    data : list[int] = field(default_factory=list)
    prio : list[int] = field(default_factory=list)

#& sACN PACKET
