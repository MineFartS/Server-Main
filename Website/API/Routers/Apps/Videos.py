from ... import User, receiveFile, root, FormStr
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, UploadFile
from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import JSON
from philh_myftp_biz.pc import Path

router = APIRouter(
    prefix = '/Apps/Videos'
)

class VideoObj(Dict):

    def __init__(self,
        id: str
    ) -> None:
        
        #==================================================================
        
        self.dir = Path(f'E:/Website/Root/Apps/Videos/files/{id}/')

        self.url = f"https://philh.myftp.biz/Apps/Videos/Player?id={id}"

        self.videoP = self.dir.child('video.mp4')

        self.thumbP = self.dir.child('thumb.jpg')

        #==================================================================
        
        _json = JSON(self.dir.child('video.json'))
        super().__init__(_json)

        self['id'] = id

        #==================================================================

@router.post('/Upload')
async def upload( 
    username: FormStr,
    token: FormStr,
    Title: FormStr,
    Video: UploadFile,
    Thumbnail: UploadFile,
    Description: FormStr = '',
):
    """
    Upload a video

    Thumbnail will be automatically generated if not given
    """
    from philh_myftp_biz.text import random
    from philh_myftp_biz.time import now

    user = User(username)

    if user.checkAuth(token):

        vid = VideoObj(random(10))

        await receiveFile(Video, vid.videoP)
        
        if len(Thumbnail.filename) > 0:
            # TODO handle invalid image formats
            await receiveFile(Thumbnail, vid.thumbP)
        else:
            # TODO Generate Thumbnail
            Thumbnail = None

        vid["Title"] = Title,
        vid["Description"] = Description,
        vid["Timestamp"] = now().unix,
        vid["Uploader"] = username,
        vid["Views"] = 0
    
        return RedirectResponse(vid.url)

@router.get('/List')
async def read_item( 
    username: None|str = None,
    token: None|str = None
) -> list[dict]:
    """
    List All Videos

    If Username and Auth Token are valid, then the user's private videos will be included
    """
    
    if username:
        user = User(username)
        show_private = user.checkAuth(token)
    else:
        show_private = False

    items = []
    
    for p in root.child('/Apps/Videos/files/').children:

        if p.is_dir:

            vid = VideoObj(p.name)
            
            if vid['Visibility'] == 'Public':
                visible = True
            
            elif show_private:
                visible = (vid['Uploader'] == username)
            
            else:
                visible = False

            if visible:
                items += [vid['id']]

    return items

@router.get('/View')
async def read_item(
    ID: str,
    count: bool = True
) -> str:
    """
    Get the details of a video

    If c, then add 1 view
    """

    vid = VideoObj(ID)

    if count:
        vid['Views'] += 1

    return vid['id'] # pyright: ignore[reportReturnType]
