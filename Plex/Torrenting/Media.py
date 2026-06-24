from philh_myftp_biz.web.torrent import Torrent, TorrentFile, Magnet, thePirateBay
from philh_myftp_biz.web.omdb import EpisodeData, Omdb
from philh_myftp_biz.functools import loc, attr
from philh_myftp_biz.json.List import List
from philh_myftp_biz.terminal import Log
from functools import cached_property
from philh_myftp_biz.pc import Path
from .weights import WEIGHTS
from typing import Callable
from . import this, qbit

class MediaItem:

    magnet: None|Magnet = None

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    @cached_property
    def weights(self) -> WEIGHTS:
        w = WEIGHTS()
        self.valid = w.parse
        return w

    def start(self) -> None:
        """Search thepiratebay.org and start the download"""

        # Search thePirateBay for magnets
        magnets: List[Torrent] = thePirateBay.search(*self.queries)

        # Get torrents already in the download queue
        magnets.extend(qbit.queue)

        # Remove magnets with invalid names
        magnets.filter(lambda m: self.valid(m.name))

        # Select the most seeded magnet
        self.magnet = magnets.max(lambda m: m.seeders)

        if self.magnet:

            Log.VERB(
                f'Found: {self=}\n'+ \
                f'{self.magnet.name=}\n'+ \
                f'{self.magnet.seeders=}'
            )

            if not self.magnet.exists:
                try:
                    self.magnet.start()
                    self.magnet.wait()
                    [f.stop() for f in self.magnet.files]
                except TimeoutError:
                    Log.FAIL('', exc_info=True)

    @cached_property
    def exists(self) -> bool:
        """Check if the destination file already exists"""
        return any(
            (self.valid(p.name) and p.type=='video') for p in self.dir.children
        )
    
    @cached_property
    def file(self) -> TorrentFile | None:
        if self.magnet:
            files = self.magnet.files.copy()
            files.filter(lambda m: self.valid(m.name))
            return self.magnet.files.max(lambda f: f.size)

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

        self.weights['TITLE'] = self.Title
        self.weights['YEAR'] = self.Year

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

        self.seasons = [Season(self, *i) for i in Omdb.show(title, year).Seasons.items()]

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
            f'{self.show.Title} Season {self}',
            f'{self.show.Title} s{self:02d}',
            f'{self.show.Title} s{self}',
        ]

        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights['TITLE'] = self.show.Title
        self.weights['SEASON'] = int(self)
        self.weights['EPISODE'] = None
        self.weights['YEAR'] = self.show.Year

    @cached_property
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

        self.show: Show = season.show
        self.season: Season = season
        self.Title: str = episode.Title

        self.dir = season.dir
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        attr(self, '__int__').set(lambda s: episode.Number)

        self.queries = [
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}'
        ]

        self.weights['TITLE'] = [self.show.Title, self.Title, None]
        self.weights['YEAR'] = self.show.Year
        self.weights['SEASON'] = int(self.season)
        self.weights['EPISODE'] = int(self)

    def start(self) -> None:

        self.magnet = self.season.magnet

        # Search again if no file was found in the season
        if self.file is None:
            del self.file
            super().start()

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
