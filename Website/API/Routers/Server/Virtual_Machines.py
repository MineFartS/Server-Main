from philh_myftp_biz.modules import Module
from fastapi.responses import FileResponse
from philh_myftp_biz.file import temp
from fastapi import APIRouter
from ... import User

# Declare FastAPI router
router = APIRouter(
    prefix = '/Server/Virtual Machines'
)

# Virtual Machine Module
VM = Module('E:/Virtual Machines')

# 
templ = """
full address:s:philh.myftp.biz
pcb:s:{id}
server port:i:2179
negotiate security layer:i:0
screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
winposstr:s:0,3,0,0,800,600
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:0
enableworkspacereconnect:i:0
remoteappmousemoveinject:i:1
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
audiomode:i:0
redirectprinters:i:1
redirectlocation:i:1
redirectcomports:i:1
redirectsmartcards:i:1
redirectwebauthn:i:1
redirectclipboard:i:1
redirectposdevices:i:0
camerastoredirect:s:*
devicestoredirect:s:*
drivestoredirect:s:*
autoreconnection enabled:i:1
authentication level:i:0
prompt for credentials:i:0
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
enablerdsaadauth:i:0
"""

@router.get('/connectRDP')
async def _(
    username: str,
    token: str
) -> FileResponse: # pyright: ignore[reportReturnType]
    
    user = User(username)

    if user.checkAuth(token):

        code = templ.format(
            id = VM.cap('ID', f'User-{username}')
        )

        file = temp(
            name = 'connect',
            ext = 'rdp'
        )

        with file.open('w') as f:
            f.write(code)

        return FileResponse(
            path = str(file),
            filename = f'{username}.rdp',
            media_type = 'application/octet-stream'
        )

@router.get('/start')
async def _(
    username: str,
    token: str
) -> None:
    
    user = User(username)

    if user.checkAuth(token):

        VM.run(
            'start', 
            f'User-{username}'
        )

@router.get('/stop')
async def _(
    username: str,
    token: str
) -> None:
    
    user = User(username)

    if user.checkAuth(token):
    
        VM.run(
            'stop', 
            f'User-{username}'
        )

@router.get('/status')
async def read_item(
    username: str,
    token: str
) -> None | bool:
    
    user = User(username)

    if user.checkAuth(token):
    
        # Get the power status of the virtual machine
        return VM.cap(
            'status', 
            f'User-{username}'
        ) # pyright: ignore[reportReturnType]
