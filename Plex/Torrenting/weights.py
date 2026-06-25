from philh_myftp_biz.web.torrent import NameParser
from philh_myftp_biz.text import similarity
from philh_myftp_biz.terminal import Log
from typing import Any

class WEIGHTS(dict[str, Any]):

    def parse(self, name:str) -> bool:

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
        sample: str | None,
        control: list[str|None]
    ) -> bool:
        return any(similarity(sample, c)>.65 for c in control)

    def SEASON(self,
        sample: list[int], 
        control: int
    ) -> bool:
        return (control in sample)
        
    def YEAR(self,
        sample: list[int], 
        control: int
    ) -> bool:
        return (len(sample) == 0) or (control in sample)

    def EPISODE(self,
        sample: list[int], 
        control: int | None
    ) -> bool:
        if len(sample) > 0:
            return control == sample[0]
        else:
            return control is None

