from sqlmodel import SQLModel,Field,Relationship
from pydantic import field_validator
from .helpers import StrMayus


class TipoVehiculoBase(SQLModel):
    nombre:StrMayus
    activo:bool


class TipoVehiculo(TipoVehiculoBase,table = True):
    id: int | None = Field(default=None, primary_key=True)
    

class TipoVehiculoCreate(TipoVehiculoBase):
    pass

class TipoVehiculoPublic(TipoVehiculoBase):
    id : int


#TipoVehiculoNested con tabla vehiculos