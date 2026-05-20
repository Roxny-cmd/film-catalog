from sqlalchemy.orm import Session
from models.models import Platform

def get_platform_by_name(db:Session, name:str):
    return db.query(Platform).filter(Platform.name == name).first()

def get_platform_by_id(db:Session, id:int):
    return db.query(Platform).filter(Platform.id == id).first()

def get_all_platforms(db:Session):
    return db.query(Platform).all()

def create_platform(db:Session, name:str):
    platform = Platform(name=name)
    db.add(platform)
    db.commit()
    db.refresh(platform)
    return platform

def delete_platform_by_id(db:Session, id:int):
    platform = db.get(Platform, id)
    db.delete(platform)
    db.commit()
    return platform

def update_platform_by_id(db:Session, id:int, name:str):
    platform = db.get(Platform, id)
    if not platform:
        return None
    platform.name = name
    db.commit()
    db.refresh(platform)
    return platform