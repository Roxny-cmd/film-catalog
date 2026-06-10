from pydantic import BaseModel, ConfigDict

class DirectorSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class DirectorCreateSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class DirectorShortSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)