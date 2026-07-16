from plexapi.exceptions import Unauthorized
from plexapi.myplex import PlexServer
from philh_myftp_biz.db import Ring

ring = Ring('Plex')
token = ring.Key('X-Plex-Token')

try:
    plex_server = PlexServer("http://127.0.0.1:32400", token.read())

except Unauthorized:

    token.prompt(secure=False)

    plex_server = PlexServer("http://127.0.0.1:32400", token.read())

