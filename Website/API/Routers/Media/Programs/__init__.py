from fastapi.responses import RedirectResponse, FileResponse
from philh_myftp_biz.pc.Path import Path
from fastapi import APIRouter
from typing import Literal
from . import items

systems = 'Windows', 'MacOS', 'Linux'

router = APIRouter(
    prefix = '/Media/Programs'
)

@router.get('/list')
def _(
    os: Literal[*systems]
) -> list[str]:
    
    programs: list[str] = []
    
    for name, obj in vars(items).items():

        if hasattr(obj, os):

            programs += [name]

    return sorted(programs)

@router.get('/get', response_model=None)
def _(
    name: str,
    os: Literal[*systems]
) -> RedirectResponse | FileResponse:

    program = getattr(items, name) ()
    item: str|Path = getattr(program, os)

    if isinstance(item, Path):
        return FileResponse(item.path)
    elif isinstance(item, str):
        return RedirectResponse(item)

