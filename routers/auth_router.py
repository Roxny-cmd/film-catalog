from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.auth_schema import LoginSchema, RegisterSchema
from schemas.token_schema import TokenSchema
from services.auth_service import authenticate_user, register_user
from database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenSchema)
def login(data:LoginSchema, db: Session = Depends(get_db)):
    token = authenticate_user(db, data.email, data.password)
    if not token:
        raise HTTPException(status_code=404, detail="Incorrect email or password")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=TokenSchema)
def register(data:RegisterSchema, db: Session = Depends(get_db)):
    token = register_user(db, data.email, data.password)
    if not token:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"access_token": token, "token_type": "bearer"}