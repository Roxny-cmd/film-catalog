from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.project_cast_repository import (
    create_project_cast,
    get_project_cast,
    get_project_cast_member,
    delete_project_cast_member,
    update_project_cast_member_role
)

from repositories.project_repository import (
    get_project_by_id
)

from repositories.actor_repository import (
    get_actor_by_id
)

def create_project_cast_service(db:Session, project_id:int, actor_id:int, role:str):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    actor = get_actor_by_id(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    existing = get_project_cast_member(db, project_id, actor_id)
    if existing:
        raise HTTPException(status_code=409, detail="Project cast member already exists")
    return create_project_cast(db, project_id, actor_id, role)

def get_project_cast_service(db:Session, project_id:int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return get_project_cast(db, project_id)

def delete_project_cast_service(db:Session, project_id:int, actor_id:int):
    cast = get_project_cast_member(db, project_id, actor_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Project cast member not found")
    return delete_project_cast_member(db, project_id, actor_id)

def update_project_cast_service(db:Session, project_id:int, actor_id:int, role:str):
    cast = get_project_cast_member(db, project_id, actor_id)
    if not cast:
        raise HTTPException(status_code=404, detail="Project cast member not found")
    return update_project_cast_member_role(db, project_id, actor_id, role)