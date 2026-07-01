from philh_myftp_biz.terminal import ParsedArgs, Log, ProgressBar
from philh_myftp_biz.web.omdb import MediaNotFoundError
from philh_myftp_biz.web.torrent import qBitTorrent
from . import VM, driver, PIDstore, Media
from .Scanner import Missing
from time import sleep
from os import getpid

# ===============================================================

queue: list[Media.Movie|Media.Episode] = []

qBitTorrent.clear(rm_files=False)

# ===============================================================

while True:

    try:

        d = next(Missing)

        d.start()

        if d.file:

            Log.INFO(f'Downloading File: {d=}')

            d.file.start()
            queue += [d]

        else:
            Log.VERB(f'Magnet Not Found: {d=}')

    except TimeoutError, MediaNotFoundError, ValueError:
        Log.FAIL('', exc_info=True)
        continue

    except StopIteration, ConnectionAbortedError:
        Log.WARN(exc_info=True)
        break

    # Break the loop if the queue limit has been reached
    if len(queue) >= ParsedArgs['limit']:
        Log.WARN('Download Limit Reached')
        break

# ===============================================================

PIDstore.save([f'python-{getpid()}'])

driver.close()

Log.INFO(f'Waiting for downloads: {len(queue)=}')

# ===============================================================

pbar = ProgressBar(
    queue, 
    mode = 'FCOUNTER',
    label = 'Torrents'
)

while len(queue) > 0:

    sleep(1)

    # Clear queue items that have nothing selected
    qBitTorrent.clear(True, lambda t: len(t.enabled_files)==0)

    # Sort queue by seeders (most seeded first)
    qBitTorrent.sort(lambda t: t.seeders)

    for d in queue:

        if d.file.finished:

            try:

                Log.INFO(f'Download Complete: {d=}')
                
                src, dst = d.paths

                src.copy(dst)

                Log.INFO(f'Copy Complete: {d=}')

                d.finish()

                pbar.step()

                d.file.stop()

                queue.remove(d)

            except FileNotFoundError, OSError, TypeError:
                Log.WARN(exc_info=True)
                d.magnet.recheck()

        elif d.magnet.errored:
            d.magnet.start()

# ===============================================================

VM.runH('Save', 'Torrenting')
