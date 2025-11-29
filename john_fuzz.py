
from keywords import FIXT_FUZZ_KEYS, CTRLR_FUZZ_KEYS, EQUIP_FUZZ_KEYS, GENERIC_KEYWORDS
from data_models import EQCategory
from rapidfuzz import process, fuzz

from util_classes import ColorLog
log = ColorLog('JOHN_FUZZ')

# RETURN TEXT AS LOWERCASE WITH NO SPACES
def norm_text(text: str):
    return ''.join(text.lower().split())

#^ FUZZ KEYWORD CATEGORY MAP
CATEGORY_MAP = {
    EQCategory.CTRLR : CTRLR_FUZZ_KEYS,
    EQCategory.FIXT : FIXT_FUZZ_KEYS,
    EQCategory.EQUIP : EQUIP_FUZZ_KEYS,
}

#* TAKES A LABEL:STR AND USES A DEF OR GIVEN KEYWORD DICT-
#* -TO FIND BEST MATCH 
#* RETURNS:(LABEL/VALUE)
def match_label(label : str, category: EQCategory | dict):
    # CAN BE PASSED AS KEYWORD DICTIONARY: {str,[str]}
    # OR SET BY PASSING EQCategory.<type>
    fuzz_keys = (
        category if isinstance(category,dict)
        else CATEGORY_MAP.get(category, GENERIC_KEYWORDS)
    )
    # NORMALIZE THE TEXT FOR COMPARISSON
    label_norm = norm_text(label)
    
    best_key = None
    best_score = 0
    for key, key_map in fuzz_keys.items():
        result = process.extractOne(
            label_norm,
            [norm_text(p) for p in key_map],
            scorer=fuzz.token_sort_ratio)
        
        if not result:
            continue
        
        match, score, _ = result
        if score > best_score:
            best_key = key
            best_score = score

    return best_key, best_score
