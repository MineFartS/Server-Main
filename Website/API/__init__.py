from philh_myftp_biz.file import JSON, temp
from philh_myftp_biz.modules import Module
from philh_myftp_biz.text import random
from philh_myftp_biz.array import List
from fastapi import UploadFile, Form
from philh_myftp_biz.pc import Path
from philh_myftp_biz.db import Ring
from typing import Annotated
from aiofiles import open

# ================================================================================================================

this = Module('E:/Website')
Users = Module('E:/Users')

root = this.child('Root')

tokenRing = Ring('AuthTokens')

PIDstore: List[int] = List(JSON(this.child('/API/__pycache__/PID.json')))

# ================================================================================================================

FormStr = Annotated[str, Form()]

async def receiveFile(
    stream: 'UploadFile',
    dst: None|Path = None
) -> Path:

    if dst is None:
        dst = temp(
            name = 'UploadedFile',
            ext = stream.filename[stream.filename.rfind('.')+1:]
        )

    contents = await stream.read()

    async with open(dst.path, 'wb') as f:
        await f.write(contents)

    return dst

# ================================================================================================================

class User:

    def __init__(self, username:str):
        
        self.username = username
        self.Dir = Path(f'E:/Users/philh/{username}/__AppData__/')

        self.__token = tokenRing.Key(username)

    def checkPass(self, password:str):
        return Users.run(
            'CheckPass',
            '-Username', self.username,
            '-Password', password
        ).output('json')
    
    def create(self, password:str):
        Users.run(
            'Create',
            '-Username', self.username,
            '-Password', password
        )

    def setPass(self, password:str):
        Users.run(
            'SetPass',
            '-Username', self.username,
            '-Password', password
        )

    @property
    def exists(self) -> bool:
        return Users.run(
            'Exists',
            '-Username', self.username
        ).output('json') # pyright: ignore[reportReturnType]

    def checkAuth(self, token:str):
        return (self.__token.read() == token)

    def resetAuth(self) -> str:
        token = random(10)
        self.__token.save(token)
        return token

# ================================================================================================================
