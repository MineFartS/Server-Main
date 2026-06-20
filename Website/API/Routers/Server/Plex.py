from philh_myftp_biz.modules import Service
from philh_myftp_biz.pc import Path
from fastapi import APIRouter
from typing import Literal

# Declare FastAPI router
router = APIRouter(
    prefix = '/Server/Plex'
)

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
    
    # Name of the movie file
    name = f'{Title} ({Year})'
    
    # If the media type is a show
    if Type == 'series':
        
        # Show Folder
        dir = shows.child(f'/{name}/')

        # If the folder already exists
        if dir.exists:
            
            mess =  'Show already exists'
        
        # If the folder does not exist
        else:
            
            # Create the folder
            dir.mkdir()
            
            mess =  'Show has been added to the download queue'

    # If the media type is a movie
    elif Type == 'movie':

        # Iter through all movie files
        for p in movies.children:
            
            # If the file has the same name as the movie
            if p.name == name:
                
                mess = 'Movie already exists'
            
        # Path of Placeholder file
        todo = movies.child(f'/{name}.todo')

        # If the placeholder file exists
        if todo.exists:
            
            mess = 'Movie is already in the download queue'
        
        # If the placeholder file does not exist
        else:
            
            # Create the placeholder file
            todo.open('w')
            
            mess = 'Movie has been added to the download queue'

    if not Torrenting.running:
        Torrenting.start()

    return mess