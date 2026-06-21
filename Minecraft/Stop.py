from .World import Worlds
from . import Tasks

for w in Worlds:
    Tasks[w.name].stop()

