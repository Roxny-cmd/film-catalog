from sqlalchemy.orm import Session
from models.models import Country

def get_country_by_name(db:Session, name:str):
    return db.query(Country).filter(Country.name == name).first()

def get_country_by_id(db:Session, id:int):
    return db.query(Country).filter(Country.id == id).first()

def create_country(db:Session, name: str):
    country = Country(name=name)
    db.add(country)
    db.commit()
    db.refresh(country)
    return country

def get_all_countries(db:Session):
    return db.query(Country).all()

def delete_country_by_id(db:Session, id:int):
    country = get_country_by_id(db, id)
    db.delete(country)
    db.commit()
    return country

def update_country_by_id(db:Session, id:int, name:str):
    country = db.get(Country, id)
    if not country:
        return None
    country.name = name
    db.commit()
    db.refresh(country)
    return country
