from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.director_repository import (
    get_director_by_name,
    create_director,
    get_all_directors,
    get_director_by_id,
    delete_director_by_id,
    update_director_by_id
)

def create_director_service(db:Session, name:str):
    existing = get_director_by_name(db,name)
    if existing:
        raise HTTPException(status_code=400, detail="Director already exists")
    return create_director(db,name)

def get_all_director_service(db:Session):
    return get_all_directors(db)

def get_director_by_name_service(db:Session, name:str):
    existing = get_director_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Director not found")
    return existing

def get_director_by_id_service(db:Session, id:int):
    existing = get_director_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Director not found")
    return existing

def delete_director_service(db:Session, id:int):
    existing = get_director_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Director not found")
    return delete_director_by_id(db,id)

def update_director_service(db:Session,id:int, name:str):
    existing = get_director_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Director not found")
    return update_director_by_id(db, id, name)


