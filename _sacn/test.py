



import os, sys
from pathlib import Path



#* FIND PROJECT ROOT AND INSERT IF NOT IN SYSTEM PATH *#
import os, sys
from pathlib import Path
TREE = [str(p) for p in Path(__file__).resolve().parents]
ROOT = 'DEEREATCHAIN'  #? ROOT FOLDER TO LOOK FOR
for path in TREE:
    if Path(path).name == ROOT:
        if path not in sys.path:
            print(f'ADDING {ROOT} TO SYSTEM PATHS')
            sys.path.insert(0, path)
            
#* ROOT FINDER -------------------------------------- *#


test = [{ '1' : bytearray(512) }]
print(f'{test[0]['1']}')