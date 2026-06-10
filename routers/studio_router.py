from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.studio import StudioSchema, StudioCreateSchema
from services.studio_service import (
    get_all_studios_service,
    get_studio_by_id_service,
    get_studio_by_name_service,
    create_studio_service,
    update_studio_service,
    delete_studio_service
)

router = APIRouter(prefix="/studio", tags=["Studio"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=StudioSchema)
def add_studio(data: StudioCreateSchema, db: Session = Depends(get_db)):
    return create_studio_service(db, data.name)

@router.get("/", response_model=list[StudioSchema])
def get_studios(db: Session = Depends(get_db)):
    return get_all_studios_service(db)

@router.get("/search", response_model=StudioSchema)
def search_studio(name:str, db: Session = Depends(get_db)):
    return get_studio_by_name_service(db, name)

@router.get("/{id}", response_model=StudioSchema)
def get_studio_by_id(id: int, db: Session = Depends(get_db)):
    return get_studio_by_id_service(db, id)

@router.delete("/{id}", response_model=StudioSchema)
def delete_Studio(id: int, db: Session = Depends(get_db)):
    return delete_studio_service(db, id)

@router.put("/{id}", response_model=StudioSchema)
def update_Studio(id:int, data:StudioCreateSchema, db: Session = Depends(get_db)):
    return update_studio_service(db, id, data.name)