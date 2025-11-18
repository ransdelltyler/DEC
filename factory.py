
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
    CTRLType,
    Voltage,
    LEDProtocol,
    Shape,
    Diffusion,
    BendDir,
    Protocol,
    IPRating,
    FinishColor,
    Fuse,
    ConnDir,
    ConnType,
    WireSize,
    CableType,
)

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
    'wcode'     : '!WIRE-CODE!',
    'dsheet'    : '!DATASHEET!',
    'url'       : '!URLS!',
    'certurls'  : '!CERT-URL!',
    'iprating'  : '!IP-RATING!',
    'finishc'   : '!FINISH-COLOR!',

    #^ JOB FACTORY
    'jobid'     : '!JOB-ID!',
    'jobaddr'   : '!JOB-ADDRESS!',
    
    #^ ANCHOR FACTORY
    'anchor'    : '!ANCHOR!'
}



#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#

def base_id(*, name, comments):
    return {
        'id' : uuid4(),
        'name' : name or DEF_STR['name'],
        'comments' : comments or [],
    }

def equipment_base(*, manuf, vin, vout, fuse, l_mm, w_mm, h_mm, rated_watts, actual_watts, terminals):
    return {
        'manuf' : manuf or DEF_STR['manuf'],
        'vin' : int(vin) if vin is not None else 0,
        'vout' : int(vout) if vout is not None else 0,
        'fuse' : float(fuse) if fuse is not None else 0,
        'l_mm' : l_mm or 0,
        'w_mm' : w_mm or 0,
        'h_mm' : h_mm or 0,
        'rated_watts' : rated_watts or 0,
        'actual_watts' : actual_watts or 0,
        'terminals' : terminals or 0,
        }


#? ======================================================== ?#
#?                   VALIDATION FUNCTIONS                   ?#
#? ======================================================== ?#
#* CATCHES NONE OR NON-POSITIVE VALUE
def valid_num(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if value >= 0:
            return value
    raise ValueError("Must be >= 0")

#* CATCHES STRINGS OR NONE PASSED TO ENUM PARAMETERS
def to_enum(value, enum_cls):
    if isinstance(value, enum_cls):
        return value
    
    if isinstance(value, str):
        try:
            return enum_cls[value.upper()]
        except KeyError:
            return enum_cls.UNKWN
    
    return enum_cls.UNKWN



#~ ======================================================== ~#
#~                    FACTORY DEFINITIONS                   ~#
#~ ======================================================== ~#

# - ALL OUTPUT OBJECTS HAVE:
# -    BASEID['ID'] SET TO GENERATED UUID AT CREATION
# -    BASEID['NAME'] SETTABLE BUT NOT REQUIRED


#& PROJECT FACTORY
def new_project(*,
                #? BASE ID PARAMS
                name : str | None=None,

                #? PROJECT PARAMS
                job_id : str | None=None,
                address : str | None=None,
                anchors : list[Anchor] | None=None,
                **kwargs,
                ) -> Project:
    
    return Project(
                   #? BASE ID PARAMS
                   **base_id(name=name,comments=kwargs.get('comments')),
                   
                   #? PROJECT PARAMS
                   job_id=job_id or DEF_STR['jobid'],
                   address=address or DEF_STR['jobaddr'],
                   anchors=anchors or [],
                   )


#& ANCHOR FACTORY
def new_anchor(*,
               #? BASE ID PARAMS
               name : str | None=None,
               
               #? ANCHOR PARAMS
               anchor_name:str | None=None,
               rooms : list[Room] | None=None,
               **kwargs,
               ) -> Anchor:
    
    return Anchor(
                  #? BASE ID PARAMS
                  **base_id(name=name,comments=kwargs.get('comments')),
                  
                  #? ANCHOR PARAMS
                  anchor_name=anchor_name or DEF_STR['anchor'],
                  rooms = rooms or [],
                  )


#& ROOM FACTORY
def new_room(*,
             #? BASE ID PARAMS
             name : str | None=None,

             #? ROOM PARAMS
             enclosures : list[Enclosure] | None=None,
             installs : list[Install] | None=None
             **kwargs,
             ) -> Room:
    
    return Room(
                #? BASE ID PARAMS
                **base_id(name=name,comments=kwargs.get('comments')),

                #? ROOM PARAMS
                enclosures=enclosures or [],
                installs=installs or []
                )


#& INSTALL FACTORY
def new_install(*,
                #? BASE ID PARAMS
                name : str | None=None,
                comments : list[str] | None=None,

                #? INSTALL PARAMS
                actual_watts : int | None=None,
                rated_watts : int | None=None,
                branches : list[LEDSeg] | None=None,
                **kwargs,
                ) -> Install:
    
    return Install(
                #? BASE ID PARAMS
                **base_id(name=name,comments=kwargs.get('comments')),
                
                #? INSTALL PARAMS
                actual_watts= int(valid_num(actual_watts) or 0),
                rated_watts= int(valid_num(rated_watts) or 0),
                branches=branches or [],
                )


#& EQUIPMENT FACTORY
def new_equipment(*,
                  comments : list[str] | None=None,
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
                  **kwargs,
                  ) -> Equipment:

    return Equipment(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=kwargs.get('comments')),
                    

                    **equipment_base(manuf = manuf or DEF_STR['manuf'],
                                     vin   = valid_num(vin) or Voltage.UNKWN,
                                     vout  = valid_num(vout) or Voltage.UNKWN,
                                     fuse  = valid_num(fuse) or Fuse.UNKWN,
                                     l_mm  = valid_num(l_mm) or 0,
                                     w_mm  = valid_num(w_mm) or 0,
                                     h_mm  = valid_num(h_mm) or 0,
                                     rated_watts  = valid_num(rated_watts) or 0,
                                     actual_watts = valid_num(actual_watts) or 0,
                                     terminals    = terminals or [],
                                     ),
                    )


