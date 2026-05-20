from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.director import DirectorCreateSchema, DirectorSchema
from services.director_service import (
    create_director_service,
    get_all_director_service,
    delete_director_service,
    get_director_by_name_service,
    update_director_service,
    get_director_by_id_service
)

router = APIRouter(prefix='/directors', tags=['Directors'], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=DirectorSchema)
def add_director(data: DirectorCreateSchema, db: Session = Depends(get_db)):
    return create_director_service(db, data.name)

@router.get("/", response_model=list[DirectorSchema])
def get_directors(db: Session = Depends(get_db)):
    return get_all_director_service(db)

@router.get("/search", response_model=DirectorSchema)
def search_director(name:str, db: Session = Depends(get_db)):
    return get_director_by_name_service(db, name)

@router.get("/{id}", response_model=DirectorSchema)
def get_director_by_id(id: int, db: Session = Depends(get_db)):
    return get_director_by_id_service(db, id)

@router.delete("/{id}", response_model=DirectorSchema)
def delete_director(id: int, db: Session = Depends(get_db)):
    return delete_director_service(db, id)

@router.put("/{id}", response_model=DirectorSchema)
def update_director(id:int, data:DirectorCreateSchema, db: Session = Depends(get_db)):
    return update_director_service(db, id, data.name)