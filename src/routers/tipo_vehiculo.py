from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from models.tipo_vehiculo_models import TipoVehiculo,TipoVehiculoCreate,TipoVehiculoPublic,TipoVehiculoPublicNested
from sqlmodel import Session, select
from database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

tipo_vehiculo_routers = APIRouter()

NO_ENCONTRADO = {
    404: {
        "description": "Tipo vehiculo no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Tipo vehiculo no encontrado",
                }
            }
        },
    },
}

BORRADO_EXITOSO = {
    204: {
        "description": "Tipo de vehículo eliminado con éxito",
    }
}



@tipo_vehiculo_routers.get(
    "/",
    response_model=Page[TipoVehiculoPublic],
)
async def getTipoVehiculo(db: Session = Depends(get_db)):
    
    query = select(TipoVehiculo)
    return paginate(db,query)


@tipo_vehiculo_routers.get(
    "/{id}",
    response_model=TipoVehiculoPublicNested,
    responses=NO_ENCONTRADO,
)
async def obtenerTipoVehiculoId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
) -> TipoVehiculoPublic:
    tipo_vehiculo_obtenido = db.get(TipoVehiculo, id)
    if tipo_vehiculo_obtenido is not None:
        return tipo_vehiculo_obtenido

    raise HTTPException(status_code=404, detail="Tipo vehiculo no encontrado")


@tipo_vehiculo_routers.post(
    "/",
    response_model=TipoVehiculoPublic,
)
async def postTipoVehiculo(
    tipo_vehiculo_nuevo: TipoVehiculoCreate,
    db: Session = Depends(get_db),
):
    nuevo_tipo_vehiculo = TipoVehiculo.model_validate(tipo_vehiculo_nuevo)

    db.add(nuevo_tipo_vehiculo)
    db.commit()
    db.refresh(nuevo_tipo_vehiculo)

    return nuevo_tipo_vehiculo


@tipo_vehiculo_routers.put(
    "/{id}",
    responses=NO_ENCONTRADO,
    response_model=TipoVehiculoPublic,
)
async def modificarTipoVehiculo(
    id: Annotated[int, Path(gt=0)],
    tipo_vehiculo_editado: TipoVehiculoCreate,
    db: Session = Depends(get_db),
) -> TipoVehiculoPublic:
    tipo_vehiculo_obtenido = db.get(TipoVehiculo, id)

    if not tipo_vehiculo_obtenido:
        raise HTTPException(status_code=404, detail="Tipo vehiculo no encontrado")

    tipo_vehiculo_obtenido.nombre = tipo_vehiculo_editado.nombre
    tipo_vehiculo_obtenido.activo = tipo_vehiculo_editado.activo

    db.commit()
    db.refresh(tipo_vehiculo_obtenido)

    return tipo_vehiculo_obtenido


@tipo_vehiculo_routers.delete(
    "/{id}",
    status_code=204,
    responses={**NO_ENCONTRADO, **BORRADO_EXITOSO},
)
def borrarTipoVehiculo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
    db: Session = Depends(get_db),
) -> None:
    tipo_vehiculo_obtenido = db.get(TipoVehiculo, id)

    if not tipo_vehiculo_obtenido:
        raise HTTPException(status_code=404, detail="Tipo vehiculo no encontrado")

    if logico:
        tipo_vehiculo_obtenido.activo = False
    else:
        db.delete(tipo_vehiculo_obtenido)

    db.commit()
    return None