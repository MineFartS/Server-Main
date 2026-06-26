from philh_myftp_biz.pc import Path

Movies = Path('E:/Plex/Media/Movies/')
Shows = Movies.sibling('/Shows/')

for f in Movies.children:
    f.open('w').close()

for f in Shows.descendants:

    if f.is_file and not f.in_use:

        print(f)

        f.delete()
