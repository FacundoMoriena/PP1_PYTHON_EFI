from typing import Annotated
from pydantic.functional_validators import AfterValidator
from pydantic import Field




def str_mayus(t:str):
    if isinstance(t,str):
        nombre = t.upper().strip()
    return nombre

def str_title(t:str):
    if isinstance(t,str):
        nombre = t.title().strip()
    return nombre





StrMayus = Annotated[str,Field(min_length=1,max_length=47),AfterValidator(str_mayus)]
StrTitle = Annotated[str,Field(min_length=1,max_length=50),AfterValidator(str_title)]