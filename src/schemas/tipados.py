from typing import Annotated
from pydantic import BaseModel,Field,BeforeValidator


BoolActivo = Annotated[bool,Field(description="Estado?")]
StrNombre = Annotated[str,Field(min_length=1,max_length=47)]
