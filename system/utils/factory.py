
#* ======================================================== *#
#*                    FILE DESCRIPTION                   
#*
#*
#*
#*
#* ======================================================== *#



from __future__ import annotations
import os, sys
from pathlib import Path
# set project root to DEEREATCHAIN (two levels up from this file)
ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# GLOBAL VARIABLES IMPORT
from DEEREATCHAIN.system.gen import settings
# CUSTOM COLORLOG CLASS
from system.utils.util_classes import ColorLog


from uuid import uuid4

import numpy as np

from util_classes import ColorLog
from typing import Literal

from DEEREATCHAIN.system.utils.data_models import ( 
                        GenDescr, CTRLType, Voltage, LEDProtocol,
                        Shape, Diffusion, BendDir, EQProto, IPRating,
                        FinishColor,Fuse,ConnDir,ConnType, WireSize,
                        CableType, )

from DEEREATCHAIN.system.utils.data_models import ( 
                        BaseID, Project, Anchor, Room, Install,
                        Equipment, Enclosure, Ctrlr, LEDProd,
                        Terminal, Cable, Path3D, LEDBranch,
                        LEDSeg, )


#! ======================================================== !#
#!                   DEFAULTS / VARIABLES                   !#
#! ======================================================== !#

log = ColorLog('DATA_FACT',level=1)

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

def equipment_base(*,
                   manuf = None,
                   vin = None,
                   vout = None,
                   fuse : Fuse | None = None,
                   l_mm = None,
                   w_mm = None,
                   h_mm = None,
                   rated_watts = None,
                   actual_watts = None,
                   terminals = None,
                   ):
    return {
        'manuf' : manuf or DEF_STR['manuf'],
        'vin' : int(vin) if vin is not None else 0,
        'vout' : int(vout) if vout is not None else 0,
        'fuse' : to_enum(fuse, Fuse.UNKWN),
        'l_mm' : l_mm or 0,
        'w_mm' : w_mm or 0,
        'h_mm' : h_mm or 0,
        'rated_watts' : rated_watts or 0,
        'actual_watts' : actual_watts or 0,
        'terminals' : terminals or [],
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
                name: str,
                comments = None,
                #? PROJECT PARAMS
                job_id = None,
                address = None,
                anchors = None,
                **kwargs,) -> Project:
    
    if job_id is None:
        job_id = str(job_id)
        
    if anchors is None:
        anchors = []
        
        
    return Project(
                   #? BASE ID PARAMS
                   **base_id(name=name,comments=comments),
                   #? PROJECT PARAMS
                   address = address or DEF_STR['jobaddr'],
                   anchors = anchors or [],
                   )


#& ANCHOR FACTORY
def new_anchor(*,
               #? BASE ID PARAMS
               name = None,
               comments = None,
               
               #? ANCHOR PARAMS
               anchor_name = None,
               rooms = None,
               **kwargs,) -> Anchor:
    
    return Anchor(
                  #? BASE ID PARAMS
                  **base_id(name=name,comments=comments),
                  
                  #? ANCHOR PARAMS
                  rooms = rooms or [],
                  )


#& ROOM FACTORY
def new_room(*,
             #? BASE ID PARAMS
             name = None,
             comments = None,

             #? ROOM PARAMS
             enclosures = None,
             installs = None,
             **kwargs,) -> Room:
    
    return Room(
                #? BASE ID PARAMS
                **base_id(name=name,comments=comments),

                #? ROOM PARAMS
                enclosures=enclosures or [],
                installs=installs or []
                )


#& INSTALL FACTORY
def new_install(*,
                #? BASE ID PARAMS
                name = None,
                comments = None,
                #? INSTALL PARAMS
                actual_watts = None,
                rated_watts = None,
                branches = None,
                **kwargs,) -> Install:
    # TODO : ADD ENCLOSURE MAP
    return Install(
                #? BASE ID PARAMS
                **base_id(name=name,comments=comments),
                
                #? INSTALL PARAMS
                actual_watts = actual_watts if actual_watts is not None else 0,
                rated_watts= rated_watts if rated_watts is not None else 0,
                branches=branches or [],
                )


