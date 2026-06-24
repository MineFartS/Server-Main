from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.functools import singleton
from philh_myftp_biz.text import contains
from philh_myftp_biz.terminal import Log
from typing import Generator
from . import Media

def _FILTER(name:str):
    return (ParsedArgs['filter']=='') or contains.any(name, ParsedArgs['filter'])

def ReadName(name) -> tuple[str, int]:
    """'Test (2025)' -> 'Test', 2025"""
    return (
        name.split(' (')[0],
        int(name.split('(')[1].split(')')[0])
    )

@singleton
def Missing() -> Generator[Media.Movie|Media.Episode]:

    #==========================================================

    for p in Media.Movie.dir.children:

        if _FILTER(p.name) and (p.size == 0):

            movie = Media.Movie(*ReadName(p.name))

            movie.finish = p.delete

            if movie.exists:
                Log.INFO(f'Movie Exists\n{movie.Title=}\n{movie.Year=}')
            else:
                Log.WARN(f'Movie Missing\n{movie.Title=}\n{movie.Year=}')
                yield movie

    #==========================================================

    for ShowDir in Media.Show.dir.children:

        if not _FILTER(ShowDir.name): 
            continue

        show = Media.Show(*ReadName(ShowDir.name))

        Log.VERB(f'Scanning Show\n{show=}\n{ShowDir=}')

        for season in show.seasons:

            if season.exists:
                Log.INFO(f'Season Exists\n{show=}\n{season=}')
            
            else:
                
                try: season.start()
                except TimeoutError: Log.FAIL('', exc_info=True)

                for episode in season.episodes:

                    if episode.exists:
                        Log.INFO(f'Episode Exists\n{show=}\n{season=}\n{episode=}')

                    else:
                        Log.WARN(f'Episode Missing\n{show=}\n{season=}\n{episode=}')
                        yield episode

    #==========================================================