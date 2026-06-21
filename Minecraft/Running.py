from philh_myftp_biz.terminal import cls, set_package

set_package('E:/Minecraft')

from .World import Worlds
from . import Tasks

for w in Worlds:
    if Tasks[w.name].running:
        cls()
        print('true')
        break

else:    
    cls()
    print('false')