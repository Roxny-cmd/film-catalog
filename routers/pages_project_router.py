from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
from jose import jwt, JWTError

from database.session import get_db
from core.config import settings
from repositories.project_repository import (
    get_all_projects, get_project_by_id, get_projects_by_owner,
    create_project, update_project_by_id, delete_project_by_id
)
from repositories.director_repository import get_all_directors
from repositories.studio_repository import get_all_studios
from repositories.country_repository import get_all_countries
from repositories.genre_repository import get_all_genres
from repositories.platform_repository import get_all_platforms
from repositories.project_genre_repository import create_project_genre, get_project_genres, delete_project_genre
from repositories.project_platform_repository import create_project_platform, get_project_platforms, delete_project_platform

router = APIRouter(tags=["Project Pages"])
templates = Jinja2Templates(directory="templates")


def get_user_id_from_cookie(token: Optional[str] = None) -> Optional[int]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        return int(user_id) if user_id else None
    except JWTError:
        return None


@router.get("/", response_class=HTMLResponse)
def catalog(request: Request, search: Optional[str] = None, db: Session = Depends(get_db)):
    projects = get_all_projects(db)
    if search:
        search_lower = search.lower()
        projects = [p for p in projects if search_lower in p.title.lower()]
    return templates.TemplateResponse(
        request=request,
        name="projects/index.html",
        context={"projects": projects, "search": search}
    )


@router.get("/my", response_class=HTMLResponse)
def my_projects(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    projects = get_projects_by_owner(db, user_id)
    return templates.TemplateResponse(
        request=request,
        name="projects/my_projects.html",
        context={"projects": projects}
    )


@router.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request, db: Session = Depends(get_db)):
    if not get_user_id_from_cookie(request.cookies.get("token")):
        return RedirectResponse("/auth/login", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="projects/form.html",
        context={
            "project": None,
            "directors": get_all_directors(db),
            "studios": get_all_studios(db),
            "countries": get_all_countries(db),
            "genres": get_all_genres(db),
            "platforms": get_all_platforms(db),
        }
    )


@router.post("/projects/new")
def new_project_submit(
    request: Request,
    db: Session = Depends(get_db),
    title: str = Form(...),
    project_type: str = Form(...),
    date_of_release: str = Form(...),
    rating: float = Form(...),
    description: Optional[str] = Form(default=None),
    director_id: Optional[int] = Form(default=None),
    studio_id: Optional[int] = Form(default=None),
    country_id: Optional[int] = Form(default=None),
    genre_ids: Optional[List[int]] = Form(default=None),
    platform_ids: Optional[List[int]] = Form(default=None),
):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    try:
        from datetime import date
        data = {
            "title": title,
            "project_type": project_type,
            "date_of_release": date.fromisoformat(date_of_release),
            "rating": rating,
            "description": description or None,
            "director_id": director_id or None,
            "studio_id": studio_id or None,
            "country_id": country_id or None,
            "owner_id": user_id
        }
        project = create_project(db, data)
        for gid in (genre_ids or []):
            create_project_genre(db, project.id, gid)
        for pid in (platform_ids or []):
            create_project_platform(db, project.id, pid)
        return RedirectResponse(f"/projects/{project.id}", status_code=302)
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="projects/form.html",
            context={
                "project": None,
                "directors": get_all_directors(db),
                "studios": get_all_studios(db),
                "countries": get_all_countries(db),
                "genres": get_all_genres(db),
                "platforms": get_all_platforms(db),
                "error": f"Ошибка при создании: {str(e)}"
            }
        )


@router.get("/projects/{id}/edit", response_class=HTMLResponse)
def edit_project_page(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="projects/form.html",
        context={
            "project": project,
            "directors": get_all_directors(db),
            "studios": get_all_studios(db),
            "countries": get_all_countries(db),
            "genres": get_all_genres(db),
            "platforms": get_all_platforms(db),
        }
    )


@router.post("/projects/{id}/edit")
def edit_project_submit(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    project_type: str = Form(...),
    date_of_release: str = Form(...),
    rating: float = Form(...),
    description: Optional[str] = Form(default=None),
    director_id: Optional[int] = Form(default=None),
    studio_id: Optional[int] = Form(default=None),
    country_id: Optional[int] = Form(default=None),
    genre_ids: Optional[List[int]] = Form(default=None),
    platform_ids: Optional[List[int]] = Form(default=None),
):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)
    try:
        from datetime import date
        data = {
            "title": title,
            "project_type": project_type,
            "date_of_release": date.fromisoformat(date_of_release),
            "rating": rating,
            "description": description or None,
            "director_id": director_id or None,
            "studio_id": studio_id or None,
            "country_id": country_id or None,
        }
        update_project_by_id(db, id, data)
        for pg in get_project_genres(db, id):
            delete_project_genre(db, id, pg.genre_id)
        for gid in (genre_ids or []):
            create_project_genre(db, id, gid)
        for pp in get_project_platforms(db, id):
            delete_project_platform(db, id, pp.platform_id)
        for pid in (platform_ids or []):
            create_project_platform(db, id, pid)
        return RedirectResponse(f"/projects/{id}", status_code=302)
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="projects/form.html",
            context={
                "project": project,
                "directors": get_all_directors(db),
                "studios": get_all_studios(db),
                "countries": get_all_countries(db),
                "genres": get_all_genres(db),
                "platforms": get_all_platforms(db),
                "error": f"Ошибка при сохранении: {str(e)}"
            }
        )


@router.get("/projects/{id}", response_class=HTMLResponse)
def project_detail(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    project = get_project_by_id(db, id)
    if not project:
        return templates.TemplateResponse(
            request=request,
            name="projects/index.html",
            context={"projects": [], "error": "Фильм не найден"}
        )
    return templates.TemplateResponse(
        request=request,
        name="projects/detail.html",
        context={"project": project, "is_owner": user_id == project.owner_id}
    )


@router.post("/projects/{id}/delete")
def delete_project(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request.cookies.get("token"))
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if project and project.owner_id == user_id:
        delete_project_by_id(db, id)
    return RedirectResponse("/my", status_code=302)
