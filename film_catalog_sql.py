from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from sqlalchemy.exc import SQLAlchemyError


engine = create_engine('postgresql://postgres:Roxn1--Y@localhost/film_catalog')
Base = declarative_base()

# Models
class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("Project", back_populates="director")

class Studio(Base):
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("Project", back_populates="studio")

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("Project", secondary="project_genre", back_populates="genres")

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)



class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("Project", secondary="project_on_platform", back_populates="platforms")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False, index=True)
    project_type = Column(String(256), nullable=False)
    date_of_release = Column(Date, nullable=False)
    rating = Column(Numeric(3,1), nullable=False)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey('directors.id', ondelete='SET NULL') )
    studio_id = Column(Integer, ForeignKey('studios.id', ondelete='SET NULL') )
    country_id = Column(Integer, ForeignKey('countries.id', ondelete='SET NULL') )

    __table_args__ = (
        CheckConstraint("project_type IN ('film', 'serial')", name='check_film_or_serial'),
        CheckConstraint("rating >= 0 AND rating <= 10", name='check_rating'),
    )

    director = relationship("Director", back_populates="projects")
    studio = relationship("Studio", back_populates="projects")
    genres = relationship("Genre", secondary="project_genre", back_populates="projects")
    platforms = relationship("Platform", secondary="project_on_platform", back_populates="projects")

class ProjectCast(Base):
    __tablename__ = 'project_cast'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True)

    role = Column(String(256), nullable=False)

class ProjectGenre(Base):
    __tablename__ = 'project_genre'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)

class ProjectOnPlatform(Base):
    __tablename__ = 'project_on_platform'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"), primary_key=True)

# Create Tables
Base.metadata.create_all(engine)

# Session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# CRUD

# CRUD FOR DIRECTORS
# CREATE
def create_director(session: Session, name: str):
    try:
        director = Director(name=name)
        session.add(director)
        session.commit()
        session.refresh(director)
        return director

    except SQLAlchemyError:
        session.rollback()
        raise

# READ ONE
def read_one_director(session: Session, director_id: int):
    return session.get(Director, director_id)

# READ ALL
def read_all_directors(session: Session):
    return session.query(Director).all()

# UPDATE
def update_director(session: Session, director_id: int, name: str):
    try:
        director = session.get(Director, director_id)
        if not director:
            raise Exception(f"Director {name} not found")
        director.name = name
        session.commit()
        return director

    except SQLAlchemyError:
        session.rollback()
        raise

# DELETE
def delete_director(session: Session, director_id: int):
    try:
        director = session.get(Director, director_id)
        if not director:
            raise Exception(f"Director {name} not found")
        session.delete(director)
        session.commit()
        return director

    except SQLAlchemyError:
        session.rollback()
        raise

# CRUD FOR STUDIOS
# CREATE
def create_studio(session: Session, name: str):
    try:
        studio = Studio(name=name)
        session.add(studio)
        session.commit()
        session.refresh(studio)
        return studio

    except SQLAlchemyError:
        session.rollback()
        raise

# READ ONE
def read_one_studio(session: Session, studio_id: int):
    return session.get(Studio, studio_id)

# READ ALL
def read_all_studios(session: Session):
    return session.query(Studio).all()

# UPDATE
def update_studio(session: Session, studio_id: int, name: str):
    try:
        studio = session.get(Studio, studio_id)
        if not studio:
            raise Exception(f"Studio {name} not found")
        studio.name = name
        session.commit()
        return studio

    except SQLAlchemyError:
        session.rollback()
        raise

# DELETE
def delete_studio(session: Session, studio_id: int):
    try:
        studio = session.get(Studio, studio_id)
        if not studio:
            raise Exception(f"Studio {name} not found")
        session.delete(studio)
        session.commit()
        return studio

    except SQLAlchemyError:
        session.rollback()
        raise

# CRUD FOR PROJECTS
# CREATE
def create_project(session: Session, data: dict):
    try:
        project = Project(**data)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    except SQLAlchemyError:
        session.rollback()
        raise

# READ ONE
def read_one_project(session: Session, project_id: int):
    return session.get(Project, project_id)

