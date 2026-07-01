from philh_myftp_biz.gui import Window, Widget
from plexapi.exceptions import Unauthorized
from plexapi.myplex import PlexServer
from philh_myftp_biz.db import Ring

_ring = Ring('Plex')
token = _ring.Key('token')

try:
    plex_server = PlexServer("http://127.0.0.1:32400", token.read())

except Unauthorized:

    gui = Window()
    gui.title = 'Plex Metadata Config'

    page = gui.Page()
    page += Widget.Input('X-Plex-Token', key=token)
    page += Widget.Button('Save', gui.close)
    page += Widget.Link('Find Token', "https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/")

    gui.page = page

    gui.run()

    plex_server = PlexServer("http://127.0.0.1:32400", token.read())

