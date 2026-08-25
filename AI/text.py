from philh_myftp_biz.terminal import set_package, Args
set_package('E:/AI/')

from philh_myftp_biz.modules import Service
from ollama import pull, chat, ChatResponse
from philh_myftp_biz.terminal import Log
from typing import Iterator
from . import messages

OllamaServ = Service('E:/AI/Ollama/')
ollama = Client('http://127.0.0.1:11434')

# ====================================================
# MODEL

Args.Arg(
    name = 'model',
    default = 'llama3'
)

if not OllamaServ.running:

    OllamaServ.start()

Log.VERB(f'Pulling Model: {Args['model']}')

# Download & install the model
pull(args['model'])

# ====================================================
# HANDLE RESPONSE

Log.VERB(f'Sending Messages to Model')

stream: Iterator[ChatResponse] = chat(
    model = Args['model'],
    messages = messages,
    stream = True
)

content = ''

for chunk in stream:

    content += chunk.message.content
    
    Log.VERB(f'Response: {content}')

messages.add_text(
    role = 'assistant', 
    content = content
)

# ====================================================

messages.output()
