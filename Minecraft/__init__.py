from philh_myftp_biz.terminal import ParsedArgs
from philh_myftp_biz.process import SubProcess
from philh_myftp_biz.modules import Module
from philh_myftp_biz.json import Dict

version = "26.1"

#============================================================

# Minecraft Module
this = Module('E:/Minecraft/')

java_exe = this.child('/.java/bin/java.exe')

#============================================================

# Parsed Command Line Arguements
args = ParsedArgs()

args.Arg(
    name = 'world',
    desc = 'Select Specific World'
)

args.Flag(
    name = 'force',
    letter = 'f'
)

#============================================================

Tasks: Dict[SubProcess] = this.child('/__pycache__/Tasks.pkl').PKL.Dict

#============================================================
