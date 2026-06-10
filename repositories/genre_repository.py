from sqlalchemy.orm import Session
from models.models import Genre

def get_genre_by_name(db:Session, name:str):
    return db.query(Genre).filter(Genre.name == name).first()

def get_genre_by_id(db:Session, id:int):
    return db.query(Genre).filter(Genre.id == id).first()

def get_all_genres(db:Session):
    return db.query(Genre).all()

def create_genre(db:Session, name:str):
    genre = Genre(name=name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre

def delete_genre_by_id(db:Session, id:int):
    genre = db.get(Genre, id)
    db.delete(genre)
    db.commit()
    return genre

def update_genre_by_id(db:Session, id:int, name:str):
    genre = db.get(Genre, id)
    if not genre:
        return None
    genre.name = name
    db.commit()
    db.refresh(genre)
    return genre