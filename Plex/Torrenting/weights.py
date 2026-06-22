from philh_myftp_biz.web.torrent import NameParser
from philh_myftp_biz.text import similarity
from philh_myftp_biz.terminal import Log
from typing import Any

class WEIGHTS(dict[str, Any]):

    def parse(self, name:str):

        parse = NameParser(name)

        logm: str = f'Validating: {name}'

        valid = True

        for key, control in self.items():

            sample = getattr(parse, key.lower())

            _valid = getattr(self, key)(
                sample = sample,
                control = control
            )

            valid &= _valid

            logm += f'\n{key}={_valid:d} | {sample=} | {control=}'

        logm += f'\n{valid=}'
 
        Log.VERB(logm)

        return valid

    def TITLE(self,
        sample: str, 
        control: str|list[str]|None
    ) -> bool:
        
        if control is None:
            return True
        
        elif isinstance(control, list):
            return any(self.TITLE(sample, c) for c in control)
        
        else:
            return (similarity(a=sample, b=control) > .65)

    def SEASON(self,
        sample: int|list[int]|None, 
        control: int
    ) -> bool:
        
        if isinstance(sample, int):
            return (control == sample)

        elif isinstance(sample, list):
            return (control in sample)
        
        else:
            return False
        
    def YEAR(self,
        sample: int|list[int]|None, 
        control: int|list[int]
    ) -> bool:
        
        match (x.__class__.__name__ for x in (sample, control)):
        
            case 'list', 'int':
                return self.TITLE(sample, [control])
            
            case 'list', 'list':
                return any(c in sample for c in control)
        
            case 'int', 'int':
                return abs(control - sample) < 2
        
            case 'int', 'list':
                return sample in range(
                    control[0]-1, 
                    control[-1]+1
                )
            
            case _:
                return True

    def EPISODE(self,
        sample: int|list[int]|None, 
        control: int|None
    ) -> bool:
        
        if isinstance(sample, list):
            sample = sample[0]
        
        return (control == sample)
        
    def QUALITY(self,
        sample: None|str,
        control: None
    ) -> bool:
        
        if sample is None:
            return True
        
        return sample not in ['hdtv', 'tvrip'] 

