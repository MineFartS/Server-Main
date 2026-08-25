from philh_myftp_biz.terminal import Args, cls
from philh_myftp_biz.modules import Module
from philh_myftp_biz import json, HELP
from typing import Literal, NoReturn
from philh_myftp_biz.pc import Path

# ====================================================

this = Module('E:/AI/')

# ====================================================
# PARSE INPUT

Args.Arg(
    name = 'messages',
    handler = json.loads
)

Args.Arg(
    name = 'prompt'
)

# ====================================================

class Messages(list[dict[Literal['kind', 'role', 'content'], str]]):

    def __init__(self,
        messages: list[dict[str, str]] = []
    ) -> None:
        
        super().__init__()

        self += messages

    def add_text(self,
        role: Literal['user', 'assistant'],
        content: str
    ) -> None:
        self += [{
            'kind': 'text',
            'role': role,
            'content': content
        }]

    def add_file(self,
        role: Literal['user', 'assistant'],
        path: Path
    ) -> None:
        self += [{
            'kind': 'file',
            'role': role,
            'content': str(path)
        }]
    
    def output(self) -> NoReturn:
        
        # Clear the Terminal Window
        cls()

        data = json.dumps(self)

        # Print the messagees
        print(data)

        # Stop the execution
        exit()

    def prompt(self) -> None | str:

        lmessage = self[-1]

        if lmessage['role'] == 'user':
            
            return lmessage['content']

# ====================================================
# PARSE MESSAGES

# Do nothing if '-h' is passed
if HELP:
    messages = None

elif Args['messages']:
    messages = Messages(Args['messages'])

elif Args['prompt']:
    messages = Messages()
    messages.add_text('user', Args['prompt'])

else:
    raise Exception('No prompt or messages given')

# ====================================================