from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from core.dependencies import get_current_user
from schemas.project_cast import (
    ProjectCastCreateSchema,
    ProjectCastSchema
)

from services.project_cast_service import (
    create_project_cast_service,
    get_project_cast_service,
    delete_project_cast_service,
    update_project_cast_service
)

router = APIRouter(prefix="/projects", tags=["Project cast"], dependencies=[Depends(get_current_user)])

@router.post("/{project_id}/cast",response_model=ProjectCastSchema)
def add_actor_to_project(project_id: int,data: ProjectCastCreateSchema,db: Session = Depends(get_db)):
    return create_project_cast_service(db,project_id,data.actor_id,data.role)


@router.get("/{project_id}/cast",response_model=list[ProjectCastSchema])
def get_project_cast(project_id: int,db: Session = Depends(get_db)):
    return get_project_cast_service(db,project_id)


@router.delete("/{project_id}/cast/{actor_id}",response_model=ProjectCastSchema)
def delete_actor_from_project(project_id: int,actor_id: int,db: Session = Depends(get_db)):
    return delete_project_cast_service(db,project_id,actor_id)

@router.put("/{project_id}/cast/{actor_id}",response_model=ProjectCastSchema)
def update_actor_role_from_project(project_id:int,actor_id:int,role:str,db: Session = Depends(get_db)):
    return update_project_cast_service(db,project_id,actor_id,role)