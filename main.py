from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# API роутеры
from routers.director_router import router as director_router
from routers.studio_router import router as studio_router
from routers.actor_router import router as actor_router
from routers.project_router import router as project_router
from routers.country_router import router as country_router
from routers.project_cast_router import router as project_cast_router
from routers.genre_router import router as genre_router
from routers.platform_router import router as platform_router
from routers.project_genre_router import router as project_genre_router
from routers.project_platform_router import router as project_platform_router  # имя файла исправлено
from routers.auth_router import router as auth_api_router

# Роутеры страниц (Jinja2)
from routers.pages_auth_router import router as pages_auth_router
from routers.pages_project_router import router as pages_project_router

app = FastAPI(
    title="Film Catalog",
    description="Каталог фильмов и сериалов",
    version="1.0.0"
)

# Статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Страницы (Jinja2) — регистрируем ПЕРВЫМИ ──
app.include_router(pages_auth_router)
app.include_router(pages_project_router)

# ── API роутеры (под /api префиксом чтобы не конфликтовать) ──
app.include_router(auth_api_router, prefix="/api")
app.include_router(director_router, prefix="/api")
app.include_router(studio_router, prefix="/api")
app.include_router(actor_router, prefix="/api")
app.include_router(country_router, prefix="/api")
app.include_router(genre_router, prefix="/api")
app.include_router(platform_router, prefix="/api")
app.include_router(project_router, prefix="/api")
app.include_router(project_cast_router, prefix="/api")
app.include_router(project_genre_router, prefix="/api")
app.include_router(project_platform_router, prefix="/api")
