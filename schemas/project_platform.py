from pydantic import BaseModel

class ProjectPlatformCreateSchema(BaseModel):
    platform_id: int

class ProjectPlatformSchema(BaseModel):
    project_id: int
    platform_id: int

    class Config:
        from_attributes = True