from fastapi.responses import RemoteFileResponse, FileResponse
from philh_myftp_biz.pc.Path import Path
from fastapi import APIRouter
from typing import Literal
from . import items

OS = Literal['Windows', 'MacOS', 'Linux']

router = APIRouter('/Media/Programs')

cache: dict[tuple[str, str], str|Path] = {}

@router.get('/list')
def _(os: OS) -> list[str]:
    
    programs: list[str] = []
    
    for name, obj in vars(items).items():

        if hasattr(obj, os):

            programs += [name]

    return sorted(programs)

@router.get('/get', response_model=None)
def _(name: str, os: OS) -> RemoteFileResponse | FileResponse:

    if (key := (name, os)) not in cache:
        program = getattr(items, name) ()
        cache[key] = getattr(program, os)

    item: str|Path = cache[key]

    if isinstance(item, Path):
        return FileResponse(item.path)
    
    elif isinstance(item, str):        
        return RemoteFileResponse(item, name)

