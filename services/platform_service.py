from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.platform_repository import (
    create_platform,
    get_platform_by_id,
    get_platform_by_name,
    get_all_platforms,
    delete_platform_by_id,
    update_platform_by_id
)

def create_platform_service(db:Session, name:str):
    existing = get_platform_by_name(db,name)
    if existing:
        raise HTTPException(status_code=404, detail="Platform already exists")
    return create_platform(db,name)

def get_platform_by_id_service(db:Session, id:int):
    existing = get_platform_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Platform not found")
    return existing

def get_platform_by_name_service(db:Session, name:str):
    existing = get_platform_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Platform not found")
    return existing

def get_all_platforms_service(db:Session):
    return get_all_platforms(db)

def delete_platform_service(db:Session, id:int):
    existing = get_platform_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Platform not found")
    return delete_platform_by_id(db,id)

def update_platform_service(db:Session, id:int, name:str):
    existing = get_platform_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Platform not found")
    return update_platform_by_id(db,id,name)