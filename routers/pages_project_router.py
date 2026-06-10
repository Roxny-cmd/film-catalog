from fastapi import APIRouter, Request, Form, Depends, Query
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
from repositories.actor_repository import get_all_actors
from repositories.project_genre_repository import (
    create_project_genre, get_project_genres, delete_project_genre
)
from repositories.project_platform_repository import (
    create_project_platform, get_project_platforms, delete_project_platform
)
from repositories.project_cast_repository import (
    create_project_cast, get_project_cast,
    delete_project_cast_member
)

router = APIRouter(tags=["Project Pages"])
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


def form_context(db: Session, project=None, error=None):
    cast_entries = get_project_cast(db, project.id) if project else []
    return {
        "project": project,
        "directors": get_all_directors(db),
        "studios": get_all_studios(db),
        "countries": get_all_countries(db),
        "genres": get_all_genres(db),
        "platforms": get_all_platforms(db),
        "actors": get_all_actors(db),
        "cast_entries": cast_entries,
        "error": error,
    }


def save_relations(db, project_id, genre_ids, platform_ids, cast_actor_ids, cast_roles):
    for pg in get_project_genres(db, project_id):
        delete_project_genre(db, project_id, pg.genre_id)
    for gid in (genre_ids or []):
        create_project_genre(db, project_id, gid)

    for pp in get_project_platforms(db, project_id):
        delete_project_platform(db, project_id, pp.platform_id)
    for pid in (platform_ids or []):
        create_project_platform(db, project_id, pid)

    for cast in get_project_cast(db, project_id):
        delete_project_cast_member(db, project_id, cast.actor_id)

    seen = set()
    for actor_id, role in zip(cast_actor_ids or [], cast_roles or []):
        if not actor_id or not role.strip() or actor_id in seen:
            continue
        seen.add(actor_id)
        create_project_cast(db, project_id, actor_id, role.strip())


def apply_filters(projects, search, project_type, genre_id, country_id,
                  director_id, actor_id, year_from, year_to):
    if search:
        s = search.lower()
        projects = [p for p in projects if s in p.title.lower()]
    if project_type:
        projects = [p for p in projects if p.project_type == project_type]
    if genre_id:
        gid = int(genre_id)
        projects = [p for p in projects if any(g.id == gid for g in p.genres)]
    if country_id:
        cid = int(country_id)
        projects = [p for p in projects if p.country_id == cid]
    if director_id:
        did = int(director_id)
        projects = [p for p in projects if p.director_id == did]
    if actor_id:
        aid = int(actor_id)
        projects = [p for p in projects if any(c.actor_id == aid for c in p.casts)]
    if year_from:
        projects = [p for p in projects if p.date_of_release.year >= int(year_from)]
    if year_to:
        projects = [p for p in projects if p.date_of_release.year <= int(year_to)]
    return projects


# ───── Главная с фильтрами ─────

@router.get("/", response_class=HTMLResponse)
def catalog(
    request: Request,
    db: Session = Depends(get_db),
    search:       Optional[str] = Query(default=None),
    project_type: Optional[str] = Query(default=None),
    genre_id:     Optional[str] = Query(default=None),
    country_id:   Optional[str] = Query(default=None),
    director_id:  Optional[str] = Query(default=None),
    actor_id:     Optional[str] = Query(default=None),
    year_from:    Optional[str] = Query(default=None),
    year_to:      Optional[str] = Query(default=None),
):
    all_projects = get_all_projects(db)
    total = len(all_projects)

    filtered = apply_filters(
        all_projects, search, project_type,
        genre_id, country_id, director_id, actor_id,
        year_from, year_to
    )

    return templates.TemplateResponse(
        request=request,
        name="projects/index.html",
        context={
            "projects": filtered,
            "total": total,
            "all_genres":    get_all_genres(db),
            "all_countries": get_all_countries(db),
            "all_directors": get_all_directors(db),
            "all_actors":    get_all_actors(db),
            "filters": {
                "search":      search,
                "project_type": project_type,
                "genre_id":    genre_id,
                "country_id":  country_id,
                "director_id": director_id,
                "actor_id":    actor_id,
                "year_from":   year_from,
                "year_to":     year_to,
            },
        }
    )


