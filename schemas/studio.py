from pydantic import BaseModel, ConfigDict

class StudioSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class StudioCreateSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)