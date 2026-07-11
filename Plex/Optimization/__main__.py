from ffmpeg_progress_yield import FfmpegProgress
from philh_myftp_biz.programs import FFMPEG
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.terminal import Args
from philh_myftp_biz.file import temp
from philh_myftp_biz.pc import Path
from tqdm import tqdm

pbar = tqdm(
    position = 1,
    total = Args['limit'],
    desc = "Encoding"
)

for src in Path('E:/Plex/Media/').descendants:

    if pbar.finished: break
    if (src.type != 'video') or (src.ext == 'mp4'): continue

    dst = src.with_ext('mp4')
    tmp = temp('encoding', 'mp4')

    pbar.reset()

    try:

        ff = FfmpegProgress([
            FFMPEG().path, # Ffmpeg.exe
            '-hwaccel', 'cuda', # Use GPU
            '-i', src.path, # Input Path
            '-c:v', 'h265_nvenc', # Video Codec
            '-c:a', 'aac', # Audio Codec
            tmp.path, # Output Path
        ])

        for progress in ff.run_command_with_progress():
            pbar.update(progress - pbar.n)
        
        tmp.move(dst)
        src.delete()

    except RuntimeError:
        Log.FAIL(exc_info=True)

