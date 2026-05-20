from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from schemas.auth_schema import LoginSchema, RegisterSchema
from schemas.token_schema import TokenSchema
from services.auth_service import authenticate_user, register_user
from database.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    token = authenticate_user(db,form_data.username,form_data.password)

    if not token:
        raise HTTPException(status_code=401,detail="Incorrect email or password")

    return {"access_token": token,"token_type": "bearer"}

@router.post("/register", response_model=TokenSchema)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    token = register_user(db, data.email, data.password)
    return {"access_token": token,"token_type": "bearer"}