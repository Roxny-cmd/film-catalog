from sqlalchemy.orm import Session
from models.models import Actor

def get_actor_by_name(db:Session, name:str):
    return db.query(Actor).filter(Actor.name == name).first()

def get_actor_by_id(db:Session, id:int):
    return db.query(Actor).filter(Actor.id == id).first()

def create_actor(db:Session, name: str):
    actor = Actor(name=name)
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor

def get_all_actors(db:Session):
    return db.query(Actor).all()

def delete_actor_by_id(db:Session, id:int):
    actor = get_actor_by_id(db, id)
    db.delete(actor)
    db.commit()
    return actor

def update_actor_by_id(db:Session, id:int, name:str):
    actor = db.get(Actor, id)
    if not actor:
        return None
    actor.name = name
    db.commit()
    db.refresh(actor)
    return actor
