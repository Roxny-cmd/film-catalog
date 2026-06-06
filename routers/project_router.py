from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from models.user import User
from schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectSchema
from services.project_service import (
    create_project_service,
    get_all_projects_service,
    get_project_by_id_service,
    get_project_by_title_service,   # переименованный
    get_my_projects_service,        # новый
    update_project_service,
    delete_project_service
)

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectSchema)
def add_project(
    data: ProjectCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_project_service(db, data.model_dump(), current_user.id)

@router.get("/", response_model=list[ProjectSchema])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_projects_service(db)

@router.get("/my", response_model=list[ProjectSchema])   # новый — личный каталог
def get_my_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_my_projects_service(db, current_user.id)

@router.get("/search", response_model=ProjectSchema)
def search_project(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_by_title_service(db, title)

@router.get("/{id}", response_model=ProjectSchema)
def get_project_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_by_id_service(db, id)

@router.delete("/{id}", response_model=ProjectSchema)
def delete_project(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_project_service(db, id, current_user.id)  # передаём owner_id

@router.put("/{id}", response_model=ProjectSchema)
def update_project(
    id: int,
    data: ProjectUpdateSchema,                              # используем UpdateSchema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_project_service(db, id, data.model_dump(exclude_unset=True), current_user.id)