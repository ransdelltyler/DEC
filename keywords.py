# //////////////////////////////////////////////////////////////////////////////////////#
# HOLDS DICTIONARIES OF VARIABLE_NAME(PYTHON) : KEYWORD(EXCEL-COL-NAME)
# - LED_KEYWORDS
# - PSU_KEYWORDS
# - CTRLR_KEYWORDS
# - GENERIC_KEYWORDS
# //////////////////////////////////////////////////////////////////////////////////////#

# ------ START KEYWORD DEFINITION BLOCK ------ #

# KEYWORDS USED TO FIND COLUMN INDEXES | VAR : COLUMN_NAME
# LED EQUIPMENT | ENVI_ELUXTRA_NEON_WTP_RGB30K {...}
#               | MANUFACTURER_MODEL_TYPE_SUBTYPE_COLORS
LED_KEYWORDS = {
    'manu' : 'Manufacturer',
    'model' : 'Model',
    'name' : 'Name',
    'colors' : 'LED Colors',
    'partnum' : 'PN',
    'vin' : 'VIN',
    'watt_m' : 'Watt/m',
    'watt_ft' : 'Watt/ft',
    'm_roll' : 'M/Roll',
    'led_m' : 'LED/m',
    'price' : 'Price',
    'cutLen_mm' : 'Cut Length (mm)',
    'cutLen_in' : 'Cut Length (in)',
    'pixPitch_m' : 'Pixel Pitch (m)',
    'tapeWidth_mm' : 'Tape Width (mm)',
    'accessories' : 'Accessories',
    'shape' : 'Shape',
    'diffusion' : 'Diffusion',
    'viewAngle' : 'View Angle',
    'bendDir' : 'Bend Direction',
    'cri' : 'CRI',
    'cct' : 'CCT',
    'lumens_m' : 'Lumens (m)',
    'lumens_ft' : 'Lumens (ft)',
    'length' : 'Length',
    'width' : 'Width',
    'height' : 'Height',
    'protocol' : 'Protocol',
    'wireCode' : 'Wire Color Code',
    'url' : 'URL',
    'datasheet' : 'Datasheet',
    'ul_list' : 'UL Listed',
    'ul_recog' : 'UL Recognized',
    'cert_url' : 'Certification URL',
    'ipRating' : 'IP Rating',
    'finish' : 'Finish',
    'comments' : 'Comments'
}

# PSU EQUIPMENT | MEANWELL_HLG240 {...}
#               | MANUFACTURER_MODEL
PSU_KEYWORDS = {
    'manu' : 'Manufacturer',
    'model' : 'Model',
    'name' : 'Name',
    'partnum' : 'PN',
    'vin' : 'Vin',
    'vout' : 'Vout',
    'wattage' : 'Wattage',
    'amp' : 'Amps',
    'p_class' : 'Class',
    'efficiency' : 'Efficiency',
    'length' : 'Length',
    'width' : 'Width',
    'height' : 'Height',
    'dimming' : 'Dimming',
    'url' : 'URL',
    'datasheet' : 'Datasheet',
    'ul_list' : 'UL Listed',
    'ul_recog' : 'UL Recognized',
    'cert_url' : 'Certification URL',
    'price' : 'Price',
    'comments' : 'Comments'
}

# CONTROLLER EQUIPMENT | ADVATEK_R1FS {...}
#                      | MANUFACTURER_MODEL
CTRLR_KEYWORDS = {
    'manu' : 'Manufacturer',
    'model' : 'Model',
    'name' : 'Name',
    'partnum' : 'PN',
    'type' : 'Type',
    'vin' : 'Vin',
    'vout' : 'Vout',
    'amps_port' : 'Amps / Port',
    'fused' : 'Fused',
    'price' : 'Price',
    'url' : 'URL',
    'datasheet' : 'Datasheet',
    'ul_list' : 'UL Listed',
    'ul_recog' : 'UL Recognized',
    'channels' : 'Channels',
    'pixels_out' : 'Pixels / Output',
    'outputs' : 'Outputs',
    'din' : 'DIN',
    'dout' : 'DOUT',
    'mounting' : 'Mounting',
    'accessories' : 'Accessories',
    'length' : 'Length',
    'width' : 'Width',
    'height' : 'Height',
    'comments' : 'Comments'
}

# GENERIC EQUIPMENT | GEN_RECEPTACLE {...}, GEN_WIRE {...}, GEN_BUTTON {...}
#                   | MANUFACTURER_MODEL
GENERIC_KEYWORDS = {
    'manu' : 'Manufacturer',
    'model' : 'Model',
    'name' : 'Name',
    'partnum' : 'PN',
    'description' : 'Description',
    'vin' : 'Vin',
    'vout' : 'Vout',
    'wattage' : 'Wattage',
    'price' : 'Price',
    'url' : 'URL',
    'datasheet' : 'Datasheet',
    'unit_qty' : 'Unit Qty',
    'comments' : 'Comments'
}


# ------ END KEYWORD DEFINITION BLOCK ------ #

# //////////////////////////////////////////////////////////////////////////////////////#