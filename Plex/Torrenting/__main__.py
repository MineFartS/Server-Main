from philh_myftp_biz.terminal import ParsedArgs, Log, ProgressBar
from philh_myftp_biz.web.omdb import MediaNotFoundError
from . import qbit, VM, driver, PIDstore, Media
from .Scanner import Missing
from time import sleep
from os import getpid

# ===============================================================

queue: list[Media.Movie|Media.Episode] = []

qbit.clear(rm_files=False)

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

    except TimeoutError, MediaNotFoundError:
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

pbar = ProgressBar(queue, label='Torrents')

while len(queue) > 0:

    sleep(1)

    # Clear queue items that have nothing selected
    qbit.clear(True, lambda t: len(t.enabled_files)==0)

    # Sort queue by seeders (most seeded first)
    qbit.sort(lambda t: t.seeders)

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

            except FileNotFoundError, OSError:
                d.magnet.recheck()

        elif d.magnet.errored:
            d.magnet.start()

# ===============================================================

VM.runH('Save', 'Torrenting')
