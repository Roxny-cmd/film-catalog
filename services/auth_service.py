from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.user_repository import get_user_by_email, create_user
from core.password import verify_password, hash_password
from core.security import create_access_token

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id)})
    return token

def register_user(db: Session, username: str, email: str, password: str):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(password)
    user = create_user(db, username=username, email=email, hashed_password=hashed)
    token = create_access_token({"sub": str(user.id)})
    return token