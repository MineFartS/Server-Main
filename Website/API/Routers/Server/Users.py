from fastapi.responses import HTMLResponse, FileResponse
from philh_myftp_biz.web import URL
from fastapi import APIRouter
from ... import Users

apiURL = URL('https://philh.myftp.biz:8000/Server/Users/')

# Declare FastAPI router
router = APIRouter(
    prefix = '/Server/Users'
)

link_line = '<a href="{}">{}</a> <br>'.format

@router.get("/open")
async def _(
    username: str, 
    path: str
):
    
    url = apiURL.child('open')

    url.params = {
        'username': username
    }

    _path = Users.child(f'/philh/{username}/Website{path}')

    if path[-1] != '/':
        path += '/'

    if _path.is_dir:

        _html = f"<html> <body> <h1>{username}/Website{path}</h1>".replace('//', '/')

        if path == '/':

            _html += link_line("https://philh.myftp.biz/Server/Users/Share.html", '...')

        else:

            url.params['path'] = path[:path[:-1].rfind('/')+1]

            _html += link_line(url, '...')

        for child in _path.children:

            url.params['path'] = path + child.seg()

            _html += link_line(url, child.seg())

        _html += "</body></html>"

        return HTMLResponse(_html)

    else:
        return FileResponse(_path.path)
