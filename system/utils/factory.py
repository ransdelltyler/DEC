
#* ======================================================== *#
#*                    FILE DESCRIPTION                   
#*
#*
#*
#*
#* ======================================================== *#



from __future__ import annotations
from enum import Enum
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


from uuid import UUID, uuid4

import numpy as np

from system.utils.util_classes import ColorLog
from typing import Literal

from system.utils.data_models import ( 
                        PSU, EQCategory, GenDescr, CTRLType, Voltage, LEDProtocol,
                        Shape, Diffusion, BendDir, EQProto, IPRating,
                        FinishColor,Fuse,ConnDir,ConnType, WireSize,
                        CableType, )

from system.utils.data_models import ( 
                        BaseID, 
                        Equipment, Enclosure, Ctrlr, LEDProd,
                        )

from system.utils.design_models import ( 
                        Fixture, Controller, PowerSupply,
                        Project, Anchor, Room, Install,
                        Terminal, Cable, Path3D, LEDBranch,
                        )

#! ======================================================== !#
#!                   DEFAULTS / VARIABLES                   !#
#! ======================================================== !#

log = ColorLog('DATA_FACT',level=1)


#? ======================================================== ?#
#?                    HELPER FUNCTIONS                      ?#
#? ======================================================== ?#

def base_id(*, name, description, comments):
    return {
        'name' : name or '',
        'description' : description or '',
        'comments' : comments or [],
    }

def equipment_base(*,
                manuf = None,
                model = None,
                partnum = None,
                vin = None,
                vout = None,
                fuse : Fuse | None = None,
                l_mm = None,
                w_mm = None,
                h_mm = None,
                rated_watts = None,
                actual_watts = None,
                url = None,
                datasheet = None,
                ul_list = None,
                ul_recog = None,
                cert_url = None,
                iprating = None,
                finish = None,
                price = None,
                eqproto = EQProto.UNKWN,
                eq_category = EQCategory.UNKWN,
                related_pns = None,
                terminals = None,
                ):
    return {
        'manuf' : manuf,
        'model' : model or '',
        'partnum' : partnum,
        'vin' : to_enum(vin, Voltage) if vin is not None else Voltage.UNKWN,
        'vout' : to_enum(vout, Voltage) if vout is not None else Voltage.UNKWN,
        'fuse' : to_enum(fuse, Fuse.UNKWN),
        'l_mm' : l_mm or 0,
        'w_mm' : w_mm or 0,
        'h_mm' : h_mm or 0,
        'rated_watts' : rated_watts or 0,
        'actual_watts' : actual_watts or 0,
        'url' : url or '',
        'datasheet' : datasheet or '',
        'ul_list' : ul_list or GenDescr.UNKWN,
        'ul_recog' : ul_recog or GenDescr.UNKWN,
        'cert_url' : cert_url or '',
        'iprating' : to_enum(iprating, IPRating) if iprating is not None else IPRating.UNKWN,
        'finish' : to_enum(finish, FinishColor) if finish is not None else FinishColor.UNKWN,
        'price' : price or 0.0,
        'eqproto' : eqproto,
        'eq_category' : eq_category,
        'related_pns' : related_pns or [],
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
def to_enum(value, enum_cls) -> Enum:
    if isinstance(value, Enum):
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
                description: str,
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
                   **base_id(name=name, description=description, comments=comments),
                   #? PROJECT PARAMS
                   address = address or '!NONE!',
                   anchors = anchors or [],
                   )


#& ANCHOR FACTORY
def new_anchor(*,
               #? BASE ID PARAMS
               name = str,
               description = None,
               comments = None,
               
               #? ANCHOR PARAMS
               rooms = None,
               **kwargs,) -> Anchor:
    
    return Anchor(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),
                  
                  #? ANCHOR PARAMS
                rooms = rooms or [],
                )


#& ROOM FACTORY
def new_room(*,
             #? BASE ID PARAMS
             name = None,
             description = None,
             comments = None,

             #? ROOM PARAMS
             enclosures = None,
             installs = None,
             **kwargs,) -> Room:
    
    return Room(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),

                #? ROOM PARAMS
                enclosures=enclosures or [],
                installs=installs or []
                )