# ───── Мои фильмы ─────

@router.get("/my", response_class=HTMLResponse)
def my_projects(request: Request, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="projects/my_projects.html",
        context={"projects": get_projects_by_owner(db, user_id)}
    )


# ───── Создание — ВЫШЕ /{id} ─────

@router.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request, db: Session = Depends(get_db)):
    if not get_user_id_from_cookie(request):
        return RedirectResponse("/auth/login", status_code=302)
    return templates.TemplateResponse(
        request=request,
        name="projects/form.html",
        context=form_context(db)
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
    cast_actor_ids: Optional[List[int]] = Form(default=None),
    cast_roles: Optional[List[str]] = Form(default=None),
):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    try:
        from datetime import date
        data = {
            "title": title, "project_type": project_type,
            "date_of_release": date.fromisoformat(date_of_release),
            "rating": rating, "description": description or None,
            "director_id": director_id or None,
            "studio_id": studio_id or None,
            "country_id": country_id or None,
            "owner_id": user_id,
        }
        project = create_project(db, data)
        save_relations(db, project.id, genre_ids, platform_ids, cast_actor_ids, cast_roles)
        return RedirectResponse(f"/projects/{project.id}", status_code=302)
    except Exception as e:
        return templates.TemplateResponse(
            request=request, name="projects/form.html",
            context=form_context(db, error=f"Ошибка: {e}")
        )


# ───── Редактирование ─────

@router.get("/projects/{id}/edit", response_class=HTMLResponse)
def edit_project_page(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(
        request=request, name="projects/form.html",
        context=form_context(db, project)
    )


@router.post("/projects/{id}/edit")
def edit_project_submit(
    request: Request, id: int,
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
    cast_actor_ids: Optional[List[int]] = Form(default=None),
    cast_roles: Optional[List[str]] = Form(default=None),
):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if not project or project.owner_id != user_id:
        return RedirectResponse("/", status_code=302)
    try:
        from datetime import date
        data = {
            "title": title, "project_type": project_type,
            "date_of_release": date.fromisoformat(date_of_release),
            "rating": rating, "description": description or None,
            "director_id": director_id or None,
            "studio_id": studio_id or None,
            "country_id": country_id or None,
        }
        update_project_by_id(db, id, data)
        save_relations(db, id, genre_ids, platform_ids, cast_actor_ids, cast_roles)
        return RedirectResponse(f"/projects/{id}", status_code=302)
    except Exception as e:
        return templates.TemplateResponse(
            request=request, name="projects/form.html",
            context=form_context(db, project, error=f"Ошибка: {e}")
        )


# ───── Детальная — НИЖЕ /new и /edit ─────

@router.get("/projects/{id}", response_class=HTMLResponse)
def project_detail(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    project = get_project_by_id(db, id)
    if not project:
        return templates.TemplateResponse(
            request=request, name="projects/index.html",
            context={"projects": [], "total": 0, "all_genres": [],
                     "all_countries": [], "all_directors": [], "all_actors": [],
                     "filters": {}, "error": "Фильм не найден"}
        )
    return templates.TemplateResponse(
        request=request, name="projects/detail.html",
        context={"project": project, "is_owner": user_id == project.owner_id}
    )


# ───── Удаление ─────

@router.post("/projects/{id}/delete")
def delete_project(request: Request, id: int, db: Session = Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    if not user_id:
        return RedirectResponse("/auth/login", status_code=302)
    project = get_project_by_id(db, id)
    if project and project.owner_id == user_id:
        delete_project_by_id(db, id)
    return RedirectResponse("/my", status_code=302)
