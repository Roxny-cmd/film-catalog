from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.genre import GenreSchema, GenreCreateSchema
from services.genre_service import (
    get_all_genres_service,
    get_genre_by_id_service,
    get_genre_by_name_service,
    create_genre_service,
    update_genre_service,
    delete_genre_service
)

router = APIRouter(prefix="/genre", tags=["Genre"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=GenreSchema)
def add_genre(data: GenreCreateSchema, db: Session = Depends(get_db)):
    return create_genre_service(db, data.name)

@router.get("/", response_model=list[GenreSchema])
def get_genres(db: Session = Depends(get_db)):
    return get_all_genres_service(db)

@router.get("/search", response_model=GenreSchema)
def search_genre(name:str, db: Session = Depends(get_db)):
    return get_genre_by_name_service(db, name)

@router.get("/{id}", response_model=GenreSchema)
def get_genre_by_id(id: int, db: Session = Depends(get_db)):
    return get_genre_by_id_service(db, id)

@router.delete("/{id}", response_model=GenreSchema)
def delete_Genre(id: int, db: Session = Depends(get_db)):
    return delete_genre_service(db, id)

@router.put("/{id}", response_model=GenreSchema)
def update_Genre(id:int, data:GenreCreateSchema, db: Session = Depends(get_db)):
    return update_genre_service(db, id, data.name)