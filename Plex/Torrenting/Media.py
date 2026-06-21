from philh_myftp_biz.web.torrent import Torrent, TorrentFile, Magnet, thePirateBay
from philh_myftp_biz.web.omdb import EpisodeData, Omdb
from philh_myftp_biz.classtools import loc, attr
from philh_myftp_biz.json.List import List
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.db import MimeType
from functools import cached_property
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE
from .weights import WEIGHTS
from typing import Callable
from . import this, qbit

class MediaItem:

    weights: WEIGHTS

    magnet: None|Magnet = None

    queries: list[str]
    """List of queries for the pirate bay"""

    paths: tuple[Path, Path]
    """Get the source and destination paths of the file"""

    finish: Callable[[], None] = lambda s: None
    """tasks to run after the download is complete"""

    dir: Path
    """Parent Folder"""

    def start(self) -> None:
        """Search thepiratebay.org and start the download"""

        # Search thePirateBay for magnets
        magnets: List[Magnet|Torrent] = thePirateBay.search(*self.queries)

        # Get torrents already in the download queue
        magnets.extend(qbit.queue)

        # Remove magnets with invalid names
        magnets.filter(lambda m: self.valid(m.name))

        # Select the most seeded magnet
        self.magnet = magnets.max(func=lambda m: m.seeders)

        # If a magnet has been found
        if self.magnet:

            Log.VERB(
                f'Found: {self=}\n'+ \
                f'{self.magnet.name=}\n'+ \
                f'{self.magnet.seeders=}'
            )

            if not self.magnet.exists:

                # Download the magnet
                self.magnet.start()

                # Stop all files in the magnet
                [f.stop() for f in self.magnet.files]

    @property
    def exists(self) -> bool:
        """Check if the destination file already exists"""

        VERBOSE.pause()

        # Iter through all items in the folder
        for p in self.dir.children:

            # If the file has a valid name
            if self.valid(p):

                VERBOSE.resume()

                return True
            
        VERBOSE.resume()
            
        return False

    def valid(self,
        item: str | Path
    ) -> bool:
        
        if isinstance(item, str):
            return self.weights.parse(item)
        
        else:

            # If the mimetype of the file is 'video' or 'ignore'
            TYPE = (MimeType.Path(item) in ['video', 'ignore'])

            # If the name of the file is valid
            NAME = self.weights.parse(item.name)

            return (TYPE and NAME)
    
    @cached_property
    def file(self) -> TorrentFile | None:
        """File Instance"""
        
        if self.magnet:

            files: list[TorrentFile] = list(filter(
                lambda m: self.valid(m.path),
                self.magnet.files
            ))

            if len(files) > 0:

                return max(
                    files,
                    key = lambda m: m.size
                )

class Movie(MediaItem):

    dir = this.child('/Media/Movies/')

    def __init__(self,
        title: str,
        year: int,
        todo: Path = None
    ) -> None:
        
        self.Title = title
        self.Year = year

        self.__todo = todo

        self.queries = [
            title,
            f'{title} {year}'
        ]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = self.Title
        self.weights['YEAR'] = self.Year

    @property
    def paths(self):

        # The source file
        src = self.file.path

        # The destination file path
        dst = this.child(f"/Media/Movies/{self.Title} ({self.Year}).{src.ext}")

        return src, dst

    def finish(self):

        # If a todo/placeholder file was passed during initialization
        if self.__todo:

            # Delete the placeholder file
            self.__todo.delete()

    def __repr__(self):
        return f'<Movie "{self.Title} ({self.Year})" @{loc(self)}>'

class Show:

    def __init__(self,
        title: str,
        year: int             
    ) -> None:

        self.Title = title
        self.Year = year

        self.dir = this.child(f"/Media/Shows/{title} ({year})/")
        """../Media/Shows/{Title} ({Year})/"""

        # List of 'Season' OBJs
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

        # Destination File Directory
        self.dir = show.dir.child(f"/Season {self:02d}/")
        """E:/Plex/Media/Shows/{Show}/Season {Season}/"""

        # Create the folder if it doesn't exist
        self.dir.mkdir()

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} Season {self}',
            f'{self.show.Title} s{self:02d}',
            f'{self.show.Title} s{self}',
        ]

        # List of 'Episode' OBJs
        self.episodes = [Episode(self, i[1]) for i in episodes.items()]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = self.show.Title
        self.weights['SEASON'] = int(self)
        self.weights['EPISODE'] = None
        self.weights['YEAR'] = self.show.Year

    @property
    def exists(self) -> bool:
        
        # Iter through all episodes this season
        for episode in self.episodes:

            # If the episode does not exist
            if not episode.exists:
                
                return False
            
        return True
    
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

        # Integer Function
        attr(self, '__int__').set(lambda s: episode.Number)

        # List of TPB queries
        self.queries = [
            f'{self.show.Title} s{season:02d}e{self:02d}',
            f'{self.show.Title} {season:02d}x{self:02d}',
            f'{self.show.Title} {season}{self:02d}'
        ]

        self.weights = WEIGHTS()
        self.weights['TITLE'] = [self.show.Title, self.Title]
        self.weights['YEAR'] = self.show.Year
        self.weights['SEASON'] = int(self.season)
        self.weights['EPISODE'] = int(self)

    def start(self) -> None:

        self.magnet = self.season.magnet

        # If no file was found in the season magnet
        if self.file is None:

            # Start downloading the episode
            super().start()

    @property
    def paths(self) -> tuple[Path, Path]:

        # The source file
        src = self.file.path
        
        # The destination file path
        dst = self.dir.child(f'/Season {self.season:02d} Episode {self:02d}.{src.ext}')

        return src, dst
    
    def __format__(self, format_spec:str) -> str:
        return f'{int(self):{format_spec}}'
    
    def __repr__(self) -> str:
        return f'<Episode "{self.season}x{self}" - "{self.show.Title}" @{loc(self)}>'

type DOWNLOAD = Movie|Episode
