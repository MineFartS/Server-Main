from philh_myftp_biz.terminal import set_package

set_package('E:/Minecraft')

from .World import Worlds
from . import Tasks

for w in Worlds:
    Tasks[w.name].stop()

