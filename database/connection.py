from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('postgresql://postgres:Roxn1--Y@localhost:5432/film_catalog')
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
