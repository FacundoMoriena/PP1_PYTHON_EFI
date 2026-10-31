from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from models.vehiculo_models import (
    Vehiculo,
    VehiculoCreate,
    VehiculoPublic,
    VehiculoPublicNested,
)
from models.marca_models import Marca
from models.tipo_vehiculo_models import TipoVehiculo
from sqlmodel import Session, select , col
from database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

vehiculos_routers = APIRouter()

NO_ENCONTRADO = {
    404: {
        "description": "Vehículo no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Vehículo no encontrado",
                }
            }
        },
    },
}

BORRADO_EXITOSO = {
    204: {
        "description": "Vehículo eliminado con éxito",
    }
}

RELACION_INEXISTENTE = {
    400: {
        "description": "Marca o Tipo de vehículo no existe o está inactivo",
        "content": {
            "application/json": {
                "example": {
                    "detail": "La marca asociada no existe o está inactiva",
                }
            }
        },
    },
}

CAMPO_FILTRADO = {
    400: {
        "description": "Campo filtrado inexistente/inválido",
        "content": {
            "application/json": {
                "example": {
                    "detail": "El campo filtrado no existe",
                }
            }
        },
    },
}




@vehiculos_routers.get(
    "/",
    response_model=Page[VehiculoPublic],
    responses=CAMPO_FILTRADO,
)
def getVehiculos(
    nombre:Annotated[str,Query(description="Busqueda por nombre")] | None = None,
    marca_id : Annotated[int,Query(description="Busqueda por marca ID")] | None = None,
    modelo : Annotated [int,Query(description="Busqueda por modelo")] | None = None,
    tipo_vehiculo_id : Annotated[int,Query(description="Busqueda por tipo vehiculo ID")] | None = None,
    sort_by:Annotated[str,Query(description="Columna a ordenar resultados")] | None = None,
    order:Annotated[str,Query(description="'asc' para ascendente,'desc'para descendente")] = "asc",
    db: Session = Depends(get_db)):
    query = select(Vehiculo)

    #filtros
    if nombre:
        query = query.where(col(Vehiculo.nombre).ilike(f"%{nombre}%"))
    if marca_id is not None:
        query = query.where(col(Vehiculo.marca_id) == marca_id)
    if tipo_vehiculo_id is not None:
        query = query.where(col(Vehiculo.tipo_vehiculo_id) == tipo_vehiculo_id)
    if modelo is not None:
        query = query.where(col(Vehiculo.modelo)== modelo)
    
    if sort_by:
        campo_sort = getattr(Vehiculo,sort_by,None)
        if not campo_sort:
            raise HTTPException(status_code = 400,detail = "Campo inválido")

        if order == 'asc':
            query = query.order_by(campo_sort.asc())
        else:
            query = query.order_by(campo_sort.desc())
    
    
    
    return paginate(db, query)


@vehiculos_routers.get(
    "/{id}",
    response_model=VehiculoPublicNested,
    responses=NO_ENCONTRADO,
)
def obtenerVehiculoId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
) -> VehiculoPublicNested:
    vehiculo_obtenido = db.get(Vehiculo, id)
    if vehiculo_obtenido is not None:
        return vehiculo_obtenido

    raise HTTPException(status_code=404, detail="Vehículo no encontrado")


@vehiculos_routers.post(
    "/",
    response_model=VehiculoPublic,
    responses=RELACION_INEXISTENTE,
)
def postVehiculo(
    vehiculo_nuevo: VehiculoCreate,
    db: Session = Depends(get_db),
):
    if vehiculo_nuevo.marca_id is not None:
        marca = db.get(Marca, vehiculo_nuevo.marca_id)
        if not marca or not marca.activo:
            raise HTTPException(
                status_code=400,
                detail="La marca asociada no existe o está inactiva",
            )

    if vehiculo_nuevo.tipo_vehiculo_id is not None:
        tipo_vehiculo = db.get(TipoVehiculo, vehiculo_nuevo.tipo_vehiculo_id)
        if not tipo_vehiculo or not tipo_vehiculo.activo:
            raise HTTPException(
                status_code=400,
                detail="El tipo de vehículo asociado no existe o está inactivo",
            )

    nuevo_vehiculo = Vehiculo.model_validate(vehiculo_nuevo)

    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)

    return nuevo_vehiculo


@vehiculos_routers.put(
    "/{id}",
    responses={**NO_ENCONTRADO, **RELACION_INEXISTENTE},
    response_model=VehiculoPublic,
)
async def modificarVehiculo(
    id: Annotated[int, Path(gt=0)],
    vehiculo_editado: VehiculoCreate,
    db: Session = Depends(get_db),
) -> VehiculoPublic:
    vehiculo_obtenido = db.get(Vehiculo, id)

    if not vehiculo_obtenido:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    if vehiculo_editado.marca_id is not None:
        marca = db.get(Marca, vehiculo_editado.marca_id)
        if not marca or not marca.activo:
            raise HTTPException(
                status_code=400,
                detail="La marca asociada no existe o está inactiva",
            )

    if vehiculo_editado.tipo_vehiculo_id is not None:
        tipo_vehiculo = db.get(TipoVehiculo, vehiculo_editado.tipo_vehiculo_id)
        if not tipo_vehiculo or not tipo_vehiculo.activo:
            raise HTTPException(
                status_code=400,
                detail="El tipo de vehículo asociado no existe o está inactivo",
            )

    vehiculo_obtenido.nombre = vehiculo_editado.nombre
    vehiculo_obtenido.precio = vehiculo_editado.precio
    vehiculo_obtenido.stock = vehiculo_editado.stock
    vehiculo_obtenido.url_image = vehiculo_editado.url_image
    vehiculo_obtenido.descripcion = vehiculo_editado.descripcion
    vehiculo_obtenido.estado_uso = vehiculo_editado.estado_uso
    vehiculo_obtenido.modelo = vehiculo_editado.modelo
    vehiculo_obtenido.activo = vehiculo_editado.activo
    vehiculo_obtenido.marca_id = vehiculo_editado.marca_id
    vehiculo_obtenido.tipo_vehiculo_id = vehiculo_editado.tipo_vehiculo_id

    db.commit()
    db.refresh(vehiculo_obtenido)

    return vehiculo_obtenido


@vehiculos_routers.delete(
    "/{id}",
    status_code=204,
    responses={**NO_ENCONTRADO, **BORRADO_EXITOSO},
)
def borrarVehiculo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
    db: Session = Depends(get_db),
) -> None:
    vehiculo_obtenido = db.get(Vehiculo, id)

    if not vehiculo_obtenido:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    if logico:
        vehiculo_obtenido.activo = False
    else:
        db.delete(vehiculo_obtenido)

    db.commit()
    return None
