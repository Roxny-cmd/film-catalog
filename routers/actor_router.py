from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from schemas.actor import ActorCreateSchema, ActorSchema
from services.actor_service import (
    create_actor_service,
    get_all_actors_service,
    delete_actor_service,
    get_actor_by_name_service,
    update_actor_service,
    get_actor_by_id_service
)

router = APIRouter(prefix='/actors', tags=['Actors'], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ActorSchema)
def add_actor(data: ActorCreateSchema, db: Session = Depends(get_db)):
    return create_actor_service(db, data.name)

@router.get("/", response_model=list[ActorSchema])
def get_actors(db: Session = Depends(get_db)):
    return get_all_actors_service(db)

@router.get("/search", response_model=ActorSchema)
def search_actor(name:str, db: Session = Depends(get_db)):
    return get_actor_by_name_service(db, name)

@router.get("/{id}", response_model=ActorSchema)
def get_actor_by_id(id: int, db: Session = Depends(get_db)):
    return get_actor_by_id_service(db, id)

@router.delete("/{id}", response_model=ActorSchema)
def delete_actor(id: int, db: Session = Depends(get_db)):
    return delete_actor_service(db, id)

@router.put("/{id}", response_model=ActorSchema)
def update_actor(id:int, data:ActorCreateSchema, db: Session = Depends(get_db)):
    return update_actor_service(db, id, data.name)