from pydantic import BaseModel

class ProjectGenreCreateSchema(BaseModel):
    genre_id: int

class ProjectGenreSchema(BaseModel):
    project_id: int
    genre_id: int

    class Config:
        from_attributes = True