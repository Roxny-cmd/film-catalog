from fastapi import HTTPException

from repositories.user_repository import get_user_by_email, create_user
from core.password import verify_password, hash_password
from core.security import create_access_token

def authenticate_user(db,email:str, password:str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({"sub": str(user.id)})
    return token

def register_user(db,email, password):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(password)
    user = create_user(db, email, hashed)
    token = create_access_token({"sub": str(user.id)})
    return token