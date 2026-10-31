from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from .helpers import StrTitle

if TYPE_CHECKING:
    from .marca_models import Marca, MarcaPublic
    from .tipo_vehiculo_models import TipoVehiculo, TipoVehiculoPublic


class VehiculoBase(SQLModel):
    nombre: StrTitle
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    url_image: str | None = Field(default=None,)
    descripcion: str | None = Field(default=None, max_length=500)
    estado_uso: str | None = Field(default=None,max_length=50)
    modelo: int | None = Field(default=None,description="año de modelo ej:2005")
    activo: bool = Field(default=True)
    marca_id: int = Field(default=None, foreign_key="marca.id")
    tipo_vehiculo_id :int = Field(default=None, foreign_key="tipovehiculo.id")


class Vehiculo(VehiculoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    marca: Optional["Marca"] = Relationship(back_populates="vehiculos")
    tipo_vehiculo: Optional["TipoVehiculo"] = Relationship(back_populates="vehiculos")


class VehiculoCreate(VehiculoBase):
    pass


class VehiculoPublic(VehiculoBase):
    id: int


class VehiculoPublicNested(VehiculoPublic):
    marca: Optional["MarcaPublic"] = None
    tipo_vehiculo: Optional["TipoVehiculoPublic"] = None