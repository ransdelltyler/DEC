
#* ======================================================== *#
#*                    FILE DESCRIPTION                   
#*
#*
#*
#*
#* ======================================================== *#



# TODO:==================================================== ~#
# TODO:              TODO LIST / DEVLOG                     ~#
# TODO:==================================================== ~#


from __future__ import annotations
from uuid import uuid4

import numpy as np

from util_classes import ColorLog
from typing import Literal

from data_models import (
    BaseID,
    Project,
    Anchor,
    Room,
    Install,
    Equipment,
    Enclosure,
    Ctrlr,
    LEDFixt,
    Terminal,
    Cable,
    Path3D,
    LEDBranch,
    LEDSeg,
)


#! ======================================================== !#
#!                   DEFAULTS / VARIABLES                   !#
#! ======================================================== !#

log = ColorLog('Factory',level=1)

DEF_STR = {
    #^ BASE ID
    'name'      : '!NAME!',
    
    #^ EQUIPMENT
    'manuf'     : '!MANUFACTURER!',

    #^ CONTROLLER
    'ip'        : '!0.0.0.0!',
    'subnet'    : '!255.0.0.0!',
    
    #^LED FIXTURE
    'model'     : '!MODEL!',
    'colors'    : '!LED-COLORS!',
    'pnum'      : '!PART-NUM!',
    'subpns'    : '!SUB-PNS!',
    'shape'     : '!SHAPE!',
    'diffu'     : '!DIFFUSSION!',
    'bendd'     : '!BEND-DIR!',
    'proto'     : '!PROTOCOL!',
    'wirec'     : '!WIRE-COLORS!',
    'dsheet'    : '!DATASHEET!',
    'url'       : '!URLS!',
    'certurls'  : '!CERT-URL!',
    'iprating'  : '!IP-RATING!',
    'finishc'   : '!FINISH-COLOR!',

    #^ JOB FACTORY
    'jobid'     : '!JOB-ID!',
    'jobaddr'   : '!JOB-ADDRESS',
    
    #^ ANCHOR FACTORY
    'anchor'    : '!ANCHOR!'
}



#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#
def q_positive(value):
    if value is None:
        return None
    if not isinstance(value, (int, float)):
        raise TypeError("Expected a number")
    if value < 0:
        raise ValueError("Must be >= 0")
    return value





#~ ======================================================== ~#
#~                    FACTORY DEFINITIONS                   ~#
#~ ======================================================== ~#

# - ALL OUTPUT OBJECTS HAVE:
# -    BASEID['ID'] SET TO GENERATED UUID AT CREATION
# -    BASEID['NAME'] SETTABLE BUT NOT REQUIRED


#& PROJECT FACTORY
def new_project(*,
                name : str | None=None,
                job_id : str | None=None,
                address : str | None=None,
                comments : list[str] | None=None,
                anchors : list[Anchor] | None=None,
                ) -> Project:
    
    return Project(
                   #? BASE IDENTITY
                   id=uuid4(),
                   name=name or DEF_STR['name'],
                   comments=comments or [],
                   
                   #? PROJECT PARAMS
                   job_id=job_id or '!JOB-ID!',
                   address=address or '!JOB-ADDRESS!',
                   anchors=anchors or [],
                   )


#& ANCHOR FACTORY
def new_anchor(*,
               name : str | None=None,
               anchor_name:str | None=None,
               rooms : list[Room] | None=None,
               ):
    return Anchor(
                  #? BASE ID PARAMS
                  id=uuid4(),
                  name=name or DEF_STR['name'],
                  
                  #? ANCHOR PARAMS
                  anchor_name=anchor_name or '!ANCH-NAME!',
                  rooms = rooms or [],
                  
                  )


#& ROOM FACTORY
def new_room(*,
             #? BASE ID PARAMS
             name : str | None=None,

             #? ROOM PARAMS
             enclosures : list[Enclosure] | None=None,
             installs : list[Install] | None=None
    
             ):
    return Room(
                #? BASE ID PARAMS
                id=uuid4(),
                name=name or DEF_STR['name'],

                #? ROOM PARAMS
                enclosures=enclosures or [],
                installs=installs or []
                )


