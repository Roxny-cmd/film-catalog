from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.project_repository import (
    create_project,
    get_all_projects,
    get_project_by_id,
    get_project_by_title,       # переименованная функция
    delete_project_by_id,
    update_project_by_id,
    get_projects_by_owner
)
from repositories.project_genre_repository import create_project_genre
from repositories.project_platform_repository import create_project_platform
from repositories.genre_repository import get_genre_by_id
from repositories.platform_repository import get_platform_by_id


def create_project_service(db: Session, data: dict, owner_id: int):
    genre_ids = data.pop("genre_ids", [])
    platform_ids = data.pop("platform_ids", [])

    data["owner_id"] = owner_id
    project = create_project(db, data)

    for genre_id in genre_ids:
        if get_genre_by_id(db, genre_id):
            create_project_genre(db, project.id, genre_id)

    for platform_id in platform_ids:
        if get_platform_by_id(db, platform_id):
            create_project_platform(db, project.id, platform_id)

    return project

def get_all_projects_service(db: Session):
    return get_all_projects(db)

def get_my_projects_service(db: Session, owner_id: int):   # новый
    return get_projects_by_owner(db, owner_id)

def get_project_by_id_service(db: Session, id: int):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def get_project_by_title_service(db: Session, title: str):
    project = get_project_by_title(db, title)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def delete_project_service(db: Session, id: int, current_user_id: int):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return delete_project_by_id(db, id)

def update_project_service(db: Session, id: int, data: dict, current_user_id: int):
    project = get_project_by_id(db, id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return update_project_by_id(db, id, data)