from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.project_repository import get_project_by_id
from repositories.genre_repository import get_genre_by_id

from repositories.project_genre_repository import (
    create_project_genre,
    get_project_genres,
    get_project_genre,
    delete_project_genre
)


def create_project_genre_service(db: Session,project_id: int,genre_id: int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")

    genre = get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404,detail="Genre not found")

    existing = get_project_genre(db,project_id,genre_id)
    if existing:
        raise HTTPException(status_code=400,detail="Genre already added")

    return create_project_genre(db,project_id,genre_id)


def get_project_genres_service(db: Session,project_id: int):
    return get_project_genres(db, project_id)


def delete_project_genre_service(db: Session,project_id: int,genre_id: int):
    existing = get_project_genre(db,project_id,genre_id)
    if not existing:
        raise HTTPException(status_code=404,detail="Genre relation not found")
    return delete_project_genre(db,project_id,genre_id)