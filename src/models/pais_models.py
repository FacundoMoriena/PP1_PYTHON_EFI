from sqlmodel import SQLModel,Field,Relationship
from pydantic import field_validator
from .helpers import StrMayus


class PaisBase(SQLModel):
    nombre:StrMayus
    activo:bool


class Pais(PaisBase,table = True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion con marca

class PaisCreate(PaisBase):
    pass

class PaisPublic(PaisBase):
    id : int


#class PaisPublicNested


    

