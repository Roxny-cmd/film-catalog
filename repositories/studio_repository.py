from sqlalchemy.orm import Session
from models.models import Studio

def get_studio_by_name(db:Session, name:str):
    return db.query(Studio).filter(Studio.name == name).first()

def get_studio_by_id(db:Session, id:int):
    return db.query(Studio).filter(Studio.id == id).first()

def get_all_studios(db:Session):
    return db.query(Studio).all()

def create_studio(db:Session, name:str):
    studio = Studio(name=name)
    db.add(studio)
    db.commit()
    db.refresh(studio)
    return studio

def delete_studio_by_id(db:Session, id:int):
    studio = db.get(Studio, id)
    db.delete(studio)
    db.commit()
    return studio

def update_studio_by_id(db:Session, id:int, name:str):
    studio = db.get(Studio, id)
    if not studio:
        return None
    studio.name = name
    db.commit()
    db.refresh(studio)
    return studio