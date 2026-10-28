from .pais_models import Pais, PaisPublic, PaisPublicNested
from .marca_models import Marca, MarcaPublic, MarcaPublicNested
from .tipo_vehiculo_models import TipoVehiculo, TipoVehiculoPublic



PaisPublicNested.model_rebuild(_types_namespace={"MarcaPublic": MarcaPublic})
MarcaPublicNested.model_rebuild(_types_namespace={"PaisPublic": PaisPublic})