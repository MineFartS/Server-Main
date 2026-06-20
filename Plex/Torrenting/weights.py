from philh_myftp_biz.web.torrent import NameParser
from philh_myftp_biz.text import similarity
from philh_myftp_biz.terminal import Log
from typing import Any

class WEIGHTS(dict[str, Any]):

    def parse(self, name: str):

        parse = NameParser(name)

        logm: str = f'Validating: {name}'

        valid = True

        for key, control in self.items():

            target = getattr(parse, key.lower())

            _valid = getattr(self, key)(
                target = target,
                control = control
            )

            valid &= _valid

            logm += f'\n{key}={_valid:d} | {target=} | {control=}'

        logm += f'\n{valid=}'
 
        Log.VERB(logm)

        return valid

    def TITLE(self,
        target: str, 
        control: str|None
    ) -> bool:
        
        if control is None:
            return True
        else:
            return (similarity(a=target, b=control) > .65)

    def SEASON(self,
        target: int|list[int]|None, 
        control: int
    ) -> bool:
        
        if isinstance(target, int):
            return (control == target)

        elif isinstance(target, list):
            return (control in target)
        
        else:
            return False
        
    def YEAR(self,
        target: int|list[int]|None, 
        control: int|list[int]
    ) -> bool:
        
        if target is None:
            return True
        
        elif isinstance(target, list):
            return (control in target)
        
        else:
        
            if isinstance(control, int):
                MIN = control-1
                MAX = control+1
            else:
                MIN = control[0]-1
                MAX = control[-1]+1

            return (MIN <= target <= MAX)

    def EPISODE(self,
        target: int|list[int]|None, 
        control: int|None
    ) -> bool:
        
        if isinstance(target, list):
            return (control == target[0])
        
        else:
            return (control == target)
