from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import List, Literal

# FOR np.ndarray (Vectors)
import numpy as np


#?=============================?#
#?      ROOT ID DATACLASS      ?#
#?=============================?#
#& BASE IDENTITY FOR ALL DATACLASSES
@dataclass(kw_only=True)
class BaseID:
    name: str
    id: UUID = field(default_factory=uuid4)
    comments: list[str] = field(default_factory=list)
#~ ________________________



#?=============================?#
#?    ABSTRACT PROJECT DATA    ?#
#?=============================?#
#& PROJECT
@dataclass(kw_only=True)
class Project(BaseID):
    address : str
    job_id : str
    anchors : list[Anchor] = field(default_factory=list)
#~ ________________________


#& ANCHOR
@dataclass(kw_only=True)
class Anchor(BaseID):
    shortn : str
    rooms : list[Room] = field(default_factory=list)
#~ ________________________


#& ROOM
@dataclass(kw_only=True)
class Room(BaseID):
    enclosures : list[Enclosure] = field(default_factory=list)
    installs : list[Install] = field(default_factory=list)
#~ ________________________


#& INSTALL
@dataclass(kw_only=True)
class Install(BaseID):
    rated_watts : int
    actual_watts : int
    branches : list[LED_Seg] = field(default_factory=list)
#~ ________________________


#?=============================?#
#?    EQUIPMENT AND DEVICES    ?#
#?=============================?#
#& EQUIPMENT
@dataclass(kw_only=True)
class Equipment(BaseID):
    manuf : str
    vin : int
    vout : int
    wattage : int
    fused : bool
    fuse_A : int
    len_mm : int
    wid_mm : int
    heig_mm : int
    rated_watts : int
    actual_watts : int
    terminals : list[Terminal] = field(default_factory=list)
#~ ________________________


#& ENCLOSURE
@dataclass(kw_only=True)
class Enclosure(Equipment):
    ckts : list[BaseID] = field(default_factory=list)
    nets : list[BaseID] = field(default_factory=list)
    equipment : list[Equipment] = field(default_factory=list)
#~ ________________________


#& CTRLR
@dataclass(kw_only=True)
class CTRLR(Equipment):
    ip: str
    subn_mask : str
    eq_type : Literal['Pixel', 'PWM', 'DMX', '0-10v','']
    outputs : list[Terminal] = field(default_factory=list)
#~ ________________________


#& LED_Prod
@dataclass(kw_only=True)
class LED_Fixt(Equipment):
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
    accessories : str
    shape : str
    diffusion : str
    viewAngle : int
    bendDir : str
    cri : int
    cct : int
    length : float
    width : float
    height : float
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
#~ ________________________


#& TERMINAL
@dataclass(kw_only=True)
class Terminal(BaseID): 
    conn_dir : Literal['INPUT', 'OUTPUT', 'BI-DIR']
    conn_type : Literal['Bare-Lead', 'Edison', '5pin', '4pin', '3pin', 'RJ45', 'Screw-Term','IDC']
#~ ________________________


#& CABLE
@dataclass(kw_only=True)
class Cable(BaseID):
    m_conn : Terminal
    f_conn : Terminal
    gauge : Literal['12g', '14g', '16g', '18g', '20g', '22g', '24g']
#~ ________________________



#?===============================?#
#?      DATA - DATA CLASSES      ?#
#?===============================?#
#& DMX PACKET
@dataclass(kw_only=True)
class DMX_Packet:
    name : str
    id: UUID = field(default_factory=uuid4)
    data : list[int] = field(default_factory=list)
    prio : list[int] = field(default_factory=list)
#~ ________________________

#& sACN PACKET
#~ ________________________


#& PATH
@dataclass (kw_only=True)
class Path:
    geometry : list[np.ndarray] = field(default_factory=list)
#~ ________________________



#?=============================?#
#?      FIXTURE ABSTRACTS      ?#
#?=============================?#
#& LED BRANCH (HOLDS MULTIPLE SEGMENTS) (HELD BY CONTROLLERS)
@dataclass(kw_only=True)
class LED_Branch:
    name : str
    id: UUID = field(default_factory=uuid4)
    segments : list[LED_Seg] = field(default_factory=list)
#~ ________________________

#& HOLDS LED SEGMENT DATA FOR BUILDING INSTALL
@dataclass(kw_only=True)
class LED_Seg:
    name : str
    led_prod : LED_Fixt
    len_m : float
    
    # --- DEFAULT FIELDS ---
    id: UUID = field(default_factory=uuid4)

    #* RETURN CALCULATED WATTAGE OF SEGMENT
    @property
    def cal_watts(self) -> float:
        return self.len_m * self.led_prod.watt_m
    
    @property # TODO: REPLACE PLACEHOLDER
    #* RETURN ALL CONVERTED LENGTHS [IN, FT, MM, M]
    def conv_len(self) -> list:
        return [1,2,3] 
#~ ________________________
