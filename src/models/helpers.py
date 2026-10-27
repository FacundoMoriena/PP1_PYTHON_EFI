from typing import Annotated
from pydantic.functional_validators import BeforeValidator
from pydantic import Field




def str_mayus(t:str):
    if isinstance(t,str):
        nombre = t.upper().strip()
    return nombre





StrMayus = Annotated[str,Field(min_length=1,max_length=47),BeforeValidator(str_mayus)]