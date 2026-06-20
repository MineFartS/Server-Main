from philh_myftp_biz.modules import Module
from philh_myftp_biz.file import TXT
from os import getpid
from philh_myftp_biz.array import List
from philh_myftp_biz.file import JSON
from philh_myftp_biz.pc import Path
# ================================================================================================================
# INIT

this = Module('E:/Website')

root = this.child('Root')

# ================================================================================================================
# PID

PIDstore = TXT(this.child('/Indexer/__pycache__/PID.txt'))

PIDstore.save(getpid())

# ================================================================================================================

Search = List(JSON(
    path = root.child('/_/Search/search.json'), 
    default = []
))

class IndexRegistry(Path, List):

    def __init__(self,
        dir: Path
    ):
        
        indexJSON = JSON(dir.child('index.json'))

        Path.__init__(self, dir)
        List.__init__(self, indexJSON)

class IndexEntry(Path):

    dir: Path
    """ """

    def __init__(self,
        path: Path
    ):
        
        super().__init__(path)

        if self.is_dir:
            self.dir = self.path
        else:
            self.dir = self.parent

        self.JSON = {
            'URL': self.URL(),
            'Visible': self.Visible(),
            'Title': self.Title(),
            'SRC': self.SRC(),
            'Path': self.path
        }

    def URL(self) -> str:

        # Get base url from file path
        url = str(self).replace('E:/Website/Root', '', 1)

        # Check if file is '.href'
        if self.ext == 'href':
            # Return text contents of file
            return str(self.open().read()).strip()
        
        # Check if filename is 'index.html'
        elif url.split('/')[-1] == 'index.html':
            # Return url of parent directory
            return '/'.join(url.split('/')[:-1]) + '/'

        else:
            # Returm base url
            return url

    def Visible(self) -> bool:

        # Check if is directory
        if self.is_dir:
            # Return True unless 'hide.ini' exists inside the directory
            return (not self.child('Hide.ini').exists)

        # Check if filename starts with '__'
        elif self.seg().startswith('__'):
            return False
        
        # Check if file has a certain extension
        elif self.ext in ['ini', 'config', 'ds_store', 'json', 'js', 'py', 'css', 'gitignore']:
            return False
        
        # Check if filename is 'index.html'
        elif self.seg() == 'index.html':
            return False
        
        else:
            return True

    def Title(self) -> str:

        # Check if is dir
        if self.is_dir:
            # Return Name of Dir
            return self.name

        # Check if filename is 'index.html'
        elif self.seg() == 'index.html':

            # Check if file is in website root directory
            if self.dir == root:
                return "Phil's Server"

            else:
                # Return Name of parent directory
                return self.parent.name

        else:
            # Return Name of file
            return self.name

    def SRC(self) -> str|None:

        if self.is_dir:
            return None
        
        elif self.seg() == 'index.html':

            template = self.parent.sibling('__template__.html')
        
            if self.dir.child('Protect.ini').exists:
                src = self

            elif template.exists:
                src = template

            else:
                src = root.child('index.html')

            try:

                src.open().read()

                return str(src)
            
            except (UnicodeDecodeError, FileNotFoundError):
                pass

    def Update(self):
        from re import sub
        
        src = self.SRC()

        if src:

            mcode = sub(
                pattern = '<title>.*<\\/title>', 
                repl    = f'<title>{self.Title()}</title>', 
                string  = open(src).read()
            )
            
            self.open('w').write(mcode)

    def filter(self, term:str=None):
        if term:
            return (term.lower() in self.seg().lower())
        else:
            return True

# ================================================================================================================
