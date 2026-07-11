from philh_myftp_biz.terminal import Args
from philh_myftp_biz.pc import Path
from os import getpid

PIDstore = Path('E:/Plex/Optimization/__pycache__/PID.txt').TXT
PIDstore.save(getpid())

Args.Arg('limit', 100, None, str)

