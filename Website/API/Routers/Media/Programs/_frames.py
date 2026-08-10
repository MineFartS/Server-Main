from philh_myftp_biz.web.driver import Driver
from philh_myftp_biz.pc.Path import Path
from re import search

class GitHub:

    files: dict[str, str]

    project: str

    def __getattr__(self, name:str) -> str | None:
        
        with Driver() as d:

            d.open(f"https://github.com/{self.project}/releases/latest")

            for _el in d.element('class', 'Box-row d-flex flex-column flex-md-row'):

                el = _el.children[0].children[1]

                if search(self.files[name], el.text):
                    return el.href

class staticfile:

    def __init__(self):
        name = self.__class__.__name__
        self.dir = Path(f"E:/Website/API/Routers/Media/Programs/static/{name}/")

    def __getattr__(self, name:str) -> Path | None:

        for file in self.dir.children:

            if file.name.lower() == name.lower():

                return file

        raise AttributeError()

