from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from core.dependencies import get_current_user
from schemas.project_platform import (
    ProjectPlatformCreateSchema,
    ProjectPlatformSchema
)

from services.project_platform_service import (
    create_project_platform_service,
    get_project_platforms_service,
    delete_project_platform_service
)

router = APIRouter(prefix="/projects",tags=["Project Platforms"], dependencies=[Depends(get_current_user)])


@router.post("/{project_id}/platforms",response_model=ProjectPlatformSchema)
def add_platform_to_project(project_id: int,data: ProjectPlatformCreateSchema,db: Session = Depends(get_db)):
    return create_project_platform_service(db,project_id,data.platform_id)


@router.get("/{project_id}/platforms",response_model=list[ProjectPlatformSchema])
def get_project_platforms(project_id: int,db: Session = Depends(get_db)):
    return get_project_platforms_service(db,project_id)


@router.delete("/{project_id}/platforms/{platform_id}",response_model=ProjectPlatformSchema)
def delete_project_platform(project_id: int,platform_id: int,db: Session = Depends(get_db)):
    return delete_project_platform_service(db,project_id,platform_id)