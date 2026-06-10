from pydantic import BaseModel, ConfigDict

class PlatformSchema(BaseModel):
    id:int
    name: str

    model_config = ConfigDict(from_attributes=True)

class PlatformCreateSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)