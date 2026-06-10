from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.genre_repository import (
    create_genre,
    get_genre_by_id,
    get_genre_by_name,
    get_all_genres,
    delete_genre_by_id,
    update_genre_by_id
)

def create_genre_service(db:Session, name:str):
    existing = get_genre_by_name(db,name)
    if existing:
        raise HTTPException(status_code=404, detail="Genre already exists")
    return create_genre(db,name)

def get_genre_by_id_service(db:Session, id:int):
    existing = get_genre_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Genre not found")
    return existing

def get_genre_by_name_service(db:Session, name:str):
    existing = get_genre_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Genre not found")
    return existing

def get_all_genres_service(db:Session):
    return get_all_genres(db)

def delete_genre_service(db:Session, id:int):
    existing = get_genre_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Genre not found")
    return delete_genre_by_id(db,id)

def update_genre_service(db:Session, id:int, name:str):
    existing = get_genre_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Genre not found")
    return update_genre_by_id(db,id,name)