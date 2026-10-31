from .pais_models import Pais, PaisPublic, PaisPublicNested
from .marca_models import Marca, MarcaPublic, MarcaPublicNested
from .tipo_vehiculo_models import TipoVehiculo, TipoVehiculoPublic, TipoVehiculoPublicNested
from .vehiculo_models import Vehiculo, VehiculoCreate, VehiculoPublic, VehiculoPublicNested

PaisPublicNested.model_rebuild(_types_namespace={"MarcaPublic": MarcaPublic})
MarcaPublicNested.model_rebuild(_types_namespace={"PaisPublic": PaisPublic, "VehiculoPublic": VehiculoPublic})
TipoVehiculoPublicNested.model_rebuild(_types_namespace={"VehiculoPublic": VehiculoPublic})
VehiculoPublicNested.model_rebuild(_types_namespace={"MarcaPublic": MarcaPublic, "TipoVehiculoPublic": TipoVehiculoPublic})