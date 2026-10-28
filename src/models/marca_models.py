from sqlmodel import SQLModel,Field,Relationship
from pydantic import field_validator
from .helpers import StrTitle
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .pais_models import Pais,PaisPublic,PaisPublicNested


class MarcaBase(SQLModel):
    nombre:StrTitle
    pais_id : int | None = Field(default=None, foreign_key='pais.id')
    activo:bool


class Marca(MarcaBase,table = True):
    id: int | None = Field(default=None, primary_key=True)
    pais : Optional["Pais"] = Relationship(back_populates="marcas")

class MarcaCreate(MarcaBase):
    pass

class MarcaPublic(MarcaBase):
    id : int

class MarcaPublicNested(MarcaPublic):
     pais: Optional["PaisPublic"] = None

