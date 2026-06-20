from philh_myftp_biz.programs import COOKIES, FFMPEG
from fastapi.responses import FileResponse
from philh_myftp_biz.db import MimeType
from philh_myftp_biz.file import temp
from requests import get, head
from fastapi import APIRouter
from yt_dlp import YoutubeDL

# Declare FastAPI router
router = APIRouter(
    prefix = '/Apps/YouTube Downloader'
)

class DownloadItem:

    def __init__(self, 
        ext: str, 
        id: str
    ) -> None:
        
        #==========================

        self.ext:  str = ext
        self.id:   str = id
        self.type: str = MimeType.Ext(ext)
        
        #==========================

        self.outfile = temp('yt-download', ext, id)       

        self.seg = self.outfile.seg()

        #==========================

        self.watch_url = f'https://www.youtube.com/watch?v={id}'

        #==========================
            
        self.ytdl_args = {}

        self.ytdl_args['ffmpeg_location'] = str(FFMPEG())

        self.ytdl_args['cookies'] = str(COOKIES())

        self.ytdl_args['outtmpl'] = str(self.outfile)

        #==========================

    @property
    def thumb_url(self) -> None|str:
        
        reslist = [
            'maxresdefault',
            'hqdefault',
            "sddefault",
            "default"
        ]

        for res in reslist:

            url = f"https://img.youtube.com/vi/{self.id}/{res}.jpg"

            r = head(url, allow_redirects=True)
    
            if r.status_code < 400:

                return url

    def download(self) -> None:

        if self.type in ['video', 'audio']:

            YoutubeDL(self.ytdl_args).download([self.watch_url])

        elif self.type in ['image']:

            content: bytes = get(self.thumb_url).content

            self.outfile.open('wb').write(content)

@router.get('/video')
async def read_item(id:str) -> str:

    dwnld = DownloadItem('mp4', id)

    # Set format to 'video'
    dwnld.ytdl_args['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    # Set ext to 'mp4'
    dwnld.ytdl_args['merge_output_format'] = 'mp4'

    dwnld.download()

    return dwnld.seg

@router.get('/audio')
async def read_item(id:str) -> str:
    
    dwnld = DownloadItem('mp3', id)

    # Set format to 'audio'
    dwnld.ytdl_args['format'] = 'bestaudio/best'

    # Declare Post Processors
    dwnld.ytdl_args['postprocessors'] = [{
        'key': 'FFmpegExtractAudio', # Audio Only
        'preferredcodec': 'mp3', # mp3 codec
        'preferredquality': '192', # 192 kbps
    }]

    dwnld.download()

    return dwnld.seg + '.mp3'

@router.get('/thumbnail')
async def read_item(id:str) -> str:
    
    dwnld = DownloadItem('jpg', id)
    
    dwnld.download()

    return dwnld.seg

@router.get('/file')
async def read_item(name:str):
    return FileResponse(
        path = f'E:/__temp__/{name}',
        filename = name
    )
