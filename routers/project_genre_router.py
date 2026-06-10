from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from core.dependencies import get_current_user
from schemas.project_genre import (
    ProjectGenreCreateSchema,
    ProjectGenreSchema
)

from services.project_genre_service import (
    create_project_genre_service,
    get_project_genres_service,
    delete_project_genre_service
)

router = APIRouter(prefix="/projects",tags=["Project Genres"], dependencies=[Depends(get_current_user)])


@router.post("/{project_id}/genres",response_model=ProjectGenreSchema)
def add_genre_to_project(project_id: int,data: ProjectGenreCreateSchema,db: Session = Depends(get_db)):
    return create_project_genre_service(db,project_id,data.genre_id)


@router.get("/{project_id}/genres",response_model=list[ProjectGenreSchema])
def get_project_genres(project_id: int,db: Session = Depends(get_db)):
    return get_project_genres_service(db,project_id)


@router.delete("/{project_id}/genres/{genre_id}",response_model=ProjectGenreSchema)
def delete_project_genre(project_id: int,genre_id: int,db: Session = Depends(get_db)):
    return delete_project_genre_service(db,project_id,genre_id)