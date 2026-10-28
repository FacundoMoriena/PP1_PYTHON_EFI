from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,SQLModel
import models
from routers.paises import paises_routers
from routers.tipo_vehiculo import tipo_vehiculo_routers
from routers.marcas import marcas_routers
from fastapi_pagination import add_pagination

#SQLModel.metadata.create_all(bind = engine)
app = FastAPI()
app.title = "concesionaria vehiculos"

#routers
app.include_router(paises_routers,tags=["Paises"],prefix="/paises")
app.include_router(tipo_vehiculo_routers,tags=["TiposVehiculos"],prefix="/tipo_vehiculos")
app.include_router(marcas_routers,tags=["Marcas"],prefix="/marcas")



add_pagination(app)


#modificar despues,dependiendo del front
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)
