from philh_myftp_biz.terminal import Log, cls, ProgressBar
from philh_myftp_biz.programs import FFMPEG
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.process import Run
from philh_myftp_biz.file import temp
from philh_myftp_biz.pc import Path

pbar = ProgressBar( Args['limit'] )

for src in Path('E:/Plex/Media/').descendants:

    if pbar.finished: break
    if (src.type != 'video') or (src.ext == 'mp4'): continue

    cls()

    dst = src.with_ext('mp4')
    tmp = temp(src.name, 'mp4')

    Log.INFO(f'Encoding:\n{src=}\n{dst=}\n{tmp=}')

    Run([
        FFMPEG(),
        '-hwaccel', 'cuda',
        '-i', src,
        '-c:v', 'h265_nvenc',
        '-c:a', 'aac',
        tmp
    ])

    
    tmp.move(dst)
    src.delete()

    pbar.step()
