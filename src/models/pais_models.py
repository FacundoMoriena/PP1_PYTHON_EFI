from sqlmodel import SQLModel,Field,Relationship



class PaisBase(SQLModel):
    nombre:str
    activo:bool

class Pais(PaisBase,table = True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion con marca

class PaisCreate(PaisBase):
    pass

class PaisPublic(PaisBase):
    id : int


#class PaisPublicNested


    

