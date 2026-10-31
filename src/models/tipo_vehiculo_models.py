from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from .helpers import StrMayus

if TYPE_CHECKING:
    from .vehiculo_models import Vehiculo, VehiculoPublic


class TipoVehiculoBase(SQLModel):
    nombre: StrMayus
    activo: bool


class TipoVehiculo(TipoVehiculoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vehiculos: list["Vehiculo"] = Relationship(back_populates="tipo_vehiculo")


class TipoVehiculoCreate(TipoVehiculoBase):
    pass


class TipoVehiculoPublic(TipoVehiculoBase):
    id: int


class TipoVehiculoPublicNested(TipoVehiculoPublic):
    vehiculos: list["VehiculoPublic"] = []