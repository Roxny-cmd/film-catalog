from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal
from schemas.director import DirectorShortSchema
from schemas.genre import GenreShortSchema


class ProjectCreateSchema(BaseModel):
    title: str
    project_type: str
    date_of_release: date
    rating: Decimal
    description: str | None = None
    director_id: int
    studio_id: int | None = None
    country_id: int | None = None
    genres: list[GenreShortSchema] = []
    model_config = ConfigDict(from_attributes = True)


class ProjectSchema(ProjectCreateSchema):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes = True)