#& ENCLOSURE FACTORY
def new_enclosure(*,
                  #? BASE ID PARAMS
                  name : str | None=None,

                  #? ENCLOSURE PARAMS
                  ckts : list[BaseID] | None=None,
                  nets : list[BaseID] | None=None,
                  equipment : list[Equipment] | None=None,
                  **kwargs,
                ) -> Enclosure:

    return Enclosure(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=kwargs.get('comments')),                    
                    **equipment_base(**kwargs),

                    #? ENCLOSURE PARAMS
                    ckts=ckts or [],
                    nets=nets or [],
                    equipment=equipment or [],

                    
                    )


#& CONTROLLER FACTORY
def new_ctrlr(*,
              #? BASE ID PARAMS
              name : str | None=None,
              comments : list[str] | None=None,
              
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
              ctrl_type : CTRLType | None=None,
              outputs : list[Terminal] | None=None,
              **kwargs,
             ) -> Ctrlr:

    return Ctrlr(
                 #? BASE ID PARAMS
                 **base_id(name=name,comments=kwargs.get('comments')),
                 
                 **equipment_base(manuf = manuf or DEF_STR['manuf'],
                                     vin   = valid_num(vin) or Voltage.UNKWN,
                                     vout  = valid_num(vout) or Voltage.UNKWN,
                                     fuse  = valid_num(fuse) or Fuse.UNKWN,
                                     l_mm  = valid_num(l_mm) or 0,
                                     w_mm  = valid_num(w_mm) or 0,
                                     h_mm  = valid_num(h_mm) or 0,
                                     rated_watts  = valid_num(rated_watts) or 0,
                                     actual_watts = valid_num(actual_watts) or 0,
                                     terminals    = terminals or [],
                                     ),
                 
                 #? CONTROLLER PARAMS
                 ip=ip or '0.0.0.0',
                 subn_mask=subn_mask or DEF_STR['subnet'],
                 outputs=outputs or [],
                 ctrl_type= to_enum(ctrl_type, CTRLType),
                )


