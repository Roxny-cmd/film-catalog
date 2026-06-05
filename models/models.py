from sqlalchemy import  Column, Integer, String, Date, Numeric, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

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

    casts = relationship("ProjectCast",back_populates="actor",cascade="all, delete-orphan")

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("Project",back_populates="country")

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False, index=True)

    projects = relationship("ProjectOnPlatform", back_populates="platform")

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
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        CheckConstraint("project_type IN ('film', 'serial')", name='check_film_or_serial'),
        CheckConstraint("rating >= 0 AND rating <= 10", name='check_rating'),
    )

    director = relationship("Director",back_populates="projects")
    studio = relationship("Studio",back_populates="projects")
    country = relationship("Country",back_populates="projects")
    casts = relationship("ProjectCast",back_populates="project",cascade="all, delete-orphan")
    genres = relationship("Genre", secondary="project_genre",back_populates="projects")
    platforms = relationship("ProjectOnPlatform",back_populates="projects",cascade="all, delete-orphan")

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="projects")

class ProjectCast(Base):
    __tablename__ = 'project_cast'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True)

    role = Column(String(256), nullable=False)

    project = relationship("Project", back_populates="casts")
    actor = relationship("Actor", back_populates="casts")

class ProjectGenre(Base):
    __tablename__ = 'project_genre'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)

class ProjectOnPlatform(Base):
    __tablename__ = 'project_on_platform'

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"), primary_key=True)

    project = relationship("Project", back_populates="platforms")  # было "projects"
    platform = relationship("Platform", back_populates="projects")