# READ ALL
def read_all_projects(session: Session):
    return session.query(Project).all()

# UPDATE
def update_project(session: Session, project_id: int, data: dict):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")

        for key, value in data.items():
            setattr(project, key, value)

        session.commit()
        return project

    except SQLAlchemyError:
        session.rollback()
        raise

# DELETE
def delete_project(session: Session, project_id: int):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")
        session.delete(project)
        session.commit()
        return project

    except SQLAlchemyError:
        session.rollback()
        raise

# CRUD FOR ACTORS
# CREATE
def create_actor(session: Session, name: str):
    try:
        actor = Actor(name=name)
        session.add(actor)
        session.commit()
        session.refresh(actor)
        return actor

    except SQLAlchemyError:
        session.rollback()
        raise

# READ ONE
def read_one_actor(session: Session, actor_id: int):
    return session.get(Actor, actor_id)

# READ ALL
def read_all_actors(session: Session):
    return session.query(Actor).all()

# UPDATE
def update_actor(session: Session, actor_id: int, name: str):
    try:
        actor = session.get(Actor, actor_id)
        if not actor:
            raise Exception(f"Actor {name} not found")
        actor.name = name
        session.commit()
        return actor

    except SQLAlchemyError:
        session.rollback()
        raise

# DELETE
def delete_actor(session: Session, actor_id: int):
    try:
        actor = session.get(Actor, actor_id)
        if not actor:
            raise Exception(f"Actor {name} not found")
        session.delete(actor)
        session.commit()
        return actor

    except SQLAlchemyError:
        session.rollback()
        raise

# ADD ACTOR TO PROJECT
def add_actor_to_project(session: Session, project_id: int, actor_id: int, role: str):
    try:
        link = ProjectCast(project_id=project_id, actor_id=actor_id, role=role)
        session.add(link)
        session.commit()
        return link

    except SQLAlchemyError:
        session.rollback()
        raise

# GET PROJECT CAST
def get_project_cast(session: Session, project_id: int):
    return session.query(ProjectCast).filter_by(project_id=project_id).all()

# DELETE ACTOR FROM PROJECT
def delete_actor_from_project(session: Session, project_id: int, actor_id: int):
    try:
        link = session.query(ProjectCast).filter_by(project_id=project_id,actor_id=actor_id).first()
        if not link:
            raise Exception(f"Actor {actor_id} not found")
        session.delete(link)
        session.commit()
        return True

    except SQLAlchemyError:
        session.rollback()
        raise

# ADD GENRE TO PROJECT
def add_genre_to_project(session: Session, project_id: int, genre_id: int):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")

        genre = session.get(Genre, genre_id)
        if not genre:
            raise Exception(f"Genre {genre_id} not found")

        project.genres.append(genre)
        session.commit()

        return project

    except SQLAlchemyError:
        session.rollback()
        raise

# DELETE GENRE FROM PROJECT
def delete_genre_from_project(session: Session, project_id: int, genre_id: int):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")

        genre = session.get(Genre, genre_id)
        if not genre:
            raise Exception(f"Genre {genre_id} not found")

        project.genres.remove(genre)
        session.commit()
        return True

    except SQLAlchemyError:
        session.rollback()
        raise

# ADD PROJECT ON PLATFORM
def add_project_to_platform(session: Session, project_id: int, platform_id: int):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")

        platform = session.get(Platform, platform_id)
        if not platform:
            raise Exception(f"Platform {platform_id} not found")

        project.platforms.append(platform)
        session.commit()

        return project

    except SQLAlchemyError:
        session.rollback()
        raise

# REMOVE PROJECT FROM PLATFORM
def remove_project_from_platform(session: Session, project_id: int, platform_id: int):
    try:
        project = session.get(Project, project_id)
        if not project:
            raise Exception(f"Project {project_id} not found")

        platform = session.get(Platform, platform_id)
        if not platform:
            raise Exception(f"Platform {platform_id} not found")

        project.platforms.remove(platform)
        session.commit()

        return True

    except SQLAlchemyError:
        session.rollback()
        raise
