
from philh_myftp_biz.web.torrent import thePirateBay, qBitTorrent
from philh_myftp_biz.web.driver import Driver
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.terminal import Log
from json.decoder import JSONDecodeError
from philh_myftp_biz.array import List
from philh_myftp_biz.file import JSON
from os import getpid

#==============================================

this = Module('E:/Plex/')
VM = Module('E:/Virtual Machines/')

PIDstore: List[str] = List(JSON(this.child('/Torrenting/__pycache__/PID.json')))
PIDstore.save([f'python-{getpid()}'])

#==============================================

Args.Arg(
    name = 'filter',
    default = '',
    desc = 'Only download items whose title contains this',
    handler = lambda x: x.split('|')
)

Args.Arg(
    name = 'limit',
    default = 100,
    desc = 'Maximum # of items to download',
    handler = int
)

Args.Arg(
    name = 'timeout',
    default = 300, # 5 minutes
    desc = '# of seconds to wait before timing out',
    handler = int
)

#==============================================

VM.runH('Start', 'Torrenting')

Log.VERB(f"Discovering VM\nname='Torrenting'")

while True:
    try: 
        qBitTorrent.connect(
            host = VM.cap('IP', 'Torrenting'),
            username = 'admin',
            password = 'Torrenting123!',
            timeout = Args['timeout']
        )
        break
    except JSONDecodeError, ConnectionError: 
        pass

#==============================================

driver = Driver(
    headless = (not Args['verbose']),
    eager = True
)

for pid in driver.Task.PIDs:
    PIDstore += f'firefox-{pid}'

thePirateBay.driver = driver

#==============================================