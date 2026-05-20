from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.project_repository import (
    create_project,
    get_all_projects,
    get_project_by_id,
    get_project_by_name,
    delete_project_by_id,
    update_project_by_id
)


def create_project_service(db: Session, data: dict):
    return create_project(db, data)

def get_all_projects_service(db: Session):
    return get_all_projects(db)

def get_project_by_id_service(db: Session, id: int):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def get_project_by_name_service(db: Session, name: str):
    project = get_project_by_name(db, name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def delete_project_service(db:Session, id:int):
    existing = get_project_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    return delete_project_by_id(db,id)

def update_project_service(db:Session, id:int, name:str):
    existing = get_project_by_id(db,id)
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    return update_project_by_id(db,id,name)