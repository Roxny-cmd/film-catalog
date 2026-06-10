from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.project_repository import get_project_by_id
from repositories.platform_repository import get_platform_by_id

from repositories.project_platform_repository import (
    create_project_platform,
    get_project_platforms,
    get_project_platform,
    delete_project_platform
)


def create_project_platform_service(db: Session,project_id: int,platform_id: int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")

    platform = get_platform_by_id(db, platform_id)
    if not platform:
        raise HTTPException(status_code=404,detail="Platform not found")

    existing = get_project_platform(db,project_id,platform_id)
    if existing:
        raise HTTPException(status_code=400,detail="Platform already added")

    return create_project_platform(db,project_id,platform_id)


def get_project_platforms_service(db: Session,project_id: int):
    return get_project_platforms(db, project_id)


def delete_project_platform_service(db: Session,project_id: int,platform_id: int):
    existing = get_project_platform(db,project_id,platform_id)
    if not existing:
        raise HTTPException(status_code=404,detail="Platform relation not found")
    return delete_project_platform(db,project_id,platform_id)