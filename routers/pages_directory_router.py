from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt, JWTError

from database.session import get_db
from core.config import settings

from repositories.genre_repository import get_all_genres, create_genre, update_genre_by_id, delete_genre_by_id, get_genre_by_name
from repositories.director_repository import get_all_directors, create_director, update_director_by_id, delete_director_by_id, get_director_by_name
from repositories.actor_repository import get_all_actors, create_actor, update_actor_by_id, delete_actor_by_id, get_actor_by_name
from repositories.studio_repository import get_all_studios, create_studio, update_studio_by_id, delete_studio_by_id, get_studio_by_name
from repositories.country_repository import get_all_countries, create_country, update_country_by_id, delete_country_by_id, get_country_by_name
from repositories.platform_repository import get_all_platforms, create_platform, update_platform_by_id, delete_platform_by_id, get_platform_by_name

router = APIRouter(prefix="/directory", tags=["Directory Pages"])
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


def require_login(request: Request):
    if not get_user_id_from_cookie(request):
        return RedirectResponse("/auth/login", status_code=302)
    return None


def dir_response(request, title, items, add_url, edit_url, delete_url, placeholder, error=None, success=None):
    """Универсальный рендер страницы справочника."""
    return templates.TemplateResponse(
        request=request,
        name="directory/list.html",
        context={
            "title": title,
            "items": items,
            "placeholder": placeholder,
            "add_url": add_url,
            "edit_url": edit_url,
            "delete_url": delete_url,
            "error": error,
            "success": success,
        }
    )


# ════════════════════════════════════════════════
# Универсальная фабрика — все справочники одинаковы
# ════════════════════════════════════════════════

DIRECTORIES = {
    "genres": {
        "title": "Жанры",
        "placeholder": "Например: Фантастика",
        "get_all": get_all_genres,
        "get_by_name": get_genre_by_name,
        "create": create_genre,
        "update": update_genre_by_id,
        "delete": delete_genre_by_id,
    },
    "directors": {
        "title": "Режиссёры",
        "placeholder": "Например: Кристофер Нолан",
        "get_all": get_all_directors,
        "get_by_name": get_director_by_name,
        "create": create_director,
        "update": update_director_by_id,
        "delete": delete_director_by_id,
    },
    "actors": {
        "title": "Актёры",
        "placeholder": "Например: Том Хэнкс",
        "get_all": get_all_actors,
        "get_by_name": get_actor_by_name,
        "create": create_actor,
        "update": update_actor_by_id,
        "delete": delete_actor_by_id,
    },
    "studios": {
        "title": "Студии",
        "placeholder": "Например: Warner Bros",
        "get_all": get_all_studios,
        "get_by_name": get_studio_by_name,
        "create": create_studio,
        "update": update_studio_by_id,
        "delete": delete_studio_by_id,
    },
    "countries": {
        "title": "Страны",
        "placeholder": "Например: США",
        "get_all": get_all_countries,
        "get_by_name": get_country_by_name,
        "create": create_country,
        "update": update_country_by_id,
        "delete": delete_country_by_id,
    },
    "platforms": {
        "title": "Платформы",
        "placeholder": "Например: Netflix",
        "get_all": get_all_platforms,
        "get_by_name": get_platform_by_name,
        "create": create_platform,
        "update": update_platform_by_id,
        "delete": delete_platform_by_id,
    },
}


def _urls(key: str):
    return {
        "add_url": f"/directory/{key}/add",
        "edit_url": f"/directory/{key}/edit",
        "delete_url": f"/directory/{key}/delete",
    }


# ════════════════════════════════════════════════
# ЖАНРЫ
# ════════════════════════════════════════════════

@router.get("/genres", response_class=HTMLResponse)
def genres_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["genres"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("genres"), placeholder=d["placeholder"])

@router.post("/genres/add")
def genre_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["genres"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("genres"),
                            placeholder=d["placeholder"],
                            error=f'Жанр «{name}» уже существует в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("genres"),
                        placeholder=d["placeholder"],
                        success=f'Жанр «{name}» добавлен')

