from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.project import (ProjectCreateSchema,ProjectSchema)
from services.project_service import (
    create_project_service,
    get_all_projects_service,
    get_project_by_id_service,
    get_project_by_name_service,
    update_project_service,
    delete_project_service
)

router = APIRouter(prefix="/projects",tags=["Projects"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ProjectSchema)
def add_project(data: ProjectCreateSchema,db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return create_project_service(db,data.model_dump(), user_id)


@router.get("/", response_model=list[ProjectSchema])
def get_projects(db: Session = Depends(get_db)):
    return get_all_projects_service(db)

@router.get("/search", response_model=ProjectSchema)
def search_project(name:str, db: Session = Depends(get_db)):
    return get_project_by_name_service(db, name)

@router.get("/{id}", response_model=ProjectSchema)
def get_project_by_id(id: int, db: Session = Depends(get_db)):
    return get_project_by_id_service(db, id)

@router.delete("/{id}", response_model=ProjectSchema)
def delete_Project(id: int, db: Session = Depends(get_db)):
    return delete_project_service(db, id)

@router.put("/{id}", response_model=ProjectSchema)
def update_Project(id:int, data:ProjectCreateSchema, db: Session = Depends(get_db)):
    return update_project_service(db, id, data.name)