#& INSTALL FACTORY
def new_install(*,
                #? BASE ID PARAMS
                name : str | None=None,

                #? INSTALL PARAMS
                actual_watts : int | None=None,
                rated_watts : int | None=None,
                branches : list[LEDSeg] | None=None,

                ):
    return Install(
                #? BASE ID PARAMS
                id=uuid4(),
                name=name or DEF_STR['name'],
                
                #? INSTALL PARAMS
                actual_watts= int(q_positive(actual_watts) or 0),
                rated_watts= int(q_positive(rated_watts) or 0),
                branches=branches or [],
                )


#& EQUIPMENT FACTORY
def new_equipment(*,
                  name : str | None=None,
                  manuf : str | None=None,
                  vin : int |  None=None,
                  vout : int | None=None,
                  fuse : int | None=None,
                  l_mm : int | None=None,
                  w_mm : int | None=None,
                  h_mm : int | None=None,
                  rated_watts : int | None=None,
                  actual_watts : int | None=None,
                  terminals : list[Terminal] | None=None,
                  ):
    return Equipment(
                    #? BASE ID PARAMS
                    id=uuid4(),
                    name=name or DEF_STR['name'],
                    
                    #? EQUIPMENT PARAMS
                    manuf=manuf or '!MANUF!',
                    #& POSITIVE CHECK PARAMS
                    vin=vin or 0,
                    vout=vout or 0,
                    fuse=fuse or 0,
                    l_mm= int(q_positive(l_mm) or 0),
                    w_mm=int(q_positive(w_mm) or 0),
                    h_mm=int(q_positive(h_mm) or 0),
                    rated_watts=int(q_positive(rated_watts) or 0),
                    actual_watts=int(q_positive(actual_watts) or 0),
                    terminals=terminals or [],
                    )


#& ENCLOSURE FACTORY
def new_enclosure(*,
                  #? BASE ID PARAMS
                  name : str | None=None,
                  
                  #? BASE EQUIPMENT PARAMS
                  manuf : str | None=None,
                  vin : int |  None=None,
                  vout : int | None=None,
                  fuse : int | None=None,
                  l_mm : int | None=None,
                  w_mm : int | None=None,
                  h_mm : int | None=None,
                  rated_watts : int | None=None,
                  actual_watts : int | None=None,
                  terminals : list[Terminal] | None=None,

                  #? ENCLOSURE PARAMS
                  ckts : list[BaseID] | None=None,
                  nets : list[BaseID] | None=None,
                  equipment : list[Equipment] | None=None,

                  
                ):
    return Enclosure(
                    #? BASE ID PARAMS
                    id=uuid4(),
                    name=name or DEF_STR['name'],
                    
                    #? BASE EQUIPMENT PARAMS
                    manuf=manuf or '!MANU!',
                    vin=vin or 0,
                    vout=vout or 0,
                    fuse=fuse or 0,
                    l_mm= int(q_positive(l_mm) or 0),
                    w_mm=int(q_positive(w_mm) or 0),
                    h_mm=int(q_positive(h_mm) or 0),
                    rated_watts=int(q_positive(rated_watts) or 0),
                    actual_watts=int(q_positive(actual_watts) or 0),
                    terminals=terminals or [],

                    #? ENCLOSURE PARAMS
                    ckts=ckts or [],
                    nets=nets or [],
                    equipment=equipment or [],

                    
                    )


