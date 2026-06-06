from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from decimal import Decimal
from typing import Literal
from schemas.director import DirectorShortSchema
from schemas.genre import GenreShortSchema
from schemas.platform import PlatformSchema


class ProjectCreateSchema(BaseModel):
    title: str
    project_type: Literal['film', 'serial']      # валидация типа
    date_of_release: date
    rating: Decimal
    description: str | None = None
    director_id: int | None = None               # опциональный
    studio_id: int | None = None
    country_id: int | None = None
    genre_ids: list[int] = []                    # список id, не объектов
    platform_ids: list[int] = []                 # добавили платформы

    @field_validator("rating")
    def validate_rating(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Rating must be between 0 and 10")
        return v

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdateSchema(BaseModel):            # новый — для PATCH/PUT
    title: str | None = None
    project_type: Literal['film', 'serial'] | None = None
    date_of_release: date | None = None
    rating: Decimal | None = None
    description: str | None = None
    director_id: int | None = None
    studio_id: int | None = None
    country_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectSchema(BaseModel):                  # полная карточка для ответа
    id: int
    title: str
    project_type: str
    date_of_release: date
    rating: Decimal
    description: str | None = None
    owner_id: int
    director: DirectorShortSchema | None = None
    genres: list[GenreShortSchema] = []
    platforms: list[PlatformSchema]