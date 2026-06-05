from sqlalchemy.orm import Session
from models.user import User

def get_user_by_id(db: Session, id: int):
    return db.get(User, id)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, email: str, hashed_password: str):
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, id: int, data: dict):
    user = db.get(User, id)
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: int):
    user = db.get(User, id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user