#& CONTROLLER FACTORY
def new_ctrlr(*,
              #? BASE ID PARAMS
              name : str | None=None,
              
              #? BASE EQUIPMENT PARAMS
              manuf : str | None=None,
              vin : int |  None=None,
              vout : int | None=None,
              fuse : int | None=None,
              l_mm : int | None=None,
              w_mm : int | None=None,
              h_mm : int | None=None,
              rated_watts : int | None=None,
              actual_watts : int | None=None,
              terminals : list[Terminal] | None=None,
             
              #? CONTROLLER PARAMS
              ip : str | None=None,
              subn_mask : str | None=None,
              eq_type : Literal['Pixel', 'PWM', 'DMX', '0-10v','!X!'] | None=None,
              outputs : list[Terminal] | None=None,

             ):
    return Ctrlr(
                 #? BASE ID PARAMS
                 id=uuid4(),
                 name=name or DEF_STR['name'],
                 
                 #? BASE EQUIPMENT PARAMS
                 manuf=manuf or '!MANU!',
                 vin=vin or 0,
                 vout=vout or 0,
                 fuse=fuse or 0,
                 l_mm= int(q_positive(l_mm) or 0),
                 w_mm=int(q_positive(w_mm) or 0),
                 h_mm=int(q_positive(h_mm) or 0),
                 rated_watts=int(q_positive(rated_watts) or 0),
                 actual_watts=int(q_positive(actual_watts) or 0),
                 terminals=terminals or [],
                 
                 #? CONTROLLER PARAMS
                 ip=ip or '0.0.0.0',
                 subn_mask=subn_mask or '255.255.0.0',
                 outputs=outputs or [],
                 eq_type=eq_type or '!X!',
                )


#& LED FIXTURE FACTORY
def new_ledprod(*,
                #? BASE ID PARAMS
                name : str | None=None,
                
                #? BASE EQUIPMENT PARAMS
                manuf : str | None=None,
                vin   : int | None=None,
                vout  : int | None=None,
                fuse  : int | None=None,
                l_mm  : int | None=None,
                w_mm  : int | None=None,
                h_mm  : int | None=None,
                rated_watts : int | None=None,
                actual_watts : int | None=None,
                terminals : list[Terminal] | None=None,
                
                #? LED PRODUCT PARAMS
                model : str | None=None,
                colors : str | None=None,
                partnum : str | None=None,
                watt_m : float | None=None,
                watt_ft : float | None=None,
                m_roll : float | None=None,
                led_m : float | None=None,
                price : float | None=None,
                cutLen_mm : float | None=None,
                cutLen_in : float | None=None,
                pixPitch_m : int | None=None,
                tapeWidth_mm : int | None=None,
                sub_pns : list[str] | None=None,
                shape : str | None=None,
                diffusion : str | None=None,
                viewAngle : int | None=None,
                bendDir : str | None=None,
                cri : int | None=None,
                cct : int | None=None,
                fixt_l_mm : float | None=None,
                fixt_w_mm : float | None=None,
                fixt_h_mm : float | None=None,
                protocol : str | None=None,
                wireCode : str | None=None,
                url : str | None=None,
                datasheet : str | None=None,
                ul_list : bool | None=None,
                ul_recog : bool | None=None,
                cert_url : str | None=None,
                ipRating : str | None=None,
                finish : str | None=None,
                lumens_m : list[float] | None=None,
                lumens_ft : list[float] | None=None,
  
                ):
    return LEDFixt(
                    #? BASE ID PARAMS
                    id=uuid4(),
                    name=name or DEF_STR['name'],
                    
                    #? BASE EQUIPMENT PARAMS
                    manuf=manuf or '!MANU!',
                    vin=vin or 0,
                    vout=vout or 0,
                    fuse=fuse or 0,
                    l_mm= int(q_positive(l_mm) or 0),
                    w_mm=int(q_positive(w_mm) or 0),
                    h_mm=int(q_positive(h_mm) or 0),
                    rated_watts=int(q_positive(rated_watts) or 0),
                    actual_watts=int(q_positive(actual_watts) or 0),
                    terminals=terminals or [],

                    #? LED FIXTURE PARAMS
                    model = model or '!MODEL!',
                    colors = colors or '!COLORS!',
                    partnum = partnum or '!PN!',
                    watt_m = watt_m or 0,
                    watt_ft = watt_ft or 0,
                    m_roll = m_roll or 0,
                    led_m = led_m or 0,
                    price = price or 0,
                    cutLen_mm = cutLen_mm or 0,
                    cutLen_in = cutLen_in or 0,
                    pixPitch_m =  pixPitch_m or 0,
                    tapeWidth_mm = tapeWidth_mm or 0,
                    sub_pns = sub_pns or [],
                    shape = shape or '!SHAPE!',
                    diffusion = diffusion or '!DIFFUSION!',
                    viewAngle = viewAngle or 0,
                    bendDir = bendDir or '!BEND DIR.!',
                    cri = cri or 0,
                    cct = cct or 0,
                    fixt_l_mm = fixt_l_mm or 0,
                    fixt_w_mm = fixt_w_mm or 0,
                    fixt_h_mm = fixt_h_mm or 0,
                    protocol = protocol or '!PROTO!',
                    wireCode = wireCode or '!WCODE!',
                    url = url or '!URL!',
                    datasheet = datasheet  or '!DSHT!',
                    ul_list = ul_list or False,
                    ul_recog = ul_recog or False,
                    cert_url = cert_url or '!CTURL!',
                    ipRating = ipRating or '!IP0!',
                    finish = finish or '!fin!',
                    lumens_m = lumens_m or [],
                    lumens_ft = lumens_ft or [],
                 
                 )