@router.post("/genres/edit/{id}")
def genre_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["genres"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("genres"),
                            placeholder=d["placeholder"],
                            error=f'Жанр «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/genres", status_code=302)

@router.post("/genres/delete/{id}")
def genre_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["genres"]
    d["delete"](db, id)
    return RedirectResponse("/directory/genres", status_code=302)


# ════════════════════════════════════════════════
# РЕЖИССЁРЫ
# ════════════════════════════════════════════════

@router.get("/directors", response_class=HTMLResponse)
def directors_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["directors"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("directors"), placeholder=d["placeholder"])

@router.post("/directors/add")
def director_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["directors"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("directors"),
                            placeholder=d["placeholder"],
                            error=f'Режиссёр «{name}» уже есть в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("directors"),
                        placeholder=d["placeholder"],
                        success=f'Режиссёр «{name}» добавлен')

@router.post("/directors/edit/{id}")
def director_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["directors"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("directors"),
                            placeholder=d["placeholder"],
                            error=f'Режиссёр «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/directors", status_code=302)

@router.post("/directors/delete/{id}")
def director_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    DIRECTORIES["directors"]["delete"](db, id)
    return RedirectResponse("/directory/directors", status_code=302)


# ════════════════════════════════════════════════
# АКТЁРЫ
# ════════════════════════════════════════════════

@router.get("/actors", response_class=HTMLResponse)
def actors_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["actors"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("actors"), placeholder=d["placeholder"])

@router.post("/actors/add")
def actor_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["actors"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("actors"),
                            placeholder=d["placeholder"],
                            error=f'Актёр «{name}» уже есть в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("actors"),
                        placeholder=d["placeholder"],
                        success=f'Актёр «{name}» добавлен')

@router.post("/actors/edit/{id}")
def actor_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["actors"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("actors"),
                            placeholder=d["placeholder"],
                            error=f'Актёр «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/actors", status_code=302)

@router.post("/actors/delete/{id}")
def actor_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    DIRECTORIES["actors"]["delete"](db, id)
    return RedirectResponse("/directory/actors", status_code=302)


# ════════════════════════════════════════════════
# СТУДИИ
# ════════════════════════════════════════════════

@router.get("/studios", response_class=HTMLResponse)
def studios_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["studios"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("studios"), placeholder=d["placeholder"])

@router.post("/studios/add")
def studio_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["studios"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("studios"),
                            placeholder=d["placeholder"],
                            error=f'Студия «{name}» уже есть в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("studios"),
                        placeholder=d["placeholder"],
                        success=f'Студия «{name}» добавлена')

@router.post("/studios/edit/{id}")
def studio_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["studios"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("studios"),
                            placeholder=d["placeholder"],
                            error=f'Студия «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/studios", status_code=302)

@router.post("/studios/delete/{id}")
def studio_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    DIRECTORIES["studios"]["delete"](db, id)
    return RedirectResponse("/directory/studios", status_code=302)


# ════════════════════════════════════════════════
# СТРАНЫ
# ════════════════════════════════════════════════

@router.get("/countries", response_class=HTMLResponse)
def countries_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["countries"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("countries"), placeholder=d["placeholder"])

@router.post("/countries/add")
def country_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["countries"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("countries"),
                            placeholder=d["placeholder"],
                            error=f'Страна «{name}» уже есть в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("countries"),
                        placeholder=d["placeholder"],
                        success=f'Страна «{name}» добавлена')

@router.post("/countries/edit/{id}")
def country_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["countries"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("countries"),
                            placeholder=d["placeholder"],
                            error=f'Страна «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/countries", status_code=302)

@router.post("/countries/delete/{id}")
def country_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    DIRECTORIES["countries"]["delete"](db, id)
    return RedirectResponse("/directory/countries", status_code=302)


# ════════════════════════════════════════════════
# ПЛАТФОРМЫ
# ════════════════════════════════════════════════

@router.get("/platforms", response_class=HTMLResponse)
def platforms_page(request: Request, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["platforms"]
    return dir_response(request, d["title"], d["get_all"](db), **_urls("platforms"), placeholder=d["placeholder"])

@router.post("/platforms/add")
def platform_add(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["platforms"]
    name = name.strip()
    if d["get_by_name"](db, name):
        return dir_response(request, d["title"], d["get_all"](db), **_urls("platforms"),
                            placeholder=d["placeholder"],
                            error=f'Платформа «{name}» уже есть в общем списке')
    d["create"](db, name)
    return dir_response(request, d["title"], d["get_all"](db), **_urls("platforms"),
                        placeholder=d["placeholder"],
                        success=f'Платформа «{name}» добавлена')

@router.post("/platforms/edit/{id}")
def platform_edit(request: Request, id: int, name: str = Form(...), db: Session = Depends(get_db)):
    if r := require_login(request): return r
    d = DIRECTORIES["platforms"]
    name = name.strip()
    existing = d["get_by_name"](db, name)
    if existing and existing.id != id:
        return dir_response(request, d["title"], d["get_all"](db), **_urls("platforms"),
                            placeholder=d["placeholder"],
                            error=f'Платформа «{name}» уже существует')
    d["update"](db, id, name)
    return RedirectResponse("/directory/platforms", status_code=302)

@router.post("/platforms/delete/{id}")
def platform_delete(request: Request, id: int, db: Session = Depends(get_db)):
    if r := require_login(request): return r
    DIRECTORIES["platforms"]["delete"](db, id)
    return RedirectResponse("/directory/platforms", status_code=302)
