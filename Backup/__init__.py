from philh_myftp_biz.web.ftp import FTPPath
from philh_myftp_biz.pc import Path, loc
from philh_myftp_biz.web.ftp import FTP
from philh_myftp_biz import VERBOSE
from philh_myftp_biz.db import Ring
from typing import Generator
from os import getpid

VERBOSE.enable()

# Store PID
with loc.cache.child('PID.txt').open('w') as f:
    f.write(str(getpid()))

ring = Ring('FTP Backup Service')
password = ring.Key('Admin Password')

if password.read() is None:
    password.prompt(secure=True)

# Connect to the FTP server
ftp = FTP(
    host = 'philh.myftp.biz',
    username = 'Administrator',
    password = password.read()
)

class PathPair:

    def __init__(self,
        path: Path|FTPPath
    ) -> None:

        if isinstance(path, Path):

            self.local = path

            _path = str(path).replace('E:/', '/E/', 1)
            
            self.remote = ftp.Path(_path)

        elif isinstance(path, FTPPath):

            self.remote = path

            _path = str(path).replace('/E/', 'E:/', 1)
            
            self.local = Path(_path)

    def __str__(self) -> str:
        return f'\nlocal={self.local}\nremote={self.remote}'
    
    def __eq__(self, other:PathPair):
        return (self.local == other.local)

def Scan() -> Generator[Path | FTPPath]:

    for path in Path('E:/').children:

        if path.name == 'Backup':
            continue

        for d in path.descendants:
        
            if d.is_dir:
                pass

            elif '/$RECYCLE.BIN/' in d.path:
                pass

            elif '/.git/' in d.path:
                pass

            else:
                yield d

    # E:/Plex/WinTV/
    yield from ftp.Path('/E/Plex/WinTV/').descendants

    # E:/Website/Root/
    for path in ftp.Path('/E/Website/Root/').descendants:
        if path.seg() != 'index.json':
            yield path

    # E:/Users/philh/
    for path in ftp.Path('/E/Users/philh/').children:
        if path.name != 'Administrator':
            yield from path.descendants
