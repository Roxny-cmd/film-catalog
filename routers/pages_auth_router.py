from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.session import get_db
from services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["Auth Pages"])
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth/login.html", context={})


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        token = authenticate_user(db, username, password)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="token", value=token, httponly=True, max_age=3600, samesite="lax")
        return response
    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": "Неверный email или пароль"}
        )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="auth/register.html", context={})


@router.post("/register")
def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        token = register_user(db, username, email, password)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key="token", value=token, httponly=True, max_age=3600, samesite="lax")
        return response
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={"error": str(e.detail) if hasattr(e, 'detail') else "Ошибка при регистрации"}
        )


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("token")
    return response
