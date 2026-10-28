from sqlmodel import SQLModel,Field,Relationship
from pydantic import field_validator
from .helpers import StrMayus
from typing import TYPE_CHECKING, Optional



if TYPE_CHECKING:
    from .marca_models import Marca,MarcaPublic,MarcaPublicNested


class PaisBase(SQLModel):
    nombre:StrMayus
    activo:bool


class Pais(PaisBase,table = True):
    id: int | None = Field(default=None, primary_key=True)
    marcas : list["Marca"] = Relationship(back_populates="pais")

class PaisCreate(PaisBase):
    pass

class PaisPublic(PaisBase):
    id : int


class PaisPublicNested(PaisPublic):
    marcas : Optional[list["MarcaPublic"]] = []


    

