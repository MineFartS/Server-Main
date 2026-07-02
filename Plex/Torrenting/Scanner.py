from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.functools import singleton
from philh_myftp_biz.text import contains
from philh_myftp_biz.terminal import Log
from typing import Generator, Type
from . import Media, this

def get[T](dir, clazz:Type[T]):

    for c in this.child(f'/Media/{dir}/').children:

        if not contains.any(c.name, ParsedArgs['filter']):
            continue

        name = c.name.split(' (')[0]
        
        year = int(c.name.split('(')[1].split(')')[0])

        yield c, clazz(name, year)

@singleton
def Missing() -> Generator[Media.Movie | Media.Episode]:

    #==========================================================

    for c, movie in get('Movies', Media.Movie):

        if movie.exists:
            Log.INFO(f'Movie Exists\n{movie.Title=}\n{movie.Year=}')
        else:
            Log.WARN(f'Movie Missing\n{movie.Title=}\n{movie.Year=}')
            movie.finish = c.delete
            yield movie

    #==========================================================

    for c, show in get('Shows', Media.Show):

        Log.VERB(f'Scanning Show\n{show=}')

        for season in show.seasons:

            if season.exists:
                Log.INFO(f'Season Exists\n{show=}\n{season=}')
            
            else:

                try:
                    season.file
                except TimeoutError:
                    Log.FAIL('', exc_info=True)

                for episode in season.episodes:

                    if episode.exists:
                        Log.INFO(f'Episode Exists\n{show=}\n{season=}\n{episode=}')

                    else:
                        Log.WARN(f'Episode Missing\n{show=}\n{season=}\n{episode=}')
                        yield episode

    #==========================================================