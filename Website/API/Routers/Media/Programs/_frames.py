from philh_myftp_biz.web.driver import Driver
from re import search

class GitHub:

    files: dict[str, str]

    project: str

    def __getattr__(self, name:str):
        
        with Driver() as d:

            d.open(f"https://github.com/{self.project}/releases/latest")

            for _el in d.element('class', 'Box-row d-flex flex-column flex-md-row'):

                el = _el.children[0].children[1]

                if search(self.files[name], el.text):
                    return el.href