#& EQUIPMENT FACTORY
def new_equipment(*,
                  #? BASE ID PARAMS
                  name = None,
                  comments=None,
                  #? EQUIPMENT PARAMS
                  manuf = None,
                  vin = None,
                  vout = None,
                  fuse : Fuse | None = None,
                  l_mm = None,
                  w_mm = None,
                  h_mm = None,
                  rated_watts = None,
                  actual_watts = None,
                  terminals = None,
                  **kwargs,) -> Equipment:
    
    return Equipment(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=comments),
                    #? EQUIPMENT PARAMS
                    **equipment_base(
                                manuf = manuf,
                                vin = vin,
                                vout = vout,
                                fuse = fuse,
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                terminals = terminals,
                            ),
                    )


#& ENCLOSURE FACTORY
def new_enclosure(*,
                  #? BASE ID PARAMS
                  name = None,
                  comments = None,
                  #? EQUIPMENT PARAMS
                  manuf = None,
                  vin = None,
                  vout = None,
                  fuse : Fuse | None = None,
                  l_mm = None,
                  w_mm = None,
                  h_mm = None,
                  rated_watts = None,
                  actual_watts = None,
                  terminals = None,
                  #? ENCLOSURE PARAMS
                  ckts = None,
                  nets = None,
                  equipment = None,
                  **kwargs,) -> Enclosure:
    
    return Enclosure(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=comments),                    
                    **equipment_base(
                                manuf = manuf,
                                vin = vin,
                                vout = vout,
                                fuse = fuse,
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                terminals = terminals,
                                ),

                    #? ENCLOSURE PARAMS
                    ckts=ckts or [],
                    nets=nets or [],
                    equipment=equipment or [],

                    
                    )


#& CONTROLLER FACTORY
def new_ctrlr(*,
              #? BASE ID PARAMS
              name = None,
              comments = None,
              #? EQUIPMENT PARAMS
              manuf = None,
              vin = None,
              vout = None,
              fuse : Fuse | None = None,
              l_mm = None,
              w_mm = None,
              h_mm = None,
              rated_watts = None,
              actual_watts = None,
              terminals = None,
              #? CONTROLLER PARAMS
              ip = None,
              subn_mask = None,
              ctrl_type = None,
              outputs = None,
              **kwargs,) -> Ctrlr:
    
    return Ctrlr(
                 #? BASE ID PARAMS
                 **base_id(name=name,comments=comments),
                 
                 **equipment_base(
                                manuf = manuf,
                                vin = vin,
                                vout = vout,
                                fuse = fuse,
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                terminals = terminals,
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
                name = None,
                comments = None,
                #? EQUIPMENT PARAMS
                manuf = None,
                vin = None,
                vout = None,
                fuse : Fuse | None = None,
                l_mm = None,
                w_mm = None,
                h_mm = None,
                rated_watts = None,
                actual_watts = None,
                terminals = None,            
                #? LED PRODUCT PARAMS
                model = None,
                colors = None,
                partnum = None,
                watt_m = None,
                watt_ft = None,
                m_roll = None,
                led_m = None,
                price = None,
                cutLen_mm = None,
                cutLen_in = None,
                pixPitch_m = None,
                tapeWidth_mm = None,
                sub_pns = None,
                shape : Shape | None = None,
                diffusion : Diffusion | None = None,
                viewAngle = None,
                bendDir : BendDir | None = None,
                cri = None,
                cct = None,
                fixt_l_mm = None,
                fixt_w_mm = None,
                fixt_h_mm = None,
                eqproto : EQProto | None = None,
                wireCode = None,
                url = None,
                datasheet = None,
                ul_list : GenDescr | None = None,
                ul_recog : GenDescr | None = None,
                cert_url=None,
                iprating : IPRating | None = None,
                finish : FinishColor | None = None,
                lumens_m : list[float] | None = None,
                lumens_ft : list[float] | None = None,
                **kwargs,) -> LEDProd:
    
    
    return LEDProd(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=comments),
                    
                    **equipment_base(
                                manuf = manuf,
                                vin = vin,
                                vout = vout,
                                fuse = to_enum(fuse, Fuse),
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                terminals = terminals,
                                ),

                    #? LED FIXTURE PARAMS
                    model = model or DEF_STR['model'],
                    colors = colors or DEF_STR['colors'],
                    partnum = partnum or DEF_STR['pnum'],
                    watt_m = watt_m or 0,
                    watt_ft = watt_ft or 0,
                    m_roll = m_roll or 0,
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
                    eqproto = to_enum(eqproto, EQProto),
                    wireCode = wireCode or DEF_STR['wcode'],
                    url = url or DEF_STR['url'],
                    datasheet = datasheet  or DEF_STR['dsheet'],
                    ul_list = to_enum(ul_list, GenDescr),
                    ul_recog = to_enum(ul_recog, GenDescr),
                    cert_url = cert_url or DEF_STR['certurls'],
                    iprating = to_enum(iprating, IPRating),
                    finish = to_enum(finish, FinishColor),
                    lumens_m = lumens_m or [],
                    lumens_ft = lumens_ft or [],
                 
                 )


