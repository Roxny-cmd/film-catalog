from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.studio_repository import (
    create_studio,
    get_studio_by_id,
    get_studio_by_name,
    get_all_studios,
    delete_studio_by_id,
    update_studio_by_id
)

def create_studio_service(db:Session, name:str):
    existing = get_studio_by_name(db,name)
    if existing:
        raise HTTPException(status_code=404, detail="Studio already exists")
    return create_studio(db,name)

def get_studio_by_id_service(db:Session, id:int):
    existing = get_studio_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Studio not found")
    return existing

def get_studio_by_name_service(db:Session, name:str):
    existing = get_studio_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Studio not found")
    return existing

def get_all_studios_service(db:Session):
    return get_all_studios(db)

def delete_studio_service(db:Session, id:int):
    existing = get_studio_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Studio not found")
    return delete_studio_by_id(db,id)

def update_studio_service(db:Session, id:int, name:str):
    existing = get_studio_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Studio not found")
    return update_studio_by_id(db,id,name)