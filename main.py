from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.director_router import router as director_router
from routers.studio_router import router as studio_router
from routers.actor_router import router as actor_router
from routers.project_router import router as project_router
from routers.country_router import router as country_router
from routers.project_cast_router import router as project_cast_router
from routers.genre_router import router as genre_router
from routers.platform_router import router as platform_router
from routers.project_genre_router import router as project_genre_router
from routers.project_platform_router import router as project_platform_router
from routers.auth_router import router as auth_router

app = FastAPI(
    title="Film Catalog",
    description="Каталог фильмов и сериалов",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(director_router)
app.include_router(studio_router)
app.include_router(actor_router)
app.include_router(country_router)
app.include_router(genre_router)
app.include_router(platform_router)
app.include_router(project_router)
app.include_router(project_cast_router)
app.include_router(project_genre_router)
app.include_router(project_platform_router)