#& TERMINAL FACTORY
def new_terminal(*,
                #? BASE ID PARAMS
                name = None,
                comments = None,
                
                #? TERMINAL PARAMS
                conn_dir = None,
                conn_type = None,
                **kwargs,) -> Terminal:

    return  Terminal(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=comments),

                    #? TERMINAL PARAMS
                    conn_dir= to_enum(conn_dir, ConnDir),
                    conn_type= to_enum(conn_type, ConnType),
                    )


#& CABLE FACTORY
def new_cable(*,
            #? BASE ID PARAMS
            name=None,
            comments=None,
              
            #? CABLE PARAMS
            terminals : list['Terminal'] | None=None,
            gauge : WireSize | None=None,
            **kwargs,) -> Cable:

    return Cable(
                #? BASE ID PARAMS
                **base_id(name=name,comments=comments),
                
                #? CABLE PARAMS
                terminals=terminals or [],
                gauge= to_enum(gauge, WireSize)

                )


#& 3D PATH FACTORY
def new_path3d(*,
               #? BASE ID PARAMS
               name=None,
               comments=None,
               
               #? PATH3D PARAMS
               geometry : list[np.ndarray] | None=None,
               **kwargs,) -> Path3D:

    return Path3D(
                #? BASE ID PARAMS
                **base_id(name=name,comments=comments),

                #? PATH3D PARAMS
                geometry=geometry or [],

                )


#& LED BRANCH FACTORY
def new_ledbranch(*,
                  #? BASE ID PARAMS
                  name=None,
                  comments=None,
                  
                  #? LED BRANCH PARAMS
                  segments : list['LEDSeg'] | None = None,
                  **kwargs,) -> LEDBranch:

    return LEDBranch(
                    #? BASE ID PARAMS
                    **base_id(name=name,comments=comments),
                    
                    #? LED BRANCH PARAMS
                    segments=segments or [],
                     
                    )


#& LED SEGMENT FACTORY
def new_ledsegment(*,
                   #? BASE ID PARAMS
                   name = None,
                   comments = None,

                   #? LED SEGMENT PARAMS
                   led_prod : list['LEDProd'] | None = None,
                   len_m : float | None = None,
                   **kwargs,) -> LEDSeg:

    return LEDSeg(
                  #? BASE ID PARAMS
                  **base_id(name=name,comments=comments),

                  #? LED SEGMENT PARAMS
                  led_prod=led_prod or [], 
                  len_m=len_m or 0.0,
                  )



#? ======================================================== ?#
#?                   EXTERNAL FUNCTIONS                     ?#
#? ======================================================== ?#




#^ ======================================================== ^#
#^                   TESTING / EXAMPLES                     ^#
#^ ======================================================== ^#