from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.platform import PlatformSchema, PlatformCreateSchema
from services.platform_service import (
    get_all_platforms_service,
    get_platform_by_id_service,
    get_platform_by_name_service,
    create_platform_service,
    update_platform_service,
    delete_platform_service
)

router = APIRouter(prefix="/platform", tags=["Platform"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=PlatformSchema)
def add_platform(data: PlatformCreateSchema, db: Session = Depends(get_db)):
    return create_platform_service(db, data.name)

@router.get("/", response_model=list[PlatformSchema])
def get_platforms(db: Session = Depends(get_db)):
    return get_all_platforms_service(db)

@router.get("/search", response_model=PlatformSchema)
def search_platform(name:str, db: Session = Depends(get_db)):
    return get_platform_by_name_service(db, name)

@router.get("/{id}", response_model=PlatformSchema)
def get_platform_by_id(id: int, db: Session = Depends(get_db)):
    return get_platform_by_id_service(db, id)

@router.delete("/{id}", response_model=PlatformSchema)
def delete_Platform(id: int, db: Session = Depends(get_db)):
    return delete_platform_service(db, id)

@router.put("/{id}", response_model=PlatformSchema)
def update_Platform(id:int, data:PlatformCreateSchema, db: Session = Depends(get_db)):
    return update_platform_service(db, id, data.name)