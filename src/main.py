from contextlib import asynccontextmanager
from pathlib import Path
from alembic.config import Config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,SQLModel
import models
from routers.paises import paises_routers
from routers.tipo_vehiculo import tipo_vehiculo_routers
from routers.marcas import marcas_routers
from routers.vehiculos import vehiculos_routers
from fastapi_pagination import add_pagination


from alembic import command


BASE_DIR = Path(__file__).resolve().parent.parent


def run_migrations():
    ini_path = BASE_DIR / "alembic.ini"
    alembic_dir = BASE_DIR / "alembic"

    # Verificación rápida en los logs para confirmar que se subieron los archivos
    if not ini_path.exists():
        raise FileNotFoundError(f"No se encontró alembic.ini en: {ini_path}")

    alembic_cfg = Config(str(ini_path))

    # Forzamos la ruta absoluta de la carpeta de migraciones
    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield



#SQLModel.metadata.create_all(bind = engine)
app = FastAPI(lifespan=lifespan)
app.title = "concesionaria vehiculos"
app.description ="EFI_PP1 trabajo integrador"

#routers
app.include_router(paises_routers,tags=["Paises"],prefix="/paises")
app.include_router(tipo_vehiculo_routers,tags=["TiposVehiculos"],prefix="/tipo_vehiculos")
app.include_router(marcas_routers,tags=["Marcas"],prefix="/marcas")
app.include_router(vehiculos_routers,tags=["Vehiculos"],prefix="/vehiculos")



add_pagination(app)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        #url front desplegado
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)
