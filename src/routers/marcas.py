
from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from models.marca_models import Marca,MarcaPublicNested,MarcaCreate,MarcaPublic
from models.pais_models import Pais
from sqlmodel import Session, select
from database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

marcas_routers = APIRouter()

NO_ENCONTRADO = {
    404: {
        "description": "Marca no encontrada",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Marca no encontrada",
                }
            }
        },
    },
}

BORRADO_EXITOSO = {
    204: {
        "description" : "Marca eliminada"
    }
}

PAIS_INEXISTENTE = {
    400: {
        "description": "País no existe o está inactivo",
        "content": {
            "application/json": {
                "example": {
                    "detail": "El país asociado no existe o está inactivo",
                }
            }
        },
    },
}



@marcas_routers.get(
    "/",
    response_model=Page[MarcaPublic],
)
def getMarca(db: Session = Depends(get_db)):
    
    query = select(Marca)
    return paginate(db,query)


@marcas_routers.get(
    "/{id}",
    response_model=MarcaPublicNested,
    responses=NO_ENCONTRADO,
)
def obtenerMarcaId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
) -> MarcaPublicNested:
    marca_obtenida = db.get(Marca, id)
    if marca_obtenida is not None:
        return marca_obtenida

    raise HTTPException(status_code=404, detail="Marca no encontrada")


@marcas_routers.post(
    "/",
    response_model=MarcaPublic,
    responses=PAIS_INEXISTENTE,
)
def postMarca(
    marca_nueva: MarcaCreate,
    db: Session = Depends(get_db),
):
    if marca_nueva.pais_id is not None:
        pais = db.get(Pais, marca_nueva.pais_id)
        if not pais or not pais.activo:
            raise HTTPException(
                status_code=400,
                detail="El país asociado no existe o está inactivo",
            )

    nueva_marca = Marca.model_validate(marca_nueva)

    db.add(nueva_marca)
    db.commit()
    db.refresh(nueva_marca)

    return nueva_marca


@marcas_routers.put(
    "/{id}",
    responses={**NO_ENCONTRADO, **PAIS_INEXISTENTE},
    response_model=MarcaPublic,
)
async def modificarMarca(
    id: Annotated[int, Path(gt=0)],
    marca_editada: MarcaCreate,
    db: Session = Depends(get_db),
) -> MarcaPublic:
    marca_obtenida = db.get(Marca, id)

    if not marca_obtenida:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    if marca_editada.pais_id is not None:
        pais = db.get(Pais, marca_editada.pais_id)
        if not pais or not pais.activo:
            raise HTTPException(
                status_code=400,
                detail="El país asociado no existe o está inactivo",
            )

    marca_obtenida.nombre = marca_editada.nombre
    marca_obtenida.pais_id = marca_editada.pais_id
    marca_obtenida.activo = marca_editada.activo

    db.commit()
    db.refresh(marca_obtenida)

    return marca_obtenida


@marcas_routers.delete(
    "/{id}",
    status_code=204,
    responses={**NO_ENCONTRADO, **BORRADO_EXITOSO},
)
def borrarMarca(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
    db: Session = Depends(get_db),
) -> None:
    marca_obtenida = db.get(Marca, id)

    if not marca_obtenida:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    if logico:
        marca_obtenida.activo = False
    else:
        db.delete(marca_obtenida)

    db.commit()
    return None