#& LED FIXTURE FACTORY
def new_ledprod(*,
                #? BASE ID PARAMS
                name : str | None=None,
                comments : list[str] | None=None,
                
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
                shape : Shape | None=None,
                diffusion : Diffusion | None=None,
                viewAngle : int | None=None,
                bendDir : BendDir | None=None,
                cri : int | None=None,
                cct : int | None=None,
                fixt_l_mm : float | None=None,
                fixt_w_mm : float | None=None,
                fixt_h_mm : float | None=None,
                protocol : Protocol | None=None,
                wireCode : str | None=None,
                url : str | None=None,
                datasheet : str | None=None,
                ul_list : bool | None=None,
                ul_recog : bool | None=None,
                cert_url : str | None=None,
                ipRating : IPRating | None=None,
                finish : FinishColor | None=None,
                lumens_m : list[float] | None=None,
                lumens_ft : list[float] | None=None,
                **kwargs,
                ) -> LEDFixt:

    return LEDFixt(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=kwargs.get('comments')),
                    
                    **equipment_base(manuf = manuf or DEF_STR['manuf'],
                                     vin   = valid_num(vin) or Voltage.UNKWN,
                                     vout  = valid_num(vout) or Voltage.UNKWN,
                                     fuse  = valid_num(fuse) or Fuse.UNKWN,
                                     l_mm  = valid_num(l_mm) or 0,
                                     w_mm  = valid_num(w_mm) or 0,
                                     h_mm  = valid_num(h_mm) or 0,
                                     rated_watts  = valid_num(rated_watts) or 0,
                                     actual_watts = valid_num(actual_watts) or 0,
                                     terminals    = terminals or [],
                                     ),

                    #? LED FIXTURE PARAMS
                    model = model or DEF_STR['model'],
                    colors = colors or DEF_STR['colors'],
                    partnum = partnum or DEF_STR['pnum'],
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
                    shape = to_enum(shape, Shape),
                    diffusion = to_enum(diffusion, Diffusion),
                    viewAngle = viewAngle or 0,
                    bendDir = to_enum(bendDir, BendDir),
                    cri = cri or 0,
                    cct = cct or 0,
                    fixt_l_mm = fixt_l_mm or 0,
                    fixt_w_mm = fixt_w_mm or 0,
                    fixt_h_mm = fixt_h_mm or 0,
                    protocol = to_enum(protocol, Protocol),
                    wireCode = wireCode or DEF_STR['wcode'],
                    url = url or DEF_STR['url'],
                    datasheet = datasheet  or DEF_STR['dsheet'],
                    ul_list = ul_list or False,
                    ul_recog = ul_recog or False,
                    cert_url = cert_url or DEF_STR['certurls'],
                    ipRating = to_enum(ipRating, IPRating),
                    finish = to_enum(finish, FinishColor),
                    lumens_m = lumens_m or [],
                    lumens_ft = lumens_ft or [],
                 
                 )


#& TERMINAL FACTORY
def new_terminal(*,
                #? BASE ID PARAMS
                name : str | None=None,
                comments : list[str] | None=None,

                #? TERMINAL PARAMS
                conn_dir : ConnDir | None=None,
                conn_type : ConnType | None=None,
                **kwargs,
                ) -> Terminal:

    return  Terminal(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=kwargs.get('comments')),

                    #? TERMINAL PARAMS
                    conn_dir= to_enum(conn_dir, ConnDir),
                    conn_type= to_enum(conn_type, ConnType),
                    )


#& CABLE FACTORY
def new_cable(*,
            #? BASE ID PARAMS
            name : str | None=None,
            comments : list[str] | None=None,
              
            #? CABLE PARAMS
            terminals : list['Terminal'] | None=None,
            gauge : WireSize | None=None,
            **kwargs,
            ) -> Cable:

    return Cable(
                #? BASE ID PARAMS
                **base_id(name=name,comments=kwargs.get('comments')),
                
                #? CABLE PARAMS
                terminals=terminals or [],
                gauge= to_enum(gauge, WireSize)

                )


#& 3D PATH FACTORY
def new_path3d(*,
               #? BASE ID PARAMS
               name : str | None=None,
               comments : list[str] | None=None,
               
               #? PATH3D PARAMS
               geometry : list[np.ndarray] | None=None,
               **kwargs,
               ) -> Path3D:

    return Path3D(
                #? BASE ID PARAMS
                **base_id(name=name,comments=kwargs.get('comments')),

                #? PATH3D PARAMS
                geometry=geometry or [],

                )


#& LED BRANCH FACTORY
def new_ledbranch(*,
                  #? BASE ID PARAMS
                  name : str | None=None,
                  comments : list[str] | None=None,
                  
                  #? LED BRANCH PARAMS
                  segments : list['LEDSeg'] | None=None,
                  **kwargs,
                  ) -> LEDBranch:

    return LEDBranch(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=kwargs.get('comments')),
                    
                    #? LED BRANCH PARAMS
                    segments=segments or [],
                     
                    )


#& LED SEGMENT FACTORY
def new_ledsegment(*,
                   #? BASE ID PARAMS
                   name :str | None=None,
                   comments : list[str] | None=None,

                   #? LED SEGMENT PARAMS
                   led_prod : LEDFixt, #!REQUIRED
                   len_m    : float    | None=None,
                   **kwargs,
                   ) -> LEDSeg:

    return LEDSeg(
                  #? BASE ID PARAMS
                  **base_id(name=name,comments=kwargs.get('comments')),

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