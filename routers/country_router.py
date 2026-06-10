from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.country import CountryCreateSchema, CountrySchema
from services.country_service import (
    create_country_service,
    get_all_countries_service,
    delete_country_service,
    get_country_by_name_service,
    update_country_service,
    get_country_by_id_service
)

router = APIRouter(prefix='/countries', tags=['Countries'], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=CountrySchema)
def add_country(data: CountryCreateSchema, db: Session = Depends(get_db)):
    return create_country_service(db, data.name)

@router.get("/", response_model=list[CountrySchema])
def get_countries(db: Session = Depends(get_db)):
    return get_all_countries_service(db)

@router.get("/search", response_model=CountrySchema)
def search_country(name:str, db: Session = Depends(get_db)):
    return get_country_by_name_service(db, name)

@router.get("/{id}", response_model=CountrySchema)
def get_country_by_id(id: int, db: Session = Depends(get_db)):
    return get_country_by_id_service(db, id)

@router.delete("/{id}", response_model=CountrySchema)
def delete_country(id: int, db: Session = Depends(get_db)):
    return delete_country_service(db, id)

@router.put("/{id}", response_model=CountrySchema)
def update_country(id:int, data:CountryCreateSchema, db: Session = Depends(get_db)):
    return update_country_service(db, id, data.name)