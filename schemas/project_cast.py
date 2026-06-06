from pydantic import BaseModel, ConfigDict
from schemas.actor import ActorSchema            # импорт вместо дубля

class ProjectCastCreateSchema(BaseModel):
    actor_id: int
    role: str

class ProjectCastSchema(BaseModel):
    project_id: int
    actor: ActorSchema                           # используем общую схему
    role: str
    model_config = ConfigDict(from_attributes=True)