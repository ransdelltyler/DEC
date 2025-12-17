# HOLDS DICTIONARIES OF VARIABLE_NAME(PYTHON) : KEYWORD(EXCEL-COL-NAME)
# - LED_KEYWORDS
# - PSU_KEYWORDS
# - CTRLR_KEYWORDS
# - GENERIC_KEYWORDS

#? ======================================================== ?#
#?                   RAPIDFUZZ KEYWORDS                     ?#
#? ======================================================== ?#
FIXT_FUZZ_KEYS = {
    'model': [
        'Name',
        'Title',
    ],
    'colors':[
        'Light Color',
        'Light Color Detail',
        'LED Colors',
        'Colors',
    ],
    'partnum': [
        'Product Number',
        'PN',
        'Part Number',
        'SKU',
        'Model Number',
    ],
    'watt_m': [
        'Power (Watts/m)',
        'Watts per Meter',
        'Watts/m',
    ],
    'watt_ft': [
        'Power (Watts/ft)',
        'Watts per Foot',
        'Watts/ft',
    ],
    'm_roll': [
        'Length(Metric)',
        'Length Meters',
    ],
    'pixPitch_m': [
        'LED Density',
        'LEDs per Meter',
        'LEDs per m',
        'LEDs/m',
        'LED qty/m',
    ],
    'cutLen_mm': [
        'Min. Cutting Increment (Metric)',
        'Cut Length (mm)',
    ],
    'cutLen_ft': [
        'Min. Cutting Increment (English)',
        'Cut Length (ft)',
    ],
    'beam_angle': [
        'Beam Angle',
        'View Angle',
    ],
    'cri': [
        'CRI',
        'Color Rendering Index',
    ],
    'cct': [
        'Light Color Detail',
        'Color Temperature'
    ],
    'eqproto': [
        'Protocol',
    ],
    'iprating': [
        'IP Rating',
        'Outdoor Rating'
    ],
    'max_current': [
        'Max Current',
        'Maximum Current',
        'Current Draw',
        'Power Draw',
        'Input Current'
    ],
    'manufacturer':[
        'Manufacturer',
        'Manuf.'
    ],
    'lumens':[
        'Brightness',
        'Lumens',
        'Luminosity',
    ],
    'l_mm':[
        'Length(mm)',
        'Length(Metric)'
    ],
    'w_mm':[
        'Width',
        'Width(mm)',
        'Width(Metric)',
    ],

}

CTRLR_FUZZ_KEYS = {
    'ctrl_type': [
        'Product Type',
        'Control Output',
    ],
}

EQUIP_FUZZ_KEYS = {
    'vin': [
        'Input Voltage',
        'V Input',
        'VIN',
    ],
    'vout': [
        'Output Voltage',
        'V Output',
        'VOUT',
    ],
    'fuse': [
        'Fuse Rating',
        'Fuse Trip Current',
    ],
    'l_mm': [
        'Length (Metric)',
        'Length mm',
    ],
    'w_mm': [
        'Width (Metric)',
        'Width mm',
    ],
    'h_mm': [
        'Height (Metric)',
        'Height mm',
    ],
    'rated_watts': [
        'Input Current',
        'Max Wattage',
    ],
}

DEF_FUZZ_KEYS = {
    'name': [
        'Name',
        'Product Name',
        'Prod. Name',
        'Model Name',
        'Model',
        'Title'
    ],
    'type' : [
        'Product Type',
        'Control Type',
        'Fixture Type',
    ],
}

#? ======================================================== ?#
#?                   DATABASE KEYWORDS                      ?#
#? ======================================================== ?#
# KEYWORDS USED TO FIND COLUMN INDEXES | VAR : COLUMN_NAME
# LED EQUIPMENT | ENVI_ELUXTRA_NEON_WTP_RGB30K {...}
#               | MANUFACTURER_MODEL_TYPE_SUBTYPE_COLORS
LED_KEYWORDS = {
    'colors' : 'LEDColors',
    'watt_m' : 'Watt/m',
    'watt_ft' : 'Watt/ft',
    'm_roll' : 'M/Roll',
    'cutLen_mm' : 'CutLength(mm)',
    'cutLen_in' : 'CutLength(in)',
    'pixPitch_m' : 'PixelPitch(m)',
    'shape' : 'Shape',
    'diffusion' : 'Diffusion',
    'viewAngle' : 'ViewAngle',
    'bendDir' : 'BendDirection',
    'cri' : 'CRI',
    'cct' : 'CCT',
    'lumens_m' : 'Lumens(m)',
    'lumens_ft' : 'Lumens(ft)',
    'wireCode' : 'WireCode',
    
}

# PSU EQUIPMENT | MEANWELL_HLG240 {...}
#               | MANUFACTURER_MODEL
PSU_KEYWORDS = {
    'amps_port' : 'AmpsPerPort',
    'p_class' : 'Class',
    'efficiency' : 'Efficiency',
    'dimming' : 'Dimming',
}

# CONTROLLER EQUIPMENT | ADVATEK_R1FS {...}
#                      | MANUFACTURER_MODEL
CTRLR_KEYWORDS = {
    'type' : 'Type',
    'amps_port' : 'AmpsPerPort',
    'channels' : 'Channels',
    'pixels_out' : 'PixPerOut',
    'outputs' : 'Outputs',
    'din' : 'DIN',
    'dout' : 'DOUT',
    'mounting' : 'Mounting',
    'accessories' : 'Accessories',
}

# GENERIC EQUIPMENT | GEN_RECEPTACLE {...}, GEN_WIRE {...}, GEN_BUTTON {...}
#                   | MANUFACTURER_MODEL
GENERIC_KEYWORDS = {
    'name' : 'Name',
    'manuf' : 'Manufacturer',
    'model' : 'Model',
    'comments' : 'Comments',
    'partnum' : 'PN',
    'description' : 'Description',
    'vin' : 'Vin',
    'vout' : 'Vout',
    'rated_watts' : 'RatedWatts',
    'fused' : 'Fused',
    'l_mm' : 'Length(mm)',
    'w_mm' : 'Width(mm)',
    'h_mm' : 'Height(mm)',
    'price' : 'Price',
    'url' : 'URL',
    'datasheet' : 'Datasheet',
    'unit_qty' : 'UnitQty',
    'finish' : 'Finish',
    'iprating' : 'IPRating',
    'ul_list' : 'ULListed',
    'ul_recog' : 'ULRecognized',
    'cert_url' : 'CertURL',
    'related_pns' : 'RelatedPNs',
    'terminals' : 'Terminals',
}


# ------ END KEYWORD DEFINITION BLOCK ------ #
