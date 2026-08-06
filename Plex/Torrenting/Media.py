from philh_myftp_biz.web.torrent import Torrent, TorrentFile, thePirateBay
from philh_myftp_biz.functools import loc, attr, cached_property
from philh_myftp_biz.web.torrent import qBitTorrent as qbit
from philh_myftp_biz.web.omdb import EpisodeData, Omdb
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.json import List
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE
from .weights import Weights
from typing import Callable
from . import this

class MediaItem:

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    weights: Weights

    @property
    def exists(self) -> bool:
        """Check if the destination file already exists"""
        return any(
            (self.weights(p) and p.size>0) for p in self.dir.children
        )

    @cached_property    
    def _magnets(self) -> list[Torrent]:

        magnets = qbit.queue.filtered(self.weights)

        if len(magnets) == 0:
            magnets = List(filter(
                self.weights,
                thePirateBay.search(*self.queries)
            ))
        
        magnets.sort(lambda m: m.seeders)
        
        return list(magnets.pop(n=3))

    @cached_property
    def magnet(self) -> Torrent | None:

        if len(self._magnets) == 0:
            return

        mag = self._magnets.pop()
        mag.start()

        try:
            VERBOSE.pause()
            [f.stop() for f in mag.files]
            return mag
        except TimeoutError:
            mag.stop()
            return None
        finally:
            VERBOSE.resume()
    
    @cached_property
    def file(self) -> TorrentFile | None:

        while self._magnets and (self.magnet is None):
            del self.magnet

        if self.magnet:

            files = self.magnet.files.copy()
            files.filter(self.weights)
            files.filter(lambda f: f.path.type=='video')

            file = files.max(lambda f: f.size)
            
            if file is not None:
                file.start()
                return file

class Movie(MediaItem):

    dir = this.child('/Media/Movies/')

    def __init__(self,
        title: str,
        year: int
    ) -> None:
        
        self.Title = title
        self.Year = year

        self.queries = [
            title,
            f'{title} {year}'
        ]

        self.omdb = Omdb.movie(title, year)

        self.weights = Weights(
            TITLE = [self.Title],
            YEAR = self.Year,
            UPLOADED = self.omdb.Released
        )

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path, 
            this.child(f"/Media/Movies/{self.Title} ({self.Year}).{self.file.path.ext}")
        )
    
    def __repr__(self) -> str:
        return f'<Movie "{self.Title} ({self.Year})" @{loc(self)}>'

class Show:

    dir = this.child('/Media/Shows/')

    def __init__(self,
        title: str,
        year: int             
    ) -> None:

        self.Title = title
        self.Year = year

        self.dir = Show.dir.child(f"/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        self.omdb = Omdb.show(title, year)

        try:
            self.seasons = [Season(self, *i) for i in self.omdb.Seasons.items()]
        except IndexError:
            self.seasons = []

    @property
    def exists(self) -> bool:
        return all(s.exists for s in self.seasons)

    def __repr__(self) -> str:
        return f'<Show "{self.Title}" @{loc(self)}>'

class Season(MediaItem):

    def __init__(self,
        show: 'Show',
        season: str,
        episodes: dict[str, EpisodeData]
    ) -> None:
        
        self.show: Show = show

        attr(self, '__int__').set(lambda s: int(season))

        self.dir = show.dir.child(f"/Season {self:02d}/")
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        self.dir.mkdir()

        self.queries = [
            self.show.Title,
            f'{self.show.Title} {self.show.Year}',
            f'{self.show.Title} Season {self}',
            f'{self.show.Title} s{self:02d}',
            f'{self.show.Title} s{self}',
            f'{self.show.Title} {self}',
        ]

        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights = Weights(
            TITLE = [self.show.Title],
            SEASON = int(self),
            EPISODE = None,
            YEAR = self.show.Year,
            UPLOADED = show.omdb.Released
        )

    @property
    def exists(self) -> bool:
        return all(e.exists for e in self.episodes)
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Season "{self}" - "{self.show.Title}" @{loc(self)}>'

class Episode(MediaItem):

    def __init__(self,
        season: 'Season',
        episode: EpisodeData
    ) -> None:
        
        super().__init__()

        self.show: Show = season.show
        self.season: Season = season
        self.Title: str = episode.Title

        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        attr(self, '__int__').set(lambda s: episode.Number)

        self.queries = [
            self.show.Title,
            *self.season.queries,
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}'
        ]

        self.weights = Weights(
            TITLE = [self.show.Title, self.Title, None],
            YEAR = self.show.Year,
            SEASON = int(self.season),
            EPISODE = int(self),
            UPLOADED = self.show.omdb.Released
        )

    @cached_property
    def file(self):

        self.magnet = self.season.magnet
        
        return super().file

    @cached_property
    def paths(self) -> tuple[Path, Path]:
        return (
            self.file.path,
            self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{self.file.path.ext}')
        )
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'
