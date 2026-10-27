from typing import Annotated, Union
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from models.pais_models import Pais, PaisPublic, PaisCreate
from sqlmodel import Session, select
from database import get_db
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

paises_routers = APIRouter()

NO_ENCONTRADO = {
    404: {
        "description": "País no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "País no encontrado",
                }
            }
        },
    },
}



@paises_routers.get(
    "/",
    response_model=Page[PaisPublic],
)
async def getPaises(db: Session = Depends(get_db)):
    
    query = select(Pais)
    return paginate(db,query)


@paises_routers.get(
    "/{id}",
    response_model=PaisPublic,
    responses=NO_ENCONTRADO,
)
async def obtenerPaisId(
    id: Annotated[int, Path(gt=0)],
    db: Session = Depends(get_db),
) -> PaisPublic:
    pais_obtenido = db.get(Pais, id)
    if pais_obtenido is not None:
        return pais_obtenido

    raise HTTPException(status_code=404, detail="País no encontrado")


@paises_routers.post(
    "/",
    response_model=PaisPublic,
)
async def postPais(
    pais_nuevo: PaisCreate,
    db: Session = Depends(get_db),
):
    nuevo_pais = Pais.model_validate(pais_nuevo)

    db.add(nuevo_pais)
    db.commit()
    db.refresh(nuevo_pais)

    return nuevo_pais


@paises_routers.delete(
    "/{id}",
    responses=NO_ENCONTRADO,
    response_model=Union[PaisPublic, list[PaisPublic]],
)
async def borrarPais(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?"),
    ] = False,
    db: Session = Depends(get_db),
) -> Union[PaisPublic, list[PaisPublic]]:
    pais_obtenido = db.get(Pais, id)

    if not pais_obtenido:
        raise HTTPException(status_code=404, detail="País no encontrado")

    if logico:
        pais_obtenido.activo = False
        db.commit()
        db.refresh(pais_obtenido)
        return pais_obtenido

    db.delete(pais_obtenido)
    db.commit()

    return db.exec(select(Pais)).all()