#& TERMINAL FACTORY
def new_terminal(*,
                #? BASE ID PARAMS
                name : str | None=None,

                #? TERMINAL PARAMS
                conn_dir : Literal['INPUT', 'OUTPUT', 'BI-DIR', '!X!'] | None=None,
                conn_type : Literal['BARE-LEAD','EDISON','5PIN','4PIN','3PIN','RJ45','SCREW-TERM','IDC','!X!'] | None=None,
                
                ):
    return  Terminal(
                    #? BASE ID PARAMS
                    id=uuid4(),
                    name=name or DEF_STR['name'],

                    #? TERMINAL PARAMS
                    conn_dir=conn_dir or '!X!',
                    conn_type=conn_type or '!X!',
                    )


#& CABLE FACTORY
def new_cable(*,
            #? BASE ID PARAMS
            name : str | None=None,  
              
            #? CABLE PARAMS
            terminals : list['Terminal'] | None=None,
            gauge : Literal['12G', '14G', '16G', '18G', '20G', '22G', '24G', '!X!'] | None=None,
            
            ):
    return Cable(
                #? BASE ID PARAMS
                id=uuid4(),
                name=name or DEF_STR['name'],
                
                #? CABLE PARAMS
                terminals=terminals or [],
                gauge=gauge or '!X!'

                )


#& 3D PATH FACTORY
def new_path3d(*,
               #? BASE ID PARAMS
               name : str | None=None,
               
               #? PATH3D PARAMS
               geometry : list[np.ndarray] | None=None,
               ):
    return Path3D(
                #? BASE ID PARAMS
                id=uuid4(),
                name=name or DEF_STR['name'],

                #? PATH3D PARAMS
                geometry=geometry or [],

                )


#& LED BRANCH FACTORY
def new_ledbranch(*,
                  #? BASE ID PARAMS
                  name : str | None=None,
                  
                  #? LED BRANCH PARAMS
                  segments : list['LEDSeg'] | None=None,
                  
                  ):
    return LEDBranch(
                    #? BASE ID PARAMS
                    id=uuid4(),
                    name=name or DEF_STR['name'],
                    
                    #? LED BRANCH PARAMS
                    segments=segments or [],
                     
                    )


#& LED SEGMENT FACTORY
def new_ledsegment(*,
                   #? BASE ID PARAMS
                   name :str | None=None,

                   #? LED SEGMENT PARAMS
                   led_prod : LEDFixt, #!REQUIRED
                   len_m    : float    | None=None,
                   ):
    return LEDSeg(
                  #? BASE ID PARAMS
                  id=uuid4(),
                  name=name or DEF_STR['name'],

                  #? LED SEGMENT PARAMS
                  led_prod=led_prod, #!REQUIRED
                  len_m=len_m or 0.0,
                  )



#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#




#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#