#& INSTALL FACTORY
def new_install(*,
                #? BASE ID PARAMS
                name = None,
                description = None,
                comments = None,
                #? INSTALL PARAMS
                actual_watts = None,
                rated_watts = None,
                branches = None,
                **kwargs,) -> Install:
    # TODO : ADD ENCLOSURE MAP
    return Install(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),
                
                #? INSTALL PARAMS
                actual_watts = actual_watts if actual_watts is not None else 0,
                rated_watts= rated_watts if rated_watts is not None else 0,
                branches=branches or [],
                )


#& EQUIPMENT FACTORY
def new_equipment(*,
                #? BASE ID PARAMS
                name = None,
                description = None,
                comments=None,
                #? EQUIPMENT PARAMS
                manuf = None,
                model = None,
                partnum = None,
                vin = None,
                vout = None,
                fuse = None,
                l_mm = None,
                w_mm = None,
                h_mm = None,
                rated_watts = None,
                actual_watts = None,
                url = None,
                datasheet = None,
                ul_list = None,
                ul_recog = None,
                cert_url = None,
                iprating = None,
                finish = None,
                price = None,
                eqproto : EQProto,
                eq_category : EQCategory = EQCategory.UNKWN,
                related_pns = None,
                terminals = None,
                  **kwargs,) -> Equipment:
    
    return Equipment(
                    #? BASE ID PARAMS
                    **base_id(name=name, description=description, comments=comments),
                    #? EQUIPMENT PARAMS
                    **equipment_base(
                            manuf = manuf,
                            model = model or '',
                            partnum = partnum,
                            vin = vin,
                            vout = vout,
                            fuse = fuse,
                            l_mm = l_mm,
                            w_mm = w_mm,
                            h_mm = h_mm,
                            rated_watts = rated_watts,
                            actual_watts = actual_watts,
                            url = url or '',
                            datasheet = datasheet or '',
                            ul_list = ul_list,
                            ul_recog = ul_recog,
                            cert_url = cert_url or '',
                            iprating = iprating,
                            finish = finish,
                            price = price,
                            eqproto = eqproto,
                            eq_category = eq_category,
                            related_pns = related_pns or [],
                            terminals = terminals,
                            ),
                    )


