from .World import Worlds
from . import args

if args['force']:
    processes = [w._start() for w in Worlds]
else:
    processes = [w.start() for w in Worlds]

# Wait for all subprocesses to complete
for process in processes:
    
    process.wait()
