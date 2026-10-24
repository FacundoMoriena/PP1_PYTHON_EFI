import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,SQLModel
import models
from routers.paises import paises_routers


#SQLModel.metadata.create_all(bind = engine)
app = FastAPI()
app.title = "concesionaria autos"

#routers
app.include_router(paises_routers,tags=["Paises"],prefix="/paises")


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
