from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt, JWTError

from database.session import get_db
from core.config import settings
from repositories.project_repository import get_project_by_id
from repositories.actor_repository import get_all_actors
from repositories.project_cast_repository import (
    get_project_cast, get_project_cast_member,
    create_project_cast, delete_project_cast_member,
    update_project_cast_member_role
)

router = APIRouter(tags=["Cast Pages"])
templates = Jinja2Templates(directory="templates")


def get_user_id_from_cookie(request: Request) -> Optional[int]:
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        uid = payload.get("sub")
        return int(uid) if uid else None
    except JWTError:
        return None


def cast_response(request, project, casts, all_actors, cast_actor_ids, cast_error=None):
    """Универсальный рендер страницы состава."""
    return templates.TemplateResponse(
        request=request,
        name="projects/cast.html",
        context={
            "project": project,
            "casts": casts,
            "all_actors": all_actors,
            "cast_actor_ids": cast_actor_ids,
            "cast_error": cast_error,
        }
    )


@router.get("/projects/{id}/cast", response_class=HTMLResponse)
def cast_page(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)

    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)

    casts = get_project_cast(db, id)
    return cast_response(
        request, project, casts,
        get_all_actors(db),
        {c.actor_id for c in casts}
    )


@router.post("/projects/{id}/cast/add")
def cast_add(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    actor_id: int = Form(...),
    role: str = Form(...),
):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)

    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)

    role = role.strip()
    casts = get_project_cast(db, id)
    cast_actor_ids = {c.actor_id for c in casts}

    # Проверка дубля
    if actor_id in cast_actor_ids:
        return cast_response(
            request, project, casts,
            get_all_actors(db), cast_actor_ids,
            cast_error="Этот актёр уже есть в составе фильма"
        )

    create_project_cast(db, id, actor_id, role)
    return RedirectResponse(f"/projects/{id}/cast", status_code=302)


@router.post("/projects/{id}/cast/{actor_id}/edit")
def cast_edit(
    request: Request,
    id: int,
    actor_id: int,
    db: Session = Depends(get_db),
    role: str = Form(...),
):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)

    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)

    role = role.strip()
    update_project_cast_member_role(db, id, actor_id, role)
    return RedirectResponse(f"/projects/{id}/cast", status_code=302)


@router.post("/projects/{id}/cast/{actor_id}/delete")
def cast_delete(request: Request, id: int, actor_id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)

    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)

    if get_project_cast_member(db, id, actor_id):
        delete_project_cast_member(db, id, actor_id)

    return RedirectResponse(f"/projects/{id}/cast", status_code=302)
