from philh_myftp_biz.functools import singleton
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.text import contains
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import Path
from typing import Generator, Type
from . import Media

def children[T](dir, clazz:Type[T]):

    for path in Path(f'E:/Plex/Media/{dir}/').children:

        if contains.any(path.name, Args['filter']):
            try:

                item = clazz(
                    title = path.name.split(' (')[0],
                    year = int(path.name.split('(')[1].split(')')[0])
                )

                if path.is_file:
                    item.finish = path.delete

                yield item

            except IndexError:
                Log.FAIL(exc_info=True)

def notexists[T](items:list[T]) -> filter[T]:
    return filter(lambda e: not e.exists, items)

@singleton
def Missing() -> Generator[Media.Movie | Media.Episode]:

    #==========================================================

    yield from notexists(children('Movies', Media.Movie))

    #==========================================================

    for show in notexists(children('Shows', Media.Show)):

        for season in notexists(show.seasons):
            season.start()
            yield from notexists(season.episodes)

    #==========================================================