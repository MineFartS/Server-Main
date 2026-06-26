from philh_myftp_biz.web import FirewallException
from philh_myftp_biz.terminal import Log
from importlib import import_module
from . import this, PIDstore
from fastapi import FastAPI
from os import getpid

#=======================================================================

#FirewallException('Uvicorn').set(8000)

PIDstore.save([getpid()])

#=======================================================================
# APP

app = FastAPI()

app.set_favicon(this.child('/Root/_/main.ico'))

#=======================================================================
# ROUTERS

for file in this.child('/API/Routers/').descendants:

    if file.ext == 'py':

        imp: str = file.path
        imp = imp.split('/API/')[1]
        imp = imp.split('.')[0]
        imp = imp.replace('/', '.')
        imp = '.' + imp

        try:

            module = import_module(
                name = imp, 
                package = __package__
            )

            app.include_router(module.router)

            Log.VERB(f'Installed Router: {imp}')

        except AttributeError:
            pass

#=======================================================================

Log.INFO('Uvicorn Service Started')

app.run(
    ssl_certfile = this.file('certificates/cert'),
    ssl_keyfile = this.file('certificates/key'),
    log_level = "critical"
)

#=======================================================================