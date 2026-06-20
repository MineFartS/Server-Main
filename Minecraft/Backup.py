from philh_myftp_biz.modules import Repo
from philh_myftp_biz.terminal import Log

repo = Repo('E:/')
repo.focus('/Minecraft/Worlds/')

Log.INFO('Tracking Files')

filecount = len(repo.diff(repo.head.commit))

if filecount == 0:
    Log.WARN('No Modified Files Found')
    
else:

    Log.INFO(f'{filecount} Modified Files Found')

    Log.INFO('Committing')
    new_commit = repo.commit(
        message = f"Minecraft World Backup",
        skip_hooks = True,
    )
