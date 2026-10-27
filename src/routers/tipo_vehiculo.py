from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from models.tipo_vehiculo_models import TipoVehiculo,TipoVehiculoCreate,TipoVehiculoPublic
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



@tipo_vehiculo_routers.get(
    "/",
    response_model=Page[TipoVehiculoPublic],
)
async def getTipoVehiculo(db: Session = Depends(get_db)):
    
    query = select(TipoVehiculo)
    return paginate(db,query)


@tipo_vehiculo_routers.get(
    "/{id}",
    response_model=TipoVehiculoPublic,
    responses=NO_ENCONTRADO,
)
async def obtenerTipoVehiculoId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
) -> TipoVehiculoPublic:
    tipo_vehiculo_obtenido = db.get(TipoVehiculo, id)
    if tipo_vehiculo_obtenido is not None:
        return tipo_vehiculo_obtenido

    raise HTTPException(status_code=404, detail="País no encontrado")


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


@tipo_vehiculo_routers.delete(
    "/{id}",
    responses=NO_ENCONTRADO,
    response_model=Union[TipoVehiculoPublic, list[TipoVehiculoPublic]],
)
async def borrarTipoVehiculo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
    db: Session = Depends(get_db),
) -> Union[TipoVehiculoPublic, list[TipoVehiculoPublic]]:
    tipo_vehiculo_obtenido = db.get(TipoVehiculo, id)

    if not tipo_vehiculo_obtenido:
        raise HTTPException(status_code=404, detail="País no encontrado")

    if logico:
        tipo_vehiculo_obtenido.activo = False
        db.commit()
        db.refresh(tipo_vehiculo_obtenido)
        return tipo_vehiculo_obtenido

    db.delete(tipo_vehiculo_obtenido)
    db.commit()

    return db.exec(select(TipoVehiculo)).all()