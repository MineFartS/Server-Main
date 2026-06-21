from .World import Worlds
from . import Tasks

for w in Worlds:
    if Tasks[w.name].running:
        print('true')
        break

else:    
    print('false')