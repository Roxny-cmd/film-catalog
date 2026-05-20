from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.actor_repository import (
    get_actor_by_name,
    create_actor,
    get_all_actors,
    get_actor_by_id,
    delete_actor_by_id,
    update_actor_by_id
)

def create_actor_service(db:Session, name:str):
    existing = get_actor_by_name(db,name)
    if existing:
        raise HTTPException(status_code=400, detail="Actor already exists")
    return create_actor(db,name)

def get_all_actors_service(db:Session):
    return get_all_actors(db)

def get_actor_by_name_service(db:Session, name:str):
    existing = get_actor_by_name(db,name)
    if not existing:
        raise HTTPException(status_code=404, detail="Actor not found")
    return existing

def get_actor_by_id_service(db:Session, id:int):
    existing = get_actor_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Actor not found")
    return existing

def delete_actor_service(db:Session, id:int):
    existing = get_actor_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Actor not found")
    return delete_actor_by_id(db,id)

def update_actor_service(db:Session,id:int, name:str):
    existing = get_actor_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Actor not found")
    return update_actor_by_id(db, id, name)


