from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI

app.title = "concesionaria autos"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)