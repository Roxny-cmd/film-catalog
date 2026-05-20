from pydantic import BaseModel

class ActorShortSchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class ProjectCastCreateSchema(BaseModel):
    actor_id: int
    role: str

class ProjectCastSchema(BaseModel):
    project_id: int
    actor: ActorShortSchema
    role: str
    class Config:
        from_attributes = True