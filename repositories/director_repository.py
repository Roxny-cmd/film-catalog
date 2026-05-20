from sqlalchemy.orm import Session
from models.models import Director

def get_director_by_name(db:Session, name:str):
    return db.query(Director).filter(Director.name == name).first()

def get_director_by_id(db:Session, id:int):
    return db.query(Director).filter(Director.id == id).first()

def create_director(db:Session, name: str):
    director = Director(name=name)
    db.add(director)
    db.commit()
    db.refresh(director)
    return director

def get_all_directors(db:Session):
    return db.query(Director).all()

def delete_director_by_id(db:Session, id:int):
    director = get_director_by_id(db, id)
    db.delete(director)
    db.commit()
    return director

def update_director_by_id(db:Session, id:int, name:str):
    director = db.get(Director, id)
    if not director:
        return None
    director.name = name
    db.commit()
    db.refresh(director)
    return director
