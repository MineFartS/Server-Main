from philh_myftp_biz.modules import Service
from philh_myftp_biz.pc import Path
from fastapi import APIRouter
from typing import Literal
import sys

# Declare FastAPI router
router = APIRouter(
    prefix = '/Server/Plex'
)

#===========================
pr = 'E:/Plex/'
if pr not in sys.path:
    sys.path.append(pr)
from Torrenting.Media import Show
from Torrenting.__init__ import driver
driver.close()
#===========================

Torrenting = Service('E:/Plex/Torrenting/')

movies = Path('E:/Plex/Media/Movies/')
shows = Path('E:/Plex/Media/Shows/')

@router.get('/download')
async def read_item(
    Title: str,
    Year: int,
    Type: Literal['movie', 'series']
) -> str:
    
    mess = "An unknown error has occurred"
    name = f'{Title} ({Year})'
    
    if Type == 'series':
        
        dir = shows.child(f'/{name}/')

        if dir.exists:
            s = Show(Title, Year)
            p = sum(1 for e in s.episodes if e.exists) / len(s.episodes)

            mess = f'Show is {p:.1%} downloaded'

        else:
            dir.mkdir()
            mess = 'Show has been added to the download queue'

    elif Type == 'movie':

        for p in movies.children:
            if p.name == name:
                mess = 'Movie already exists'
                break
            
        todo = movies.child(f'/{name}.todo')

        if todo.exists:    
            mess = 'Movie is already in the download queue'
        else:
            todo.open('w').close()
            mess = 'Movie has been added to the download queue'

    if Torrenting.enabled and not Torrenting.running:
        Torrenting.args = ['--filter', name]
        Torrenting.start()

    return mess

