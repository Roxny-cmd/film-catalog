from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(
    URL.create(
        drivername="postgresql+psycopg2",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    ),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