#& ENCLOSURE FACTORY
def new_enclosure(*,
                #? BASE ID PARAMS
                name = None,
                description = None,
                comments = None,
                #? EQUIPMENT PARAMS
                manuf = None,
                model = None,
                partnum = None,
                vin = None,
                vout = None,
                fuse = None,
                l_mm = None,
                w_mm = None,
                h_mm = None,
                rated_watts = None,
                actual_watts = None,
                url = None,
                datasheet = None,
                ul_list = None,
                ul_recog = None,
                cert_url = None,
                iprating = None,
                finish = None,
                price = None,
                eqproto : EQProto,
                eq_category : EQCategory,
                related_pns = None,
                terminals = None,
                #? ENCLOSURE PARAMS
                ckts = None,
                nets = None,
                equipment = None,
                **kwargs,) -> Enclosure:
    
    return Enclosure(
                    #? BASE ID PARAMS
                    **base_id(name=name, description=description, comments=comments),                    
                    **equipment_base(
                            manuf = manuf,
                            model = model or '',
                            partnum = partnum,
                            vin = vin,
                            vout = vout,
                            fuse = fuse,
                            l_mm = l_mm,
                            w_mm = w_mm,
                            h_mm = h_mm,
                            rated_watts = rated_watts,
                            actual_watts = actual_watts,
                            url = url or '',
                            datasheet = datasheet or '',
                            ul_list = ul_list,
                            ul_recog = ul_recog,
                            cert_url = cert_url or '',
                            iprating = iprating,
                            finish = finish,
                            price = price,
                            eqproto = eqproto,
                            eq_category = eq_category,
                            related_pns = related_pns or [],
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
            description = None,
            comments = None,
            #? EQUIPMENT PARAMS
            manuf = None,
            model = None,
            partnum = None,
            vin = None,
            vout = None,
            fuse : Fuse | None = None,
            l_mm = None,
            w_mm = None,
            h_mm = None,
            rated_watts = None,
            actual_watts = None,
            url = None,
            datasheet = None,
            ul_list : GenDescr = GenDescr.UNKWN,
            ul_recog : GenDescr = GenDescr.UNKWN,
            cert_url=None,
            iprating : IPRating = IPRating.UNKWN,
            finish : FinishColor = FinishColor.UNKWN,
            price = None,
            eqproto : EQProto = EQProto.UNKWN,
            eq_category : EQCategory = EQCategory.CTRLR,
            related_pns = None,
            terminals = None,            
            #? CONTROLLER PARAMS
            ip = None,
            subn_mask = None,
            ctrl_type = CTRLType.UNKWN,
            outputs = None,
            **kwargs,) -> Ctrlr:
    
    return Ctrlr(
                 #? BASE ID PARAMS
                 **base_id(name=name, description=description, comments=comments),
                 
                 **equipment_base(
                            manuf = manuf,
                            model = model or '',
                            partnum = partnum,
                            vin = vin,
                            vout = vout,
                            fuse = fuse,
                            l_mm = l_mm,
                            w_mm = w_mm,
                            h_mm = h_mm,
                            rated_watts = rated_watts,
                            actual_watts = actual_watts,
                            url = url or '',
                            datasheet = datasheet or '',
                            ul_list = ul_list,
                            ul_recog = ul_recog,
                            cert_url = cert_url or '',
                            iprating = iprating,
                            finish = finish,
                            price = price,
                            eqproto = eqproto,
                            eq_category = eq_category,
                            related_pns = related_pns or [],
                            terminals = terminals,
                            ),
                 
                 #? CONTROLLER PARAMS
                 ip=ip or '0.0.0.0',
                 subn_mask=subn_mask or '',
                 outputs=outputs or [],
                 ctrl_type= ctrl_type,
                )


#& LED FIXTURE FACTORY
def new_ledprod(*,
                #? BASE ID PARAMS
                name = None,
                description = None,
                comments = None,
                #? EQUIPMENT PARAMS
                manuf = None,
                model = None,
                partnum = None,
                vin = None,
                fuse : Fuse | None = None,
                l_mm = None,
                w_mm = None,
                h_mm = None,
                rated_watts = None,
                actual_watts = None,
                url = None,
                datasheet = None,
                ul_list : GenDescr = GenDescr.UNKWN,
                ul_recog : GenDescr = GenDescr.UNKWN,
                cert_url=None,
                iprating : IPRating = IPRating.UNKWN,
                finish : FinishColor = FinishColor.UNKWN,
                price = None,
                eqproto : EQProto = EQProto.UNKWN,
                eq_category : EQCategory = EQCategory.LEDTAPE,
                related_pns = None,
                terminals = None,            
                #? LED PRODUCT PARAMS
                colors = None,
                watt_m = None,
                watt_ft = None,
                m_roll = None,
                cutLen_mm = None,
                cutLen_in = None,
                pixPitch_m = None,
                shape : Shape = Shape.UNKWN,
                diffusion : Diffusion = Diffusion.UNKWN,
                viewAngle = None,
                bendDir : BendDir = BendDir.UNKWN,
                cri = None,
                cct = None,
                wireCode = None,
                lumens_m = None,
                lumens_ft = None,
                max_length_m = None,
                **kwargs,) -> LEDProd:
    
    
    return LEDProd(
                    #? BASE ID PARAMS
                    **base_id(name=name, description=description, comments=comments),
                    
                    **equipment_base(
                                manuf = manuf,
                                model = model or '',
                                partnum = partnum,
                                vin = vin,
                                fuse = fuse,
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                url = url or '',
                                datasheet = datasheet or '',
                                ul_list = ul_list,
                                ul_recog = ul_recog,
                                cert_url = cert_url or '',
                                iprating = iprating,
                                finish = finish,
                                price = price,
                                eqproto = eqproto,
                                eq_category = eq_category,
                                related_pns = related_pns or [],
                                terminals = terminals,
                                ),

                    #? LED FIXTURE PARAMS
                    colors = colors or '',
                    watt_m = watt_m or 0,
                    watt_ft = watt_ft or 0,
                    m_roll = m_roll or 0,
                    cutLen_mm = cutLen_mm or 0,
                    cutLen_in = cutLen_in or 0,
                    pixPitch_m =  pixPitch_m or 0,
                    shape = shape,
                    diffusion = diffusion,
                    viewAngle = viewAngle or 0,
                    bendDir = bendDir,
                    cri = cri or 0,
                    cct = cct or 0,
                    wireCode = wireCode or '',
                    lumens_m = lumens_m or '',
                    lumens_ft = lumens_ft or '',
                    max_length_m = max_length_m or 0,
                 )
    
    
#& POWER SUPPLY FACTORY
def new_psu(*,
            #? BASE ID PARAMS
            name = None,
            description = None,
            comments = None,
            #? EQUIPMENT PARAMS
            manuf = None,
            model = None,
            partnum = None,
            vin = None,
            vout = None,
            fuse : Fuse | None = None,
            l_mm = None,
            w_mm = None,
            h_mm = None,
            rated_watts = None,
            actual_watts = None,
            url = None,
            datasheet = None,
            ul_list : GenDescr = GenDescr.UNKWN,
            ul_recog : GenDescr = GenDescr.UNKWN,
            cert_url=None,
            iprating : IPRating = IPRating.UNKWN,
            finish : FinishColor = FinishColor.UNKWN,
            price = None,
            eqproto : EQProto = EQProto.UNKWN,
            eq_category : EQCategory = EQCategory.PSU,
            related_pns = None,
            terminals = None,            
            #? PSU PARAMS
            amps_port = None,
            p_class = None,
            efficiency = None,
            dimming = None,
            current_share : bool = False,
            **kwargs,
            ) -> PSU:
    return PSU(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),
                
                **equipment_base(
                                manuf = manuf,
                                model = model or '',
                                partnum = partnum,
                                vin = vin,
                                vout = vout,
                                fuse = fuse,
                                l_mm = l_mm,
                                w_mm = w_mm,
                                h_mm = h_mm,
                                rated_watts = rated_watts,
                                actual_watts = actual_watts,
                                url = url or '',
                                datasheet = datasheet or '',
                                ul_list = ul_list,
                                ul_recog = ul_recog,
                                cert_url = cert_url or '',
                                iprating = iprating,
                                finish = finish,
                                price = price,
                                eqproto = eqproto,
                                eq_category = eq_category,
                                related_pns = related_pns or [],
                                terminals = terminals,
                                ),
                
                #? PSU PARAMS
                amps_port = amps_port or 0.0,
                p_class = p_class or '',
                efficiency = efficiency or '',
                dimming = dimming or '',
                current_share = current_share if current_share is not None else False,
                )


#& TERMINAL FACTORY
def new_terminal(*,
                #? BASE ID PARAMS
                name = None,
                description = None,
                comments = None,
                
                #? TERMINAL PARAMS
                conn_dir : ConnDir= ConnDir.UNKWN,
                conn_type : ConnType = ConnType.UNKWN,
                **kwargs,) -> Terminal:

    return  Terminal(
                    #? BASE ID PARAMS
                    **base_id(name=name, description=description, comments=comments),

                    #? TERMINAL PARAMS
                    conn_dir= conn_dir,
                    conn_type= conn_type,
                    )


#& CABLE FACTORY
def new_cable(*,
            #? BASE ID PARAMS
            name=None,
            description=None,
            comments=None,
              
            #? CABLE PARAMS
            terminals : list['Terminal'] | None=None,
            gauge : WireSize = WireSize.UNKWN,
            **kwargs,) -> Cable:

    return Cable(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),
                
                #? CABLE PARAMS
                terminals=terminals or [],
                gauge= gauge

                )


#& 3D PATH FACTORY
def new_path3d(*,
               #? BASE ID PARAMS
               name=None,
               description=None,
               comments=None,
               
               #? PATH3D PARAMS
               geometry : list[np.ndarray] | None=None,
               **kwargs,) -> Path3D:

    return Path3D(
                #? BASE ID PARAMS
                **base_id(name=name, description=description, comments=comments),

                #? PATH3D PARAMS
                geometry=geometry or [],

                )


#& LED BRANCH FACTORY
def new_ledbranch(*,
                  #? BASE ID PARAMS
                  name=None,
                  description=None,
                  comments=None,
                  
                  #? LED BRANCH PARAMS
                  segments : list['Fixture'] | None = None,
                  **kwargs,) -> LEDBranch:

    return LEDBranch(
                    #? BASE ID PARAMS
                    **base_id(name=name, description=description, comments=comments),
                    
                    #? LED BRANCH PARAMS
                    segments=segments or [],
                     
                    )







