from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.country_repository import (
    get_country_by_name,
    create_country,
    get_all_countries,
    get_country_by_id,
    delete_country_by_id,
    update_country_by_id
)

def create_country_service(db:Session, name:str):
    existing = get_country_by_name(db,name)
    if existing:
        raise HTTPException(status_code=400, detail="Country already exists")
    return create_country(db,name)

def get_all_countries_service(db:Session):
    return get_all_countries(db)

def get_country_by_name_service(db:Session, name:str):
    existing = get_country_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Country not found")
    return existing

def get_country_by_id_service(db:Session, id:int):
    existing = get_country_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Country not found")
    return existing

def delete_country_service(db:Session, id:int):
    existing = get_country_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Country not found")
    return delete_country_by_id(db,id)

def update_country_service(db:Session,id:int, name:str):
    existing = get_country_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Country not found")
    return update_country_by_id(db, id, name)


