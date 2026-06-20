from fastapi.responses import RedirectResponse
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

@router.get('/get')
def _(
    name: str,
    os: Literal[*systems]
) -> str:

    program = getattr(items, name) ()

    url: str = getattr(program, os)

    return RedirectResponse(url)

