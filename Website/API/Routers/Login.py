from typing import Literal, Callable
from fastapi import APIRouter
from .. import User

router = APIRouter(
    prefix = '/login'
)

responseT = dict[Literal['Valid', 'Alert', 'Token'], str|bool|None]

response: Callable[[], responseT] = {
    'Valid': False,
    'Alert': None,
    'Token': None
}.copy

@router.get("/change")
async def read_item( # pyright: ignore[reportRedeclaration]
    username: str,
    password: str,
    newpassword: str
) -> responseT:
    """Change the Active Directory Password of a user"""   

    r = response()

    user = User(username)

    if user.checkPass(password):

        user.setPass(newpassword)

        r['Valid'] = True
        r['Alert'] = "Password has been reset"
        r['Token'] = user.resetAuth()

    else:

        r['Alert'] = "Existing Password Incorrect"

    return r

@router.get("/create")
async def read_item( # pyright: ignore[reportRedeclaration]
    username: str,
    password: str
) -> responseT:
    """Create an Active Directory User"""

    r = response()

    user = User(username)

    if user.exists:
        r['Alert'] = "User already exists"

    else:

        r['Valid'] = True
        r['Alert'] = ""
        r['Token'] = user.resetAuth()
        
        user.create(password)
        
    return r
    
@router.get("/check")
async def read_item( # pyright: ignore[reportRedeclaration]
    username: str,
    password: str
) -> responseT:
    """Check if a User's Password is correct"""
    
    user = User(username)

    r = response()

    # Check if user exists
    if not user.exists:
        r['Alert'] = 'Username not found'

    # Check if password is correct
    elif user.checkPass(password):
        r['Valid'] = True
        r['Token'] = user.resetAuth()

    # Check if password is incorrect
    else:
        r['Alert'] = 'Password is incorrect'
 
    return r
    
@router.get("/auth")
async def read_item(
    username: str,
    token: str
) -> responseT:
    """Check if a User's Auth Token is valid """

    user = User(username)

    r = response()

    # Check if user exists
    if not user.exists:
        r['Alert'] = 'This page requires you to login'

    # Check if token is correct
    elif user.checkAuth(token):
        r['Valid'] = True

    # Check if token is incorrect
    else:
        r['Alert'] = 'Credentials Expired'